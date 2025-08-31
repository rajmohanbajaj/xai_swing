import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd

class TradingEnv(gym.Env):
    """
    Discrete actions: 0=SELL/short (-1), 1=HOLD (0), 2=BUY/long (+1)
    State: flattened window of features + current position
    Reward: position * daily_return - trading_costs (on position changes)
    """
    metadata = {"render_modes": []}

    def __init__(self, price_df: pd.DataFrame, features: list, window: int = 20,
                 commission_bps: float = 10.0, slippage_bps: float = 3.0, max_position: int = 1):
        super().__init__()
        self.df = price_df.copy()
        self.features = features
        self.window = window
        self.commission = commission_bps / 1e4   # per side
        self.slippage = slippage_bps / 1e4       # per side
        self.max_position = max_position

        self._prices = self.df["close"].values
        self._rets = self.df["close"].pct_change().fillna(0.0).values

        self.obs_size = window * len(features) + 1  # + current position
        self.action_space = spaces.Discrete(3)      # 0,1,2 → -1,0,+1
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(self.obs_size,), dtype=np.float32)

        self.reset(seed=None)

    def _get_obs(self):
        frame = self.df[self.features].iloc[self.t - self.window:self.t].values.reshape(-1)
        obs = np.concatenate([frame, np.array([self.position], dtype=float)]).astype(np.float32)
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.t = self.window
        self.position = 0  # start flat
        self.prev_action = 1
        self.equity = 1.0
        return self._get_obs(), {}

    def step(self, action: int):
        done = False
        # map action {0,1,2} → position {-1,0,+1}
        new_pos = int(action) - 1
        old_pos = self.position

        price = self._prices[self.t]
        price_prev = self._prices[self.t - 1]
        ret = (price / price_prev) - 1.0

        # costs proportional to turnover: abs(new_pos - old_pos) * (commission+slippage)
        turnover = abs(new_pos - old_pos)
        cost = turnover * (self.commission + self.slippage)

        # reward = PnL - costs
        reward = new_pos * ret - cost

        # update state
        self.position = new_pos
        self.equity *= (1.0 + reward)
        self.prev_action = action
        self.t += 1
        if self.t >= len(self._prices) - 1:
            done = True

        obs = self._get_obs()
        info = {"equity": self.equity, "ret": ret, "position": self.position, "cost": cost}
        return obs, reward, done, False, info
