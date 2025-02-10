import numpy as np
from gymnasium.wrappers import FlattenObservation
#from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from CustomEnvironment import CustomEnv
from HybridActionWrapper import HybridActionWrapper
from ppo import PPO

if __name__ == '__main__':
    env1 = CustomEnv()
    wrapped_env = HybridActionWrapper(env1)
    env = DummyVecEnv([lambda: wrapped_env])

    current_observation = env.reset()
    while True:
        # theoretically calc action from current_observation
        env1.current_turn = 5
        env1.last_observation = current_observation
        sample = env.action_space.sample()
        new_obs, rewards, dones, infos = env.step([sample])
        current_observation = new_obs
        if dones[0]: break


    #env = FlattenObservation(env)

    #model2 = PPO("MultiInputPolicy", env, verbose=1, n_steps=32, batch_size=8)
    #model2.learn(total_timesteps=512, progress_bar=True, log_interval=1)

