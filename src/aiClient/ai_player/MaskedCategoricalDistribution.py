import torch
from torch.distributions import Categorical

class MaskedCategoricalDistribution:
    def __init__(self, logits: torch.Tensor, mask: torch.Tensor):
        # logits: [batch_size, num_actions]
        # mask: [batch_size, num_actions] (bool)
        logits = logits.clone()
        #print(logits)
        #print(mask)
        logits[~mask] = float('-inf')
        self.dist = Categorical(logits=logits)

    def sample(self):
        return self.dist.sample()

    def log_prob(self, actions):
        return self.dist.log_prob(actions)

    def entropy(self):
        return self.dist.entropy()

    def mode(self):
        return torch.argmax(self.dist.probs, dim=-1)

    def probs(self):
        return self.dist.probs
