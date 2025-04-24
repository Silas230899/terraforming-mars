from CustomEnvironment2 import CustomEnv, create_action_from_observation

if __name__ == '__main__':
    env = CustomEnv()
    #env.action_space[MULTIPLE_SELECTED_CARDS].sample(env.observation_space[AVAILABLE_CARDS])
    obs1, _ = env.reset()
    action1 = create_action_from_observation(env.action_space, obs1)
    #print(action1)
    obs2, reward, done, _, _ = env.step(action1)
    action2 = create_action_from_observation(env.action_space, obs2)
    obs3, _, _, _, _ = env.step(action2)
    #print(obs2)
    #action2 = create_action_from_observation(env.action_space, obs2)

    done = False
    while not done:
        action3 = create_action_from_observation(env.action_space, obs3)
        obs3, reward, done, _, _ = env.step(action3)
