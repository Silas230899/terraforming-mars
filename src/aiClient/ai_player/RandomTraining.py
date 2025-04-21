import numpy as np
from gymnasium import spaces
from gymnasium.spaces import Discrete, Box, MultiBinary

from ai_player.CustomEnvironment import CustomEnv
from ai_player.action_observation_names import *


def create_action_from_observation(action_space: spaces.Dict, obs):
    mask_mapping = {
        # discrete
        SELECTED_ACTION_OPTION_INDEX: AVAILABLE_ACTION_OPTIONS,
        SELECTED_CARD_INDEX: AVAILABLE_CARDS,
        SELECTED_PROJECT_CARD_INDEX: AVAILABLE_PROJECT_CARDS,
        SELECTED_CARD_TO_DISCARD_INDEX: AVAILABLE_CARDS_TO_DISCARD,
        SELECTED_CARD_TO_ADD_3_MICROBES_TO_INDEX: AVAILABLE_CARDS_TO_ADD_3_MICROBES_TO,
        SELECTED_CARD_TO_ADD_2_MICROBES_TO_INDEX: AVAILABLE_CARDS_TO_ADD_2_MICROBES_TO,
        SELECTED_CARD_TO_REMOVE_2_ANIMALS_FROM_INDEX: AVAILABLE_CARDS_TO_REMOVE_2_ANIMALS_FROM,
        SELECTED_CARD_TO_ADD_2_ANIMALS_TO_INDEX: AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO,
        SELECTED_CARD_TO_ADD_4_ANIMALS_TO_INDEX: AVAILABLE_CARDS_TO_ADD_4_ANIMALS_TO,
        SELECTED_CARD_TO_ADD_2_ANIMALS_TO_2_INDEX: AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO_2,

        SELECTED_SPACE_INDEX: AVAILABLE_SPACES,
        SELECTED_PLAYER: AVAILABLE_PLAYERS,
        SELECTED_CARD_WITH_ACTION_INDEX: PLAYED_CARDS_WITH_ACTIONS,
        SELECTED_STANDARD_PROJECT_INDEX: AVAILABLE_STANDARD_PROJECTS,
        SELECTED_CORPORATION: AVAILABLE_CORPORATIONS,
        # multi binary
        MULTIPLE_SELECTED_CARDS: AVAILABLE_CARDS,
        TWO_SELECTED_CARDS_INDICES: AVAILABLE_CARDS,
        MULTIPLE_SELECTED_RESEARCH_CARDS: AVAILABLE_CARDS,
    }

    action = {}

    for key, space in action_space.spaces.items():
        if isinstance(space, Discrete) or isinstance(space, MultiBinary):
            if key in mask_mapping:
                mask_name = mask_mapping[key]
                mask = obs[mask_name]
                #print(mask_name)
                #print("mask:", mask)
                action[key] = space.sample(mask.astype(np.int8))
                #print("action:", action[key])
                #print()
            else:
                action[key] = space.sample()
        elif isinstance(space, Box):
            action[key] = space.sample()

    return action


if __name__ == '__main__':
    env = CustomEnv()
    #env.action_space[MULTIPLE_SELECTED_CARDS].sample(env.observation_space[AVAILABLE_CARDS])
    obs1, _ = env.reset()
    action1 = create_action_from_observation(env.action_space, obs1)
    #print(action1)
    obs2 = env.step(action1)
    print(obs2)
    #action2 = create_action_from_observation(env.action_space, obs2)
