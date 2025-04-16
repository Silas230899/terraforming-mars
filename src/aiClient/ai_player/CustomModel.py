import torch.nn as nn
import torch as th
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import gymnasium as gym
import numpy as np

from action_observation_names import *


class CustomFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Dict, features_dim: int = 64):
        super().__init__(observation_space, features_dim)

        input_size = int(sum(np.prod(space.shape) for space in observation_space.spaces.values()))

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
        obs_tensor = obs_tensor.float()
        # Falls keine Batch-Dimension: hinzufügen
        if obs_tensor.dim() == 1:
            obs_tensor = obs_tensor.unsqueeze(0)
        return self.fc(obs_tensor)


class HybridActorCriticPolicy(ActorCriticPolicy):
    def __init__(self, observation_space, action_space, schedule, **kwargs):
        self.original_action_space = kwargs.pop("original_action_space", action_space)
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

        # **Manuelle Zuordnung der Maskierungs-Beobachtungen**
        self.discrete_mask_mapping = {
            SELECTED_ACTION_OPTION_INDEX: AVAILABLE_ACTION_OPTIONS,
            SELECTED_CARD_INDEX: AVAILABLE_CARDS,
            SELECTED_PROJECT_CARD_INDEX: AVAILABLE_PROJECT_CARDS,
            SELECTED_CARD_TO_DISCARD_INDEX: AVAILABLE_CARDS_TO_DISCARD,
            SELECTED_CARD_TO_ADD_3_MICROBES_TO_INDEX: AVAILABLE_CARDS_TO_ADD_3_MICROBES_TO,
            SELECTED_CARD_TO_ADD_2_MICROBES_TO_INDEX: AVAILABLE_CARDS_TO_ADD_2_MICROBES_TO,
            SELECTED_CARD_TO_REMOVE_2_ANIMALS_FROM_INDEX: AVAILABLE_CARDS_TO_REMOVE_2_ANIMALS_FROM,
            SELECTED_CARD_TO_ADD_2_ANIMALS_TO_INDEX: AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO,
            SELECTED_CARD_TO_ADD_4_ANIMALS_TO_INDEX: AVAILABLE_CARDS_TO_ADD_4_ANIMALS_TO,
            SELECTED_CARD_TO_ADD_2_ANIMALS_TO_2_INDEX: AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO_2,

            SELECTED_SPACE_INDEX: AVAILABLE_SPACES,
            SELECTED_PLAYER: AVAILABLE_PLAYERS,
            SELECTED_CARD_WITH_ACTION_INDEX: PLAYED_CARDS_WITH_ACTIONS,
            SELECTED_STANDARD_PROJECT_INDEX: AVAILABLE_STANDARD_PROJECTS,
            SELECTED_CORPORATION: AVAILABLE_CORPORATIONS,
        }

        self.binary_mask_mapping = {
            MULTIPLE_SELECTED_CARDS: AVAILABLE_CARDS,
            TWO_SELECTED_CARDS_INDICES: AVAILABLE_CARDS,
            MULTIPLE_SELECTED_RESEARCH_CARDS: AVAILABLE_CARDS,
        }

    def forward(self, obs, deterministic=False):
        features = self.features_extractor(obs)
        # Falls einzelne Beobachtung: Batch-Dimension hinzufügen
        if features.dim() == 1:
            features = features.unsqueeze(0)
        discrete_logits = self.discrete_policy(features)
        continuous_mean = self.continuous_policy(features)
        binary_logits = self.binary_policy(features)  # MultiBinary Logits

        # **Masken anhand der definierten Mappings abrufen**
        discrete_masks = [obs[self.discrete_mask_mapping[key]] for key in self.discrete_keys if
                          key in self.discrete_mask_mapping]
        binary_masks = [obs[self.binary_mask_mapping[key]] for key in self.binary_keys if
                        key in self.binary_mask_mapping]

        # **Diskrete Logits maskieren**
        masked_discrete_logits = []
        start_idx = 0
        for key in self.discrete_keys:
            num_values = self.original_action_space.spaces[key].n
            logits = discrete_logits[:, start_idx:start_idx + num_values]

            if key in self.discrete_mask_mapping:
                #print(key)
                mask_key = self.discrete_mask_mapping[key]
                mask = obs[mask_key]
                mask = mask.float()
                print(mask)
                if mask.sum() == 0:
                    raise ValueError(f"Mask for '{key}' has no valid actions!")
                #print("mask dim: ", mask.dim(), mask.shape, mask.size())
                #print("logits: ", logits.shape)
                if mask.dim() == 1:
                    mask = mask.unsqueeze(0)
                mask = mask.expand(logits.size(0), -1)
                print("logits vorher: ", logits)
                # logits = logits + (1 - mask) * -float('inf')
                logits = logits.masked_fill(mask == 0, -float("inf"))
                print("in between1:", (1 - mask))
                print("in between2:", ((1 - mask) * -float('inf')))
                print(key, logits)
                print()

            masked_discrete_logits.append(logits)
            start_idx += num_values
        masked_discrete_logits = th.cat(masked_discrete_logits, dim=-1)  # Wieder zusammenführen

        # **MultiBinary Logits maskieren**
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
        print("forwarding done")
        return masked_discrete_logits, continuous_mean, masked_binary_logits

    def _predict(self, obs, deterministic=False):
        masked_discrete_logits, continuous_mean, masked_binary_logits = self.forward(obs)

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
