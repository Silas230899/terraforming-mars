import torch
from stable_baselines3.common.policies import ActorCriticPolicy
import gymnasium as gym

from action_observation_names import *
from ai_player.HybridMaskedDistribution import HybridMaskedDistribution


class HybridActorCriticPolicy(ActorCriticPolicy):

    def __init__(self, observation_space, action_space, lr_schedule, **kwargs):
        self.flat_keys = kwargs.pop('flat_keys')
        self.original_action_space = kwargs.pop("original_action_space")

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
        super().__init__(observation_space, action_space, lr_schedule, **kwargs)

        self.action_index_mapping = self.build_action_index_mapping()

    def build_action_index_mapping(self):
        mapping = {}
        idx = 0
        for key in self.flat_keys:
            space = self.original_action_space.spaces[key]
            size = 1 if isinstance(space, gym.spaces.Discrete) else space.shape[0]
            mapping[key] = (idx, idx + size)
            idx += size
        return mapping

    def _get_action_masks(self, obs):
        discrete_masks = []
        idx = 0
        for key in self.flat_keys:
            space = self.original_action_space.spaces[key]
            if isinstance(space, gym.spaces.Discrete):
                if key in self.discrete_mask_mapping:
                    mask_tensor = obs[self.discrete_mask_mapping[key]].bool()
                else:
                    mask_tensor = None
                print(key, space, "mask size", mask_tensor.shape if mask_tensor is not None else None)
                discrete_masks.append(mask_tensor)
            elif isinstance(space, gym.spaces.MultiBinary):
                if key in self.binary_mask_mapping:
                    mask_tensor = obs[self.binary_mask_mapping[key]].bool()
                    # Optional: Hier könntest du später einen Binary-Sampler bauen
                else:
                    mask_tensor = None
            # Boxes haben keine Masken
        return discrete_masks

    def forward(self, obs, deterministic=False):
        features = self.extract_features(obs)
        latent_pi, latent_vf = self.mlp_extractor(features)

        logits = self.action_net(latent_pi)
        values = self.value_net(latent_vf)

        discrete_logits = []
        continuous_parts = []
        discrete_masks = []

        idx = 0
        for key in self.flat_keys:
            space = self.original_action_space.spaces[key]
            size = 1 if isinstance(space, gym.spaces.Discrete) else space.shape[0]
            out = logits[:, idx:idx + size]
            idx += size

            if isinstance(space, gym.spaces.Discrete):
                print(key, space, out)
                discrete_logits.append(out)
            elif isinstance(space, (gym.spaces.Box, gym.spaces.MultiBinary)):
                mean = out
                std = torch.ones_like(mean)
                continuous_parts.append((mean, std))
        print()
        discrete_masks = self._get_action_masks(obs)
        print("hier", discrete_logits[1], discrete_masks[1])
        dist = HybridMaskedDistribution(discrete_logits, discrete_masks, continuous_parts)

        actions = dist.mode() if deterministic else dist.sample()
        log_prob = dist.log_prob(actions)

        return actions, values, log_prob


