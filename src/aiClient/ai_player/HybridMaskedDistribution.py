import torch
from torch.distributions import Categorical, Normal

from ai_player.MaskedCategoricalDistribution import MaskedCategoricalDistribution


class HybridMaskedDistribution:
    def __init__(self, discrete_logits, discrete_masks, continuous_parts):
        self.discrete_dists = []
        self.continuous_dists = []

        #print(discrete_masks[1], discrete_masks[1])

        #print(len(discrete_logits), len(discrete_masks))
        #print(discrete_logits, "now masks:", discrete_masks)

        for logits, mask in zip(discrete_logits, discrete_masks):
            print("xyz:", logits, mask)
            if mask is not None:
                self.discrete_dists.append(MaskedCategoricalDistribution(logits, mask))
            else:
                self.discrete_dists.append(Categorical(logits=logits))

        for mean, std in continuous_parts:
            self.continuous_dists.append(Normal(mean, std))

    def sample(self):
        discrete_actions = [dist.sample() for dist in self.discrete_dists]
        continuous_actions = [dist.sample() for dist in self.continuous_dists]
        return torch.cat(discrete_actions + continuous_actions, dim=-1)

    def log_prob(self, actions):
        log_probs = []
        idx = 0
        for dist in self.discrete_dists:
            log_probs.append(dist.log_prob(actions[:, idx]))
            idx += 1
        for dist in self.continuous_dists:
            dim = dist.mean.shape[1]
            log_probs.append(dist.log_prob(actions[:, idx:idx + dim]).sum(dim=1))
            idx += dim
        return sum(log_probs)

    def mode(self):
        discrete_modes = [dist.mode() if hasattr(dist, "mode") else dist.probs.argmax(dim=-1) for dist in self.discrete_dists]
        continuous_means = [dist.mean for dist in self.continuous_dists]
        return torch.cat(discrete_modes + continuous_means, dim=-1)
