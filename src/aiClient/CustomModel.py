import torch.nn as nn
import torch as th
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import gymnasium as gym
import numpy as np

class CustomFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 64):
        super().__init__(observation_space, features_dim)
        self.fc = nn.Sequential(
            nn.Linear(np.prod(observation_space.shape), 128),
            nn.ReLU(),
            nn.Linear(128, features_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.fc(x)


class HybridActorCriticPolicy(ActorCriticPolicy):
    def __init__(self, observation_space, action_space, **kwargs):
        super().__init__(observation_space, action_space, **kwargs)

        # Anzahl der diskreten & kontinuierlichen Aktionen bestimmen
        self.num_discrete = action_space.spaces[0].n
        self.num_continuous = action_space.spaces[1].shape[0]

        # Gemeinsames Feature-Extraktionsnetzwerk
        features_dim = 64  # Größe des gemeinsamen Feature-Outputs
        self.features_extractor = CustomFeatureExtractor(observation_space, features_dim)

        # Diskrete Policy (Softmax-Logits)
        self.discrete_policy = nn.Linear(features_dim, self.num_discrete)

        # Kontinuierliche Policy (Mittelwerte für Normalverteilung)
        self.continuous_policy = nn.Linear(features_dim, self.num_continuous)

        # Standardabweichung für kontinuierliche Aktionen (trainierbare Parameter)
        self.log_std = nn.Parameter(th.zeros(self.num_continuous))

    def forward(self, obs, deterministic: bool = False):
        features = self.features_extractor(obs)

        # Softmax für diskrete Aktion
        discrete_logits = self.discrete_policy(features)

        # Normalverteilte Mittelwerte für kontinuierliche Aktion
        continuous_mean = self.continuous_policy(features)
        continuous_std = th.exp(self.log_std)  # Positiv halten

        return discrete_logits, continuous_mean, continuous_std

    def _predict(self, obs, deterministic=False):
        discrete_logits, continuous_mean, continuous_std = self.forward(obs)

        # Diskrete Aktion: Softmax + Sampling
        discrete_probs = th.nn.functional.softmax(discrete_logits, dim=-1)
        if deterministic:
            discrete_action = th.argmax(discrete_probs, dim=-1)
        else:
            discrete_action = th.multinomial(discrete_probs, num_samples=1).squeeze(dim=-1)

        # Kontinuierliche Aktion: Gauß-Sampling oder deterministisch
        if deterministic:
            continuous_action = continuous_mean
        else:
            continuous_action = continuous_mean + continuous_std * th.randn_like(continuous_mean)

        return th.cat([discrete_action.float().unsqueeze(-1), continuous_action], dim=-1)

class ActorCritic(nn.Module):
    def __init__(self, obs_space, action_space):
        super(ActorCritic, self).__init__()
        # Actor und Critic getrennt modellieren
        self.shared_net = nn.Sequential(
            nn.Linear(obs_space, 128),
            nn.ReLU()
        )
        # Actor (Policy)
        self.actor = nn.Sequential(
            nn.Linear(128, action_space),
            nn.Softmax(dim=-1)
        )
        # Critic (Value-Funktion)
        self.critic = nn.Linear(128, 1)

    def forward(self, x):
        shared = self.shared_net(x)
        return self.actor(shared), self.critic(shared)
