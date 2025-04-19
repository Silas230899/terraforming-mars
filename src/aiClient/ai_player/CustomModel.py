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

        # Aktionen berechnen
        masked_discrete_logits, continuous_mean, masked_binary_logits = self._get_action_logits(obs, features)

        return masked_discrete_logits, continuous_mean, masked_binary_logits

    def _get_action_logits(self, obs, features):
        """
        Hilfsfunktion: Berechnet und maskiert die Logits für alle Aktionstypen.
        """
        discrete_logits = self.discrete_policy(features)
        masked_discrete_logits = []
        start_idx = 0
        for key in self.discrete_keys:
            num_values = self.original_action_space.spaces[key].n
            logits = discrete_logits[:, start_idx:start_idx + num_values]

            if key in self.discrete_mask_mapping:
                mask_key = self.discrete_mask_mapping[key]
                mask = obs[mask_key]
                mask = mask.float()

                # Debug: check mask validity
                if mask.sum() == 0:
                    print(f"WARNING: Mask for '{key}' has no valid actions! Adding a default valid action.")
                    # Add a default valid action at index 0 to avoid errors
                    if mask.dim() == 1:
                        mask[0] = 1.0
                    else:
                        mask[0, 0] = 1.0

                if mask.dim() == 1:
                    mask = mask.unsqueeze(0)
                mask = mask.expand(logits.size(0), -1)
                logits = logits.masked_fill(mask == 0, -float("inf"))

            masked_discrete_logits.append(logits)
            start_idx += num_values
        masked_discrete_logits = th.cat(masked_discrete_logits, dim=-1)

        # Kontinuierliche Mittelwerte
        continuous_mean = self.continuous_policy(features)

        # MultiBinary Logits maskieren
        binary_logits = self.binary_policy(features)
        masked_binary_logits = []
        start_idx = 0
        for key in self.binary_keys:
            num_values = self.original_action_space.spaces[key].n
            logits = binary_logits[:, start_idx:start_idx + num_values]

            if key in self.binary_mask_mapping:
                mask_key = self.binary_mask_mapping[key]
                mask = obs[mask_key]

                # Debug: check mask validity
                if mask.sum() == 0:
                    print(f"WARNING: Binary mask for '{key}' has no valid actions! Using all ones.")
                    # When no valid actions, make all actions valid
                    mask = th.ones_like(mask)

                if mask.dim() == 1:
                    mask = mask.unsqueeze(0)
                mask = mask.expand(logits.size(0), -1)
                logits = logits.masked_fill(mask == 0, -float("inf"))

            masked_binary_logits.append(logits)
            start_idx += num_values
        masked_binary_logits = th.cat(masked_binary_logits, dim=-1)

        print("_get_action_logits shapes: ",
              masked_discrete_logits.shape, continuous_mean.shape, masked_binary_logits.shape)
        return masked_discrete_logits, continuous_mean, masked_binary_logits

    def _predict(self, obs, deterministic=False):
        masked_discrete_logits, continuous_mean, masked_binary_logits = self.forward(obs)

        # Check batch dimension
        batch_size = masked_discrete_logits.shape[0]

        # Initialize list to collect actions for each action type
        actions_list = []

        # Process discrete actions
        discrete_idx = 0
        for key in self.discrete_keys:
            space = self.original_action_space.spaces[key]
            num_values = space.n
            logits = masked_discrete_logits[:, discrete_idx:discrete_idx + num_values]

            if deterministic:
                action = th.argmax(logits, dim=1, keepdim=True).float()
            else:
                probs = th.softmax(logits, dim=1)
                action = th.multinomial(probs, num_samples=1).float()

            actions_list.append(action)
            discrete_idx += num_values

        # Process continuous actions
        continuous_idx = 0
        for key in self.continuous_keys:
            space = self.original_action_space.spaces[key]
            size = int(np.prod(space.shape))

            if deterministic:
                action = continuous_mean[:, continuous_idx:continuous_idx + size]
            else:
                std = th.exp(self.log_std[continuous_idx:continuous_idx + size])
                noise = th.randn_like(continuous_mean[:, continuous_idx:continuous_idx + size])
                action = continuous_mean[:, continuous_idx:continuous_idx + size] + std * noise

            actions_list.append(action)
            continuous_idx += size

        # Process binary actions
        binary_idx = 0
        for key in self.binary_keys:
            space = self.original_action_space.spaces[key]
            num_values = space.n
            logits = masked_binary_logits[:, binary_idx:binary_idx + num_values]

            if key == TWO_SELECTED_CARDS_INDICES:
                # Handle special case for two selected cards
                probs = th.sigmoid(logits)
                action = th.zeros_like(logits)

                for i in range(batch_size):
                    # Check if we have any valid probabilities
                    valid_probs_sum = probs[i].sum().item()

                    if valid_probs_sum > 0:
                        # We have valid probabilities, let's sample
                        if deterministic:
                            # Take top 2 (or fewer if not enough valid ones)
                            num_to_select = min(2, int(th.sum(probs[i] > 0).item()))
                            if num_to_select > 0:
                                values, indices = th.topk(probs[i], k=num_to_select, dim=0)
                                action[i].scatter_(0, indices, 1.0)
                        else:
                            # Sample without replacement (safely)
                            try:
                                # Make sure probabilities are valid
                                safe_probs = probs[i].clone()
                                if safe_probs.sum() <= 0:
                                    # If no valid probs, set uniform distribution
                                    safe_probs = th.ones_like(safe_probs) / safe_probs.size(0)

                                num_samples = min(2, int((safe_probs > 0).sum().item()))
                                if num_samples > 0:
                                    selected = th.multinomial(safe_probs, num_samples=num_samples, replacement=False)
                                    action[i].scatter_(0, selected, 1.0)
                            except Exception as e:
                                print(f"Error sampling for TWO_SELECTED_CARDS_INDICES: {e}")
                                print(f"Probs sum: {probs[i].sum().item()}, max: {probs[i].max().item()}")
                                # Fallback to deterministic
                                num_to_select = min(2, int(th.sum(probs[i] > 0).item()))
                                if num_to_select > 0:
                                    values, indices = th.topk(probs[i], k=num_to_select, dim=0)
                                    action[i].scatter_(0, indices, 1.0)
            else:
                if deterministic:
                    action = (th.sigmoid(logits) > 0.5).float()
                else:
                    action = th.bernoulli(th.sigmoid(logits))

            actions_list.append(action)
            binary_idx += num_values

        # Concatenate all actions
        flat_action = th.cat(actions_list, dim=1)
        print(f"_predict flat_action shape: {flat_action.shape}")

        # Convert to numpy for SB3
        numpy_action = flat_action.detach().cpu().numpy()

        # If batch size is 1, squeeze the batch dimension to match expected shape
        if batch_size == 1:
            numpy_action = numpy_action.squeeze(0)

        print(f"Final numpy action shape: {numpy_action.shape}")
        return flat_action
        #return numpy_action







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


