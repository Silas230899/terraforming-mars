import random
import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
from gymnasium import spaces
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env import EnvContext
from ray.rllib.models.catalog import ModelCatalog
from ray.rllib.models.torch.torch_action_dist import TorchDistributionWrapper
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2


### --- Custom Environment --- ###
class HybridMaskedEnv(gym.Env):
    def __init__(self, config: EnvContext = None):
        super().__init__()

        self.action_space = spaces.Dict({
            "SELECTED_CARD_INDEX": spaces.Discrete(5),
            "MULTIPLE_SELECTED_CARDS": spaces.MultiBinary(5),
            "CONTINUOUS_ACTION": spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32),
        })

        self.observation_space = spaces.Dict({
            "features": spaces.Box(low=-1.0, high=1.0, shape=(10,), dtype=np.float32),
            "AVAILABLE_CARDS": spaces.MultiBinary(5),
        })

    def reset(self, *, seed=None, options=None):
        self.state = np.random.uniform(-1, 1, size=(10,))
        obs = {
            "features": self.state.astype(np.float32),
            "AVAILABLE_CARDS": np.array([1, 0, 1, 1, 0], dtype=np.int8),
        }
        return obs, {}

    def step(self, action):
        reward = random.random()
        terminated = random.random() < 0.05
        truncated = False  # Kein Zeitlimit gesetzt
        obs, _ = self.reset()
        return obs, reward, terminated, truncated, {}


### --- Custom Masked MultiBinary --- ###
class MaskedMultiBinaryDistribution:
    def __init__(self, logits, model):
        self.logits = logits
        self.mask = torch.ones_like(logits)

    def sample(self):
        probs = torch.sigmoid(self.logits) * self.mask
        return torch.bernoulli(probs)

    def log_prob(self, action):
        probs = torch.sigmoid(self.logits)
        probs = probs * self.mask + (1 - self.mask) * 0.5
        return (
            action * torch.log(probs + 1e-8) +
            (1 - action) * torch.log(1 - probs + 1e-8)
        ).sum(-1)

    def entropy(self):
        probs = torch.sigmoid(self.logits)
        probs = probs * self.mask + (1 - self.mask) * 0.5
        return -(
            probs * torch.log(probs + 1e-8) +
            (1 - probs) * torch.log(1 - probs + 1e-8)
        ).sum(-1)


### --- Hybrid Model --- ###
class GeneralHybridModel(TorchModelV2, nn.Module):
    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs, model_config, name)
        nn.Module.__init__(self)

        self.fc = nn.Sequential(
            nn.Linear(obs_space["features"].shape[0], 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
        )

        self.discrete_mask_mapping = {
            "SELECTED_CARD_INDEX": "AVAILABLE_CARDS",
        }

        self.binary_mask_mapping = {
            "MULTIPLE_SELECTED_CARDS": "AVAILABLE_CARDS",
        }

        self.action_splits = []
        self.total_output_size = 0
        self.subspaces = []

        for key, space in action_space.spaces.items():
            if isinstance(space, spaces.Discrete):
                size = space.n
            elif isinstance(space, spaces.MultiBinary):
                size = space.n
            elif isinstance(space, spaces.Box):
                size = int(np.prod(space.shape))
            else:
                raise ValueError(f"Unsupported space: {type(space)}")

            self.subspaces.append((key, space))
            self.action_splits.append((self.total_output_size, self.total_output_size + size, key))
            self.total_output_size += size

        self.output_layer = nn.Linear(128, self.total_output_size)
        self.value_branch = nn.Linear(128, 1)
        self._value = None

    def forward(self, input_dict, state, seq_lens):
        x = input_dict["obs"]["features"]
        h = self.fc(x)
        self._value = self.value_branch(h).squeeze(1)
        self.current_obs = input_dict["obs"]
        return self.output_layer(h), state

    def value_function(self):
        return self._value


### --- Custom Distribution --- ###
class GeneralHybridDistribution(TorchDistributionWrapper):
    def __init__(self, inputs, model):
        super().__init__(inputs, model)
        self.model = model
        self.inputs = inputs
        self.sub_dists = {}
        self._split_logits()

    def _split_logits(self):
        for start, end, key in self.model.action_splits:
            subspace = dict(self.model.action_space.spaces)[key]
            logits = self.inputs[:, start:end]

            if isinstance(subspace, spaces.Discrete):
                mask_key = self.model.discrete_mask_mapping.get(key)
                if mask_key and mask_key in self.model.current_obs:
                    mask = self.model.current_obs[mask_key]
                    logits = logits.clone()
                    logits[mask == 0] = float("-inf")
                self.sub_dists[key] = torch.distributions.Categorical(logits=logits)

            elif isinstance(subspace, spaces.MultiBinary):
                dist = MaskedMultiBinaryDistribution(logits, self.model)
                mask_key = self.model.binary_mask_mapping.get(key)
                if mask_key and mask_key in self.model.current_obs:
                    dist.mask = self.model.current_obs[mask_key]
                self.sub_dists[key] = dist

            elif isinstance(subspace, spaces.Box):
                self.sub_dists[key] = torch.distributions.Normal(loc=logits, scale=1.0)

    def sample(self):
        return {
            k: (d.sample() if not isinstance(d, torch.distributions.Normal) else d.sample())
            for k, d in self.sub_dists.items()
        }

    def deterministic_sample(self):
        return {
            k: (
                torch.argmax(d.logits, dim=-1) if isinstance(d, torch.distributions.Categorical)
                else ((d.logits > 0.5).float() * d.mask if isinstance(d, MaskedMultiBinaryDistribution)
                      else d.mean)
            )
            for k, d in self.sub_dists.items()
        }

    def logp(self, actions):
        return torch.stack([
            d.log_prob(actions[k]).sum(-1)
            for k, d in self.sub_dists.items()
        ], dim=0).sum(0)

    def entropy(self):
        return torch.stack([
            d.entropy().sum(-1)
            for d in self.sub_dists.values()
        ], dim=0).sum(0)


### --- Register & Train --- ###
if __name__ == "__main__":
    import ray
    ray.init()

    ModelCatalog.register_custom_model("general_hybrid_model", GeneralHybridModel)
    ModelCatalog.register_custom_action_dist("general_hybrid_dist", GeneralHybridDistribution)

    config = (
        PPOConfig()
        .environment(HybridMaskedEnv)
        .framework("torch")
        .experimental(_validate_config=False)
        .api_stack(enable_rl_module_and_learner=False)
        .env_runners(num_env_runners=0)
        .training(
            model={
                "custom_model": "general_hybrid_model",
                "custom_action_dist": "general_hybrid_dist"
            },
            train_batch_size=200,
        )
    )

    algo = config.build_algo()
    for i in range(10):
        result = algo.train()
        print(f"Iter {i}: reward = {result['episode_reward_mean']:.3f}")
