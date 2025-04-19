from stable_baselines3.common.distributions import Distribution
import torch as th
import gymnasium as gym

class HybridDistribution(Distribution):
    def __init__(self, discrete_logits, continuous_mean, continuous_std, binary_logits, flat_keys, sizes, original_action_space):
        super().__init__()
        self.discrete_logits = discrete_logits
        self.continuous_mean = continuous_mean
        self.continuous_std = continuous_std
        self.binary_logits = binary_logits
        self.original_action_space = original_action_space

        self.flat_keys = flat_keys
        self.sizes = sizes

        # Verteilungen aufbauen
        self.discrete_dists = []
        self.continuous_dists = []
        self.binary_dists = []

        # Wir gehen über die flat_keys durch, genauso wie im ActionWrapper
        self.split_logits = []
        self.split_index = 0

        for i, key in enumerate(flat_keys):
            space = original_action_space.spaces[key]
            size = sizes[i]

            if isinstance(space, gym.spaces.Discrete):
                # Nimm next chunk aus logits
                logits = discrete_logits[:, self.split_index:self.split_index + space.n]
                self.discrete_dists.append(th.distributions.Categorical(logits=logits))
                self.split_index += space.n

            elif isinstance(space, gym.spaces.Box):
                mean = continuous_mean[:, self.split_index:self.split_index + size]
                std = continuous_std[:, self.split_index:self.split_index + size]
                self.continuous_dists.append(th.distributions.Normal(mean, std))
                self.split_index += size

            elif isinstance(space, gym.spaces.MultiBinary):
                logits = binary_logits[:, self.split_index:self.split_index + size]
                self.binary_dists.append(th.distributions.Bernoulli(logits=logits))
                self.split_index += size

            else:
                raise NotImplementedError(f"Action type {type(space)} not supported.")

    def sample(self):
        samples = []
        for dist in self.discrete_dists:
            samples.append(dist.sample().unsqueeze(-1))
        for dist in self.continuous_dists:
            samples.append(dist.sample())
        for dist in self.binary_dists:
            samples.append(dist.sample())
        return th.cat(samples, dim=-1)

    def mode(self):
        modes = []
        for dist in self.discrete_dists:
            modes.append(dist.probs.argmax(dim=-1, keepdim=True))
        for dist in self.continuous_dists:
            modes.append(dist.mean)
        for dist in self.binary_dists:
            modes.append((dist.probs > 0.5).float())
        return th.cat(modes, dim=-1)

    def log_prob(self, actions):
        splits = th.split(actions, self.sizes, dim=-1)

        log_probs = []
        d_idx = 0
        c_idx = 0
        b_idx = 0

        for i, key in enumerate(self.flat_keys):
            space = self.original_action_space.spaces[key]
            action_part = splits[i]

            if isinstance(space, gym.spaces.Discrete):
                log_probs.append(self.discrete_dists[d_idx].log_prob(action_part.squeeze(-1)))
                d_idx += 1
            elif isinstance(space, gym.spaces.Box):
                log_probs.append(self.continuous_dists[c_idx].log_prob(action_part).sum(-1))
                c_idx += 1
            elif isinstance(space, gym.spaces.MultiBinary):
                log_probs.append(self.binary_dists[b_idx].log_prob(action_part).sum(-1))
                b_idx += 1

        return sum(log_probs)

    def entropy(self):
        ent = 0
        for dist in self.discrete_dists:
            ent += dist.entropy()
        for dist in self.continuous_dists:
            ent += dist.entropy().sum(-1)
        for dist in self.binary_dists:
            ent += dist.entropy().sum(-1)
        return ent

    # SB3-required methods:

    def proba_distribution(self, discrete_logits, continuous_mean, continuous_std, binary_logits):
        return HybridDistribution(
            discrete_logits, continuous_mean, continuous_std, binary_logits,
            self.original_action_space, self.flat_keys, self.sizes
        )

    def log_prob_from_params(self, discrete_logits, continuous_mean, continuous_std, binary_logits, actions):
        dist = self.proba_distribution(discrete_logits, continuous_mean, continuous_std, binary_logits)
        return dist.log_prob(actions)

    def actions_from_params(self, discrete_logits, continuous_mean, continuous_std, binary_logits, deterministic=False):
        dist = self.proba_distribution(discrete_logits, continuous_mean, continuous_std, binary_logits)
        return dist.mode() if deterministic else dist.sample()

    def proba_distribution_net(self, latent_dim):
        raise NotImplementedError("Wird in deiner Custom-Policy implementiert.")
