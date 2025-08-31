import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from .env import TradingEnv

def make_env(df, features, cfg):
    return lambda: TradingEnv(df, features, window=cfg.window,
                              commission_bps=cfg.commission_bps,
                              slippage_bps=cfg.slippage_bps,
                              max_position=cfg.max_position)

def train_agent(df, features, cfg):
    env = make_vec_env(make_env(df, features, cfg), n_envs=1)
    model = PPO("MlpPolicy", env, verbose=0, seed=cfg.seed)
    model.learn(total_timesteps=cfg.total_timesteps, progress_bar=True)
    os.makedirs(os.path.dirname(cfg.model_path), exist_ok=True)
    model.save(cfg.model_path)
    return cfg.model_path

def load_agent(path):
    return PPO.load(path)
