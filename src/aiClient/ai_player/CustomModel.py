import torch.nn as nn
import torch as th
from gymnasium import spaces
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import gymnasium as gym
import numpy as np

from action_observation_names import *


class CustomFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Dict, features_dim: int = 64):
        super().__init__(observation_space, features_dim)

        #input_size = int(sum(np.prod(space.shape) for space in observation_space.spaces.values()))
        input_size = 4207 # TODO ka wie man es richtig berechnet
        #print("input_size", input_size)
        self.fc = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, features_dim),
            nn.ReLU(),
        )

    def forward(self, obs_dict):
        # return self.fc(x)
        #print(obs_dict)
        obs_list = [obs_dict[key].flatten() for key in obs_dict.keys()]
        obs_tensor = th.cat(obs_list, dim=-1)  # Alle Beobachtungen kombinieren
        obs_tensor = obs_tensor.float()
        # Falls keine Batch-Dimension: hinzufügen
        if obs_tensor.dim() == 1:
            obs_tensor = obs_tensor.unsqueeze(0)
            #print(obs_tensor.shape)
        return self.fc(obs_tensor)


class HybridActorCriticPolicy(ActorCriticPolicy):
    def __init__(self, observation_space, action_space, schedule, **kwargs):
        self.original_action_space: spaces.Dict = kwargs.pop("original_action_space", action_space)
        super().__init__(observation_space, action_space, schedule, **kwargs)

        self.discrete_keys = [key for key in self.original_action_space.spaces if isinstance(self.original_action_space.spaces[key], gym.spaces.Discrete)]
        self.continuous_keys = [key for key in self.original_action_space.spaces if isinstance(self.original_action_space.spaces[key], gym.spaces.Box)]
        self.binary_keys = [key for key in self.original_action_space.spaces if isinstance(self.original_action_space.spaces[key], gym.spaces.MultiBinary)]

        self.num_discrete = sum(self.original_action_space.spaces[key].n for key in self.discrete_keys)
        self.num_continuous = sum(self.original_action_space.spaces[key].shape[0] for key in self.continuous_keys)
        self.num_binary = sum(self.original_action_space.spaces[key].n for key in self.binary_keys)

        features_dim = 64
        self.features_extractor = CustomFeatureExtractor(observation_space, features_dim)

        self.discrete_policy = nn.Linear(features_dim, self.num_discrete)
        self.continuous_policy = nn.Linear(features_dim, self.num_continuous)
        self.binary_policy = nn.Linear(features_dim, self.num_binary)  # MultiBinary als Logits

        self.log_std = nn.Parameter(th.zeros(self.num_continuous))

    def forward(self, obs, deterministic=False):
        features = self.features_extractor(obs)
        # Falls einzelne Beobachtung: Batch-Dimension hinzufügen
        if features.dim() == 1:
            features = features.unsqueeze(0)

        # Aktionen berechnen
        masked_discrete_logits, continuous_mean, masked_binary_logits = self._get_action_logits(obs, features)

        return masked_discrete_logits, continuous_mean, masked_binary_logits

    def _get_action_logits(self, obs, features):
        """
        Hilfsfunktion: Berechnet und maskiert die Logits für alle Aktionstypen.
        Gibt zurück:
            - masked_discrete_logits
            - continuous_mean
            - masked_binary_logits
        """
        discrete_logits = self.discrete_policy(features)
        masked_discrete_logits = []
        start_idx = 0
        for key in self.discrete_keys:
            num_values = self.original_action_space.spaces[key].n
            logits = discrete_logits[:, start_idx:start_idx + num_values]

            if key in self.discrete_mask_mapping:
                # print(key)
                mask_key = self.discrete_mask_mapping[key]
                mask = obs[mask_key]
                mask = mask.float()
                #print(mask)
                if mask.sum() == 0:
                    raise ValueError(f"Mask for '{key}' has no valid actions!")
                if mask.dim() == 1:
                    mask = mask.unsqueeze(0)
                mask = mask.expand(logits.size(0), -1)
                logits = logits.masked_fill(mask == 0, -float("inf"))

            masked_discrete_logits.append(logits)
            start_idx += num_values
        masked_discrete_logits = th.cat(masked_discrete_logits, dim=-1)  # Wieder zusammenführen

        # Kontinuierliche Mittelwerte
        continuous_mean = self.continuous_policy(features)

        # **MultiBinary Logits maskieren**
        binary_logits = self.binary_policy(features)  # MultiBinary Logits
        masked_binary_logits = []
        start_idx = 0
        for key in self.binary_keys:
            num_values = self.original_action_space.spaces[key].n
            logits = binary_logits[:, start_idx:start_idx + num_values]

            if key in self.binary_mask_mapping:
                mask_key = self.binary_mask_mapping[key]
                mask = obs[mask_key]
                if mask.dim() == 1:
                    mask = mask.unsqueeze(0)
                mask = mask.expand(logits.size(0), -1)
                # logits = logits + (1 - mask) * -float('inf')
                logits = logits.masked_fill(mask == 0, -float("inf"))

            masked_binary_logits.append(logits)
            start_idx += num_values
        masked_binary_logits = th.cat(masked_binary_logits, dim=-1)  # Wieder zusammenführen

        print("_get_action_logits: ", masked_discrete_logits.shape, continuous_mean.shape, binary_logits.shape)
        return masked_discrete_logits, continuous_mean, masked_binary_logits

    def _predict(self, obs, deterministic=False):
        masked_discrete_logits, continuous_mean, masked_binary_logits = self.forward(obs)

        # Indizes für kontinuierlich, diskret, binär
        discrete_idx = 0
        continuous_idx = 0
        binary_idx = 0

        action_parts = []

        for key in self.original_action_space.spaces:
            space = self.original_action_space.spaces[key]
            if isinstance(space, gym.spaces.Discrete):
                num_values = space.n
                logits = masked_discrete_logits[:, discrete_idx:discrete_idx + num_values]
                probs = th.nn.functional.softmax(logits, dim=-1)

                if deterministic:
                    action = th.argmax(probs, dim=-1).float()  # float für Kompatibilität mit Box
                else:
                    action = th.distributions.Categorical(probs=probs).sample().float()

                action_parts.append(action.unsqueeze(-1))  # [B, 1]
                discrete_idx += num_values

            elif isinstance(space, gym.spaces.Box):
                size = int(np.prod(space.shape))
                if deterministic:
                    action = continuous_mean[:, continuous_idx:continuous_idx + size]
                else:
                    std = th.exp(self.log_std[continuous_idx:continuous_idx + size])
                    noise = th.randn_like(continuous_mean[:, continuous_idx:continuous_idx + size])
                    action = continuous_mean[:, continuous_idx:continuous_idx + size] + std * noise

                action_parts.append(action)
                continuous_idx += size

            elif isinstance(space, gym.spaces.MultiBinary):
                num_values = space.n
                logits = masked_binary_logits[:, binary_idx:binary_idx + num_values]
                probs = th.sigmoid(logits)

                if key == TWO_SELECTED_CARDS_INDICES:
                    if deterministic:
                        top2 = probs.topk(2, dim=-1).indices
                        action = th.zeros_like(probs)
                        action.scatter_(-1, top2, 1)
                    else:
                        selected = th.multinomial(probs, num_samples=2, replacement=False)
                        action = th.zeros_like(probs)
                        action.scatter_(-1, selected, 1)
                else:
                    if deterministic:
                        action = (probs > 0.5).float()
                    else:
                        action = th.distributions.Bernoulli(probs=probs).sample()

                action_parts.append(action)
                binary_idx += num_values

            else:
                raise NotImplementedError(f"Unsupported action type: {type(space)}")

        # Finales Flattening
        flat_action = th.cat(action_parts, dim=-1)  # [B, total_action_dim]
        print("_predict: ", flat_action.squeeze(0).shape)
        return flat_action.squeeze(0)  # Falls nur ein Sample, [1, D] → [D]







        # Diskrete Aktion
        # discrete_probs = th.nn.functional.softmax(masked_discrete_logits, dim=-1)
        # if deterministic:
        #     discrete_action = th.argmax(discrete_probs, dim=-1)
        # else:
        #     discrete_action = th.distributions.Categorical(probs=discrete_probs).sample()
        discrete_actions = []
        start_idx = 0
        for key in self.discrete_keys:
            print(key)
            num_values = self.original_action_space.spaces[key].n
            logits = masked_discrete_logits[:, start_idx:start_idx + num_values]
            probs = th.nn.functional.softmax(logits, dim=-1)
            if deterministic:
                action = th.argmax(probs, dim=-1)
            else:
                action = th.distributions.Categorical(probs=probs).sample()
            discrete_actions.append(action)
            start_idx += num_values
        discrete_action = th.stack(discrete_actions, dim=-1)  # Richtige Struktur wiederherstellen

        # Kontinuierliche Aktion
        continuous_std = th.exp(self.log_std)
        if deterministic:
            continuous_action = continuous_mean
        else:
            continuous_action = continuous_mean + continuous_std * th.randn_like(continuous_mean)

        # # MultiBinary Aktion
        # binary_probs = th.sigmoid(masked_binary_logits)
        # if deterministic:
        #     binary_action = (binary_probs > 0.5).float()
        # else:
        #     binary_action = th.distributions.Bernoulli(probs=binary_probs).sample()

        binary_actions = []
        start_idx = 0
        for key in self.binary_keys:
            num_values = self.original_action_space.spaces[key].n
            logits = masked_binary_logits[:, start_idx:start_idx + num_values]
            probs = th.sigmoid(logits)  # Wahrscheinlichkeiten aus Logits berechnen

            if key == TWO_SELECTED_CARDS_INDICES:
                # Falls deterministic, wähle die 2 größten Wahrscheinlichkeiten
                if deterministic:
                    top2_indices = probs.topk(2, dim=-1).indices  # Indizes der zwei höchsten Werte
                    action = th.zeros_like(probs)  # Erst alle auf 0 setzen
                    action.scatter_(-1, top2_indices, 1)  # Die zwei größten auf 1 setzen
                else:
                    # Stochastische Auswahl von genau 2 Werten proportional zur Wahrscheinlichkeit
                    action = th.zeros_like(probs)  # Erst alle auf 0 setzen
                    selected_indices = th.multinomial(probs, num_samples=2, replacement=False)  # Wähle genau 2 Indizes
                    action.scatter_(-1, selected_indices, 1)  # Setze diese Indizes auf 1
            else:
                # Normale Verarbeitung für alle anderen Keys
                if deterministic:
                    action = (probs > 0.5).float()
                else:
                    action = th.distributions.Bernoulli(probs=probs).sample()

            binary_actions.append(action)
            start_idx += num_values
        binary_action = th.stack(binary_actions, dim=-1) # Richtige Struktur wiederherstellen

        return {
            "discrete": discrete_action,
            "continuous": continuous_action,
            "binary": binary_action
        }


