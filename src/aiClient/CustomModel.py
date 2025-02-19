import torch.nn as nn
import torch as th
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import gymnasium as gym
import numpy as np

class CustomFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Dict, features_dim: int = 64):
        super().__init__(observation_space, features_dim)

        input_size = sum(np.prod(space.shape) for space in observation_space.spaces.values())

        self.fc = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, features_dim),
            nn.ReLU(),
        )

    def forward(self, obs_dict):
        # return self.fc(x)
        obs_list = [obs_dict[key].flatten() for key in obs_dict.keys()]
        obs_tensor = th.cat(obs_list, dim=-1)  # Alle Beobachtungen kombinieren
        return self.fc(obs_tensor)


class HybridActorCriticPolicy(ActorCriticPolicy):
    def __init__(self, observation_space, action_space, **kwargs):
        super().__init__(observation_space, action_space, **kwargs)

        self.discrete_keys = [key for key in action_space.spaces if isinstance(action_space.spaces[key], gym.spaces.Discrete)]
        self.continuous_keys = [key for key in action_space.spaces if isinstance(action_space.spaces[key], gym.spaces.Box)]
        self.binary_keys = [key for key in action_space.spaces if isinstance(action_space.spaces[key], gym.spaces.MultiBinary)]

        self.num_discrete = sum(action_space.spaces[key].n for key in self.discrete_keys)
        self.num_continuous = sum(action_space.spaces[key].shape[0] for key in self.continuous_keys)
        self.num_binary = sum(action_space.spaces[key].n for key in self.binary_keys)

        features_dim = 64
        self.features_extractor = CustomFeatureExtractor(observation_space, features_dim)

        self.discrete_policy = nn.Linear(features_dim, self.num_discrete)
        self.continuous_policy = nn.Linear(features_dim, self.num_continuous)
        self.binary_policy = nn.Linear(features_dim, self.num_binary)  # MultiBinary als Logits

        self.log_std = nn.Parameter(th.zeros(self.num_continuous))

    def forward(self, obs, deterministic=False):
        features = self.features_extractor(obs)
        discrete_logits = self.discrete_policy(features)
        continuous_mean = self.continuous_policy(features)
        binary_logits = self.binary_policy(features)  # MultiBinary Logits

        # Extrahiere Masken aus der Beobachtung
        action_masks = {
            "discrete": obs["discrete_mask"],
            "binary": obs["binary_mask"]
        }

        # Diskrete Aktion mit Masking
        masked_discrete_logits = discrete_logits + (1 - action_masks['discrete']) * -float('inf')

        # MultiBinary Aktion mit Masking
        masked_binary_logits = binary_logits + (1 - action_masks['binary']) * -float('inf')

        return masked_discrete_logits, continuous_mean, masked_binary_logits

    def _predict(self, obs, deterministic=False):
        masked_discrete_logits, continuous_mean, masked_binary_logits = self.forward(obs)

        # Diskrete Aktion
        discrete_probs = th.nn.functional.softmax(masked_discrete_logits, dim=-1)
        if deterministic:
            discrete_action = th.argmax(discrete_probs, dim=-1)
        else:
            discrete_action = th.distributions.Categorical(probs=discrete_probs).sample()

        # Kontinuierliche Aktion
        continuous_std = th.exp(self.log_std)
        if deterministic:
            continuous_action = continuous_mean
        else:
            continuous_action = continuous_mean + continuous_std * th.randn_like(continuous_mean)

        # MultiBinary Aktion
        binary_probs = th.sigmoid(masked_binary_logits)
        if deterministic:
            binary_action = (binary_probs > 0.5).float()
        else:
            binary_action = th.distributions.Bernoulli(probs=binary_probs).sample()

        return {
            "discrete": discrete_action,
            "continuous": continuous_action,
            "binary": binary_action
        }
