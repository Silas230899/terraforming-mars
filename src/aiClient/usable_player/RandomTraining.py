from CustomEnvironment2 import CustomEnv, create_action_from_observation

if __name__ == '__main__':
    env = CustomEnv()
    #env.action_space[MULTIPLE_SELECTED_CARDS].sample(env.observation_space[AVAILABLE_CARDS])
    obs1, _ = env.reset()
    action1 = create_action_from_observation(env.action_space, obs1)
    #print(action1)
    obs2 = env.step(action1)
    #print(obs2)
    #action2 = create_action_from_observation(env.action_space, obs2)
