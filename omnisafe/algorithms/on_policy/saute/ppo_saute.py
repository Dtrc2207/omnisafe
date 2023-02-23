# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
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
# ==============================================================================
"""Implementation of the Saute algorithm."""

from omnisafe.adapter import SauteAdapter
from omnisafe.algorithms import registry
from omnisafe.algorithms.on_policy.base.ppo import PPO
from omnisafe.utils import distributed


@registry.register
class PPOSaute(PPO):
    """The Saute algorithm implemented with PPO.

    References:
        - Title: Saute RL: Almost Surely Safe Reinforcement Learning Using State Augmentation
        - Authors: Aivar Sootla, Alexander I. Cowen-Rivers, Taher Jafferjee,
            Ziyan Wang, David Mguni, Jun Wang, Haitham Bou-Ammar.
        - URL: `Saute RL<https://arxiv.org/abs/2202.06558>`_
    """

    def _init_env(self) -> None:
        self._env = SauteAdapter(self._env_id, self._cfgs.num_envs, self._seed, self._cfgs)
        assert self._cfgs.steps_per_epoch % (distributed.world_size() * self._cfgs.num_envs) == 0, (
            'The number of steps per epoch is not divisible by the number of ' 'environments.'
        )
        self._steps_per_epoch = (
            self._cfgs.steps_per_epoch // distributed.world_size() // self._cfgs.num_envs
        )

    def _init_log(self) -> None:
        super()._init_log()
        self._logger.register_key('Metrics/EpBudget')