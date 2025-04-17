from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from CustomEnvironment import CustomEnv
from HybridActionWrapper import HybridActionWrapper
from ai_player.CustomModel import HybridActorCriticPolicy, CustomFeatureExtractor

if __name__ == '__main__':
    env1 = CustomEnv()
    wrapped_env = HybridActionWrapper(env1)
    vec_env = DummyVecEnv([lambda: wrapped_env])

    #current_observation = env.reset()
    # while True:
    #     # theoretically calc action from current_observation
    #     #env1.current_turn = 5
    #     #env1.last_observation = current_observation
    #     sample = env.action_space.sample()
    #     new_obs, rewards, dones, infos = env.step([sample])
    #     current_observation = new_obs
    #     if dones[0]: break


    #env = FlattenObservation(env)

    #model2 = PPO("MultiInputPolicy", env, verbose=1, n_steps=32, batch_size=8)
    #model2.learn(total_timesteps=512, progress_bar=True, log_interval=1)

    #env2 = CustomEnv()
    #wrapped_env2 = HybridActionWrapper(env2)
    #env3 = DummyVecEnv([lambda: wrapped_env2])
    #policy_model2 = PPO("MultiInputPolicy", env=wrapped_env2, verbose=1)

    initial_dict_action_space = env1.action_space

    policy_model = PPO(policy=HybridActorCriticPolicy, env=vec_env, verbose=1,policy_kwargs=dict(
        features_extractor_class=CustomFeatureExtractor,
        features_extractor_kwargs=dict(features_dim=64),
        original_action_space=initial_dict_action_space,
    ))
    env1.policy_model = policy_model
    env1.action_wrapper = wrapped_env

    policy_model.learn(total_timesteps=10)
    #current_observation = wrapped_env.reset()
    #policy_model.predict()

