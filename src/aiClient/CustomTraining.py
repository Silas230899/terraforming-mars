from gymnasium.wrappers import FlattenObservation
#from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from CustomEnvironment import CustomEnv
from ppo import PPO

if __name__ == '__main__':
    env = CustomEnv()
    #env = DummyVecEnv([lambda: env])
    #env = FlattenObservation(env)
    model2 = PPO("MultiInputPolicy", env, verbose=1, n_steps=32, batch_size=8)
    model2.learn(total_timesteps=512, progress_bar=True, log_interval=1)

