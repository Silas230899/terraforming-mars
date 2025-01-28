import torch.nn as nn

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
