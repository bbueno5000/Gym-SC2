# Copyright 2018 Benjamin Bueno (bbueno5000)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gym
from gym import spaces
import logging
import numpy as np
from pysc2.env import sc2_env
from pysc2.env.environment import StepType
from pysc2.lib import actions
from pysc2.lib import features

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_NO_OP = actions.FUNCTIONS.no_op.id
_NOT_QUEUED = [0]
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_RELATIVE_SCALE = features.SCREEN_FEATURES.player_relative.scale
_SELECT_ALL = [0]
_SELECT_ARMY = actions.FUNCTIONS.select_army.id

class SC2Env(gym.Env):

    metadata = {'render.modes': [None, 'human']}

    def __init__(self, **kwargs) -> None:
        self._action_space = None
        self._episode = 0
        self._episode_reward = 0
        self._num_step = 0
        self._observation_space = None
        self._total_reward = 0
        self._kwargs = kwargs
        self._kwargs['map_name'] = 'MoveToBeacon'
        self._kwargs['agent_interface_format'] = \
        sc2_env.AgentInterfaceFormat(
            feature_dimensions=sc2_env.Dimensions(
                screen=64, minimap=64))
        self._env = sc2_env.SC2Env(**self._kwargs)

    def _extract_observation(self, obs):
        obs = obs.observation.feature_screen[_PLAYER_RELATIVE]
        obs = obs.reshape(self.observation_space.shape)
        return obs

    def _get_action_space(self):
        # screen_shape = self.observation_spec["screen"][1:]
        return spaces.Discrete(64 * 64 - 1)

    def _get_observation_space(self):
        # screen_shape = (1, ) + self.observation_spec["screen"][1:]
        return spaces.Box(0, _PLAYER_RELATIVE_SCALE, (1, 64, 64), np.float32)

    def _post_reset(self):
        obs, _, _, _ = self._safe_step([_SELECT_ARMY, _SELECT_ALL])
        return self._extract_observation(obs)

    def _safe_step(self, action):
        self._num_step += 1
        if action[0] not in self.available_actions:
            logger.warning("Attempted unavailable action: %s", action)
            action = [actions.FUNCTIONS.no_op.id]
        try:
            obs = self._env.step([actions.FunctionCall(action[0], action[1:])])[0]
        except KeyboardInterrupt:
            logger.info("Interrupted. Quitting.")
            return None, 0, True, {}
        except Exception:
            logger.exception("An unexpected error occurred while applying action to environment.")
            return None, 0, True, {}
        self.available_actions = obs.observation['available_actions']
        reward = obs.reward
        self._episode_reward += reward
        self._total_reward += reward
        return obs, reward, obs.step_type == StepType.LAST, {}

    def _translate_action(self, action):
        if action < 0 or action > self.action_space.n:
            return [_NO_OP]
        # screen_shape = self.observation_spec["screen"][1:]
        target = list(np.unravel_index(action, (64, 64)))
        return [_MOVE_SCREEN, _NOT_QUEUED, target]

    @property
    def action_space(self):
        if self._action_space is None:
            self._action_space = self._get_action_space()
        return self._action_space

    @property
    def action_spec(self):
        return self._env.action_spec()

    def close(self):
        if self._episode > 0:
            logger.info("Episode %d ended with reward %d after %d steps.",
                        self._episode, self._episode_reward, self._num_step)
            logger.info("Got %d total reward, with an average reward of %g per episode",
                        self._total_reward, float(self._total_reward) / self._episode)
        if self._env is not None:
            self._env.close()
        super().close()

    @property
    def episode(self):
        return self._episode

    @property
    def episode_reward(self):
        return self._episode_reward

    @property
    def num_step(self):
        return self._num_step

    @property
    def observation_space(self):
        if self._observation_space is None:
            self._observation_space = self._get_observation_space()
        return self._observation_space

    @property
    def observation_spec(self):
        return self._env.observation_spec()

    def reset(self):
        if self._episode > 0:
            logger.info("Episode %d ended with reward %d after %d steps.",
                        self._episode, self._episode_reward, self._num_step)
            logger.info("Got %d total reward so far, with an average reward of %g per episode",
                        self._total_reward, float(self._total_reward) / self._episode)
        self._episode += 1
        self._num_step = 0
        self._episode_reward = 0
        logger.info("Episode %d starting...", self._episode)
        obs = self._env.reset()[0]
        self.available_actions = obs.observation['available_actions']
        return self._post_reset()

    def save_replay(self, replay_dir):
        self._env.save_replay(replay_dir)

    @property
    def settings(self):
        return self._kwargs

    def step(self, action):
        action = self._translate_action(action)
        obs, reward, done, info = self._safe_step(action)
        if obs is None:
            return None, 0, True, {}
        obs = self._extract_observation(obs)
        return obs, reward, done, info

    @property
    def total_reward(self):
        return self._total_reward
