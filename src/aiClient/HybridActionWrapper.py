import gymnasium as gym
import numpy as np

class HybridActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)

        self.discrete_keys = [key for key in env.action_space.spaces if isinstance(env.action_space.spaces[key], gym.spaces.Discrete)]
        self.continuous_keys = [key for key in env.action_space.spaces if isinstance(env.action_space.spaces[key], gym.spaces.Box)]
        self.binary_keys = [key for key in env.action_space.spaces if isinstance(env.action_space.spaces[key], gym.spaces.MultiBinary)]

        self.num_discrete = sum(env.action_space.spaces[key].n for key in self.discrete_keys)
        self.num_continuous = sum(env.action_space.spaces[key].shape[0] for key in self.continuous_keys)
        self.num_binary = sum(env.action_space.spaces[key].n for key in self.binary_keys)

        # SB3 benötigt eine flache Box-Action
        low = np.concatenate([
            np.full(self.num_discrete, 0.0),  # Diskrete Logits
            np.concatenate([env.action_space.spaces[key].low for key in self.continuous_keys]),  # Kontinuierlich
            np.full(self.num_binary, 0.0)  # MultiBinary (Sigmoid)
        ])
        high = np.concatenate([
            np.full(self.num_discrete, 1.0),  # Diskrete Logits
            np.concatenate([env.action_space.spaces[key].high for key in self.continuous_keys]),  # Kontinuierlich
            np.full(self.num_binary, 1.0)  # MultiBinary (Sigmoid)
        ])
        self.action_space = gym.spaces.Box(low=low, high=high, dtype=np.float32)

    def action(self, action):
        """ Wandelt eine SB3-Box-Action in ein Dict mit diskreten, kontinuierlichen und MultiBinary-Aktionen um. """
        idx = 0
        discrete_actions = {}
        for key in self.discrete_keys:
            num_values = self.env.action_space.spaces[key].n
            discrete_logits = action[idx:idx + num_values]
            discrete_actions[key] = np.argmax(discrete_logits)  # Masking in Policy
            idx += num_values

        continuous_actions = {}
        for key in self.continuous_keys:
            num_values = self.env.action_space.spaces[key].shape[0]
            continuous_actions[key] = action[idx:idx + num_values]
            idx += num_values

        binary_actions = {}
        for key in self.binary_keys:
            num_values = self.env.action_space.spaces[key].n
            binary_logits = action[idx:idx + num_values]
            binary_actions[key] = (binary_logits > 0.5).astype(np.int32)  # Masking in Policy
            idx += num_values

        return {**discrete_actions, **continuous_actions, **binary_actions}

