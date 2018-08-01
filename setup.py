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

from setuptools import setup

setup(
    install_requires=['absl-py', 'gym', 'numpy', 'pysc2'],
    name='gym_sc2',
    url='https://github.com/bbueno5000/gym-sc2',
    version='0.0.1')
