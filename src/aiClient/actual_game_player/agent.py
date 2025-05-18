import json
import sys

from Player import Player
from actual_game_player.CustomEnvironment3 import CustomEnv3, create_action_from_observation
from ai_player.network_related import create_game
from ai_player.tfm_settings import settings

if __name__ == '__main__':
    env = CustomEnv3()

    user_input = None
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Enter comma seperated color, id and name of player:")

    player = Player(*user_input.split(","))
    env.observed_player = player

    obs1, _ = env.reset()
    done = False
    while not done:
        action1 = create_action_from_observation(env.action_space, obs1)
        obs1, reward, done, _, _ = env.step(action1)
    print(f"Game has ended successfully. View stats http://localhost:8080/the-end?id={player.id}")

    # $env:PYTHONPATH="E:\Programmieren\WebStorm\terraforming-mars\src\aiClient"