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
import gym.spaces as spaces
import numpy as np
import pysc2.env.sc2_env as sc2_env

class SC2Env(gym.Env):

    def __init__(self):
        steps = 250
        step_mul = 8
        self.env = sc2_env.SC2Env(
            map_name="MoveToBeacon",
            step_mul=step_mul,
            game_steps_per_episode=steps * step_mul // 2,
            agent_interface_format=sc2_env.AgentInterfaceFormat(
                feature_dimensions=sc2_env.Dimensions(
                    screen=64, minimap=64)))
        self.action_space = self._action_space()
        self.observation_space = self._observation_space()

    def _action_space(self):
        return spaces.Discrete(4)

    def _observation_space(self):
        return spaces.Box(low=0, high=64, shape=(64, 64), dtype=np.float32)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass
