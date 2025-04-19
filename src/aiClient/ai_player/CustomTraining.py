from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from CustomEnvironment import CustomEnv
from HybridActionWrapper import HybridActionWrapper
from ai_player.CustomModel import HybridActorCriticPolicy, CustomFeatureExtractor

if __name__ == '__main__':
    env1 = CustomEnv()
    wrapped_env = HybridActionWrapper(env1)
    vec_env = DummyVecEnv([lambda: wrapped_env])


    initial_dict_action_space = env1.action_space

    policy_model = PPO(policy=HybridActorCriticPolicy, env=vec_env, verbose=1,policy_kwargs=dict(
        features_extractor_class=CustomFeatureExtractor,
        features_extractor_kwargs=dict(features_dim=64),
        original_action_space=initial_dict_action_space,
    ))
    env1.policy_model = policy_model
    env1.action_wrapper = wrapped_env

    policy_model.learn(total_timesteps=10)

