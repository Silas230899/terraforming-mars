import json

from Player import Player
from actual_game_player.CustomEnvironment3 import CustomEnv3, create_action_from_observation
from ai_player.network_related import create_game
from ai_player.tfm_settings import settings

if __name__ == '__main__':
    env = CustomEnv3()

    env.observed_player = Player(input("Enter player color: "),
                          input("Enter player ID: "),
                          input("Enter player name: "))

    obs1, _ = env.reset()
    done = False
    while not done:
        action1 = create_action_from_observation(env.action_space, obs1)
        obs1, reward, done, _, _ = env.step(action1)
    print("Succesfully done")