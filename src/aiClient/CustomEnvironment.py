import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env


class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()

        # Definiere den Aktions- und Beobachtungsraum
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)

    def reset(self):
        # Initialisiere die Umgebung
        self.state = np.random.uniform(-1, 1)
        return np.array([self.state], dtype=np.float32), {}  # Rückgabe von Beobachtung und Info

    def step(self, action):
        # Aktion ausführen
        self.state += (action - 0.5) * 0.2
        reward = -abs(self.state)  # Belohnung
        done = abs(self.state) > 1  # Episode endet, wenn Zustand > 1
        return np.array([self.state], dtype=np.float32), reward, done, False, {}

    def render(self):
        print(f"Current state: {self.state}")


# Erstelle und überprüfe das Environment
env = CustomEnv()
check_env(env)

# Trainiere den PPO-Agenten
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Teste den Agenten
obs, info = env.reset()
for _ in range(100):
    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render()
    if done:
        break
