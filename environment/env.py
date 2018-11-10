import gym
from simulator import Simulator as sim
from coinbase_connector.coinbase_orderbook import CoinbaseOrderBook
from bitfinex_connector.bitfinex_orderbook import BitfinexOrderBook
from configurations.configs import TIMEZONE

import pandas as pd
import numpy as np
from datetime import datetime as dt


DEFAULT_ACTION_SET = (
    (1, 0, 0, 0, 0),  # 0. Buy
    (0, 1, 0, 0, 0),  # 1. Close-buy
    (0, 0, 1, 0, 0),  # 2. Short
    (0, 0, 0, 1, 0),  # 3. Close-short
    (0, 0, 0, 0, 1),  # 4. Do nothing
)


class Env(gym.Env):

    def __init__(self, query, lags=5, train=True):
        self.query = query
        self.train = train
        self.lags = lags
        self.sim = sim()
        self.data = self.sim.get_env_data(query=self.query, lags=self.lags)
        self.n_features = self.data.shape[1]
        self.action_space = gym.spaces.Discrete(n=DEFAULT_ACTION_SET)
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=self.data.shape, dtype=np.float32)
        self.shape = (self.lags, self.n_features)

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the environment

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        return

    def reset(self):
        """Resets the state of the environment and returns an initial observation.

        Returns: observation (object): the initial observation of the
            space.
        """
        return

    def render(self, mode='human'):
        """Renders the environment.

        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:

        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).

        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.

        Args:
            mode (str): the mode to render with
            close (bool): close all open renderings

        Example:

        class MyEnv(Env):
            metadata = {'render.modes': ['human', 'rgb_array']}

            def render(self, mode='human'):
                if mode == 'rgb_array':
                    return np.array(...) # return RGB frame suitable for video
                elif mode is 'human':
                    ... # pop up a window and render
                else:
                    super(MyEnv, self).render(mode=mode) # just raise an exception
        """
        return None

    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        return

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        self.np_random, seed = gym.utils.np_random(seed)
        return [seed]
