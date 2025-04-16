import gymnasium as gym
import numpy as np
from gymnasium import spaces

class HybridActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        print("HybridActionWrapper initialisiert")

        self.original_action_space: spaces.Dict = env.action_space
        self.flat_keys = []
        self.sizes = []
        self.low = []
        self.high = []
        self.dtypes = []

        for key, space in self.original_action_space.spaces.items():
            self.flat_keys.append(key)

            if isinstance(space, spaces.Discrete):
                self.sizes.append(1)
                self.low.append(0)
                self.high.append(space.n - 1)
                self.dtypes.append(np.int32)
            elif isinstance(space, spaces.Box):
                self.sizes.append(np.prod(space.shape))
                self.low.extend(space.low.flatten())
                self.high.extend(space.high.flatten())
                self.dtypes.append(space.dtype)
            elif isinstance(space, spaces.MultiBinary):
                self.sizes.append(space.n)
                self.low.extend([0] * space.n)
                self.high.extend([1] * space.n)
                self.dtypes.append(np.int8)
            else:
                raise NotImplementedError(f"Action type {type(space)} not supported.")

        self.flat_size = sum(self.sizes)
        self.action_space = spaces.Box(
            low=np.array(self.low, dtype=np.float32),
            high=np.array(self.high, dtype=np.float32),
            dtype=np.float32
        )

    def action(self, action_flat: np.ndarray) -> dict:
        print("Action called")
        """
        Convert flat Box action from agent into Dict action for the environment.
        """

        # Falls wir von VecEnv ein (1, N)-Array bekommen
        if isinstance(action_flat, np.ndarray) and len(action_flat.shape) == 2:
            action_flat = action_flat[0]  # nehme nur das erste (und einzige) Environment

        dict_action = {}
        idx = 0
        for i, key in enumerate(self.flat_keys):
            space = self.original_action_space.spaces[key]
            size = self.sizes[i]

            sub_action = action_flat[idx:idx + size]
            idx += size

            if isinstance(space, spaces.Discrete):
                dict_action[key] = int(np.clip(np.round(sub_action[0]), 0, space.n - 1))
            elif isinstance(space, spaces.Box):
                # print(f"[DEBUG] {key}: size={size}, expected_shape={space.shape}, sub_action.shape={np.array(sub_action).shape}")
                # reshaped = np.array(sub_action, dtype=space.dtype).reshape(space.shape)
                sub_action = np.asarray(sub_action).flatten()  # sicheres 1D-Array
                reshaped = sub_action.astype(space.dtype).reshape(space.shape)
                dict_action[key] = np.clip(reshaped, space.low, space.high)
            elif isinstance(space, spaces.MultiBinary):
                binary = (sub_action > 0.5).astype(np.int8)
                dict_action[key] = binary
            else:
                raise NotImplementedError(f"Action type {type(space)} not supported.")

        return dict_action

    # def __init__(self, env):
    #     super().__init__(env)
    #
    #     self.discrete_keys = [key for key in env.action_space.spaces if isinstance(env.action_space.spaces[key], gym.spaces.Discrete)]
    #     self.continuous_keys = [key for key in env.action_space.spaces if isinstance(env.action_space.spaces[key], gym.spaces.Box)]
    #     self.binary_keys = [key for key in env.action_space.spaces if isinstance(env.action_space.spaces[key], gym.spaces.MultiBinary)]
    #
    #     self.num_discrete = sum(env.action_space.spaces[key].n for key in self.discrete_keys)
    #     self.num_continuous = sum(env.action_space.spaces[key].shape[0] for key in self.continuous_keys)
    #     self.num_binary = sum(env.action_space.spaces[key].n for key in self.binary_keys)
    #
    #     # SB3 benötigt eine flache Box-Action
    #     low = np.concatenate([
    #         np.full(self.num_discrete, 0.0),  # Diskrete Logits
    #         np.concatenate([env.action_space.spaces[key].low for key in self.continuous_keys]),  # Kontinuierlich
    #         np.full(self.num_binary, 0.0)  # MultiBinary (Sigmoid)
    #     ])
    #     high = np.concatenate([
    #         np.full(self.num_discrete, 1.0),  # Diskrete Logits
    #         np.concatenate([env.action_space.spaces[key].high for key in self.continuous_keys]),  # Kontinuierlich
    #         np.full(self.num_binary, 1.0)  # MultiBinary (Sigmoid)
    #     ])
    #     self.action_space = gym.spaces.Box(low=low, high=high, dtype=np.float32)
    #
    # def action(self, action):
    #     """Wandelt eine SB3-Box-Action zurück in ein Dict mit allen diskreten, kontinuierlichen und MultiBinary-Aktionen."""
    #     idx = 0
    #     discrete_actions = {}
    #     for key in self.discrete_keys:
    #         num_values = self.env.action_space.spaces[key].n
    #         discrete_logits = action[idx:idx + num_values]
    #         discrete_actions[key] = np.argmax(discrete_logits)  # Masking in Policy
    #         idx += num_values
    #
    #     continuous_actions = {}
    #     for key in self.continuous_keys:
    #         num_values = self.env.action_space.spaces[key].shape[0]
    #         continuous_actions[key] = action[idx:idx + num_values]
    #         idx += num_values
    #
    #     binary_actions = {}
    #     for key in self.binary_keys:
    #         num_values = self.env.action_space.spaces[key].n
    #         binary_logits = action[idx:idx + num_values]
    #         binary_actions[key] = (binary_logits > 0.5).astype(np.int32)  # Masking in Policy
    #         idx += num_values
    #
    #     # Rekonstruiertes Dict genau wie das Original
    #     return {**discrete_actions, **continuous_actions, **binary_actions}





    # def action(self, action):
    #     """ Wandelt eine SB3-Box-Action in ein Dict mit diskreten, kontinuierlichen und MultiBinary-Aktionen um. """
    #     idx = 0
    #     discrete_actions = {}
    #     for key in self.discrete_keys:
    #         num_values = self.env.action_space.spaces[key].n
    #         discrete_logits = action[idx:idx + num_values]
    #         discrete_actions[key] = np.argmax(discrete_logits)  # Masking in Policy
    #         idx += num_values
    #
    #     continuous_actions = {}
    #     for key in self.continuous_keys:
    #         num_values = self.env.action_space.spaces[key].shape[0]
    #         continuous_actions[key] = action[idx:idx + num_values]
    #         idx += num_values
    #
    #     binary_actions = {}
    #     for key in self.binary_keys:
    #         num_values = self.env.action_space.spaces[key].n
    #         binary_logits = action[idx:idx + num_values]
    #         binary_actions[key] = (binary_logits > 0.5).astype(np.int32)  # Masking in Policy
    #         idx += num_values
    #
    #     return {**discrete_actions, **continuous_actions, **binary_actions}

