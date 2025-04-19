import gymnasium as gym
import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class CustomFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Dict, features_dim: int = 64):
        super().__init__(observation_space, features_dim)
        self.observation_space = observation_space
        flat_size = gym.spaces.flatdim(observation_space)
        self.fc = nn.Sequential(
            nn.Linear(flat_size, 128),
            nn.ReLU(),
            nn.Linear(128, features_dim),
            nn.ReLU(),
        )

    def forward(self, observations: dict) -> torch.Tensor:
        obs_list = [observations[key].flatten() for key in observations.keys()]
        obs_tensor = torch.cat(obs_list, dim=-1)  # Alle Beobachtungen kombinieren
        obs_tensor = obs_tensor.float()
        # Falls keine Batch-Dimension: hinzufügen
        if obs_tensor.dim() == 1:
            obs_tensor = obs_tensor.unsqueeze(0)
        return self.fc(obs_tensor)

        flat_obs = gym.spaces.flatten(self.observation_space, observations)
        return self.fc(flat_obs)