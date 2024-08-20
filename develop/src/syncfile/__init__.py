# Copyright 2024 ECSDevs
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from logging import basicConfig
from os import environ
basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s : %(message)s",
    **({'filename':environ['LOGGING_FILE']}  if environ.get('LOGGING_FILE') else {})
)

from . import client, down, server, utils

__all__ = [
    'client',
   'down',
   'server',
   'utils'
]