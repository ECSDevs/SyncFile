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

from sys import executable, platform
from os.path import split
from os import environ

PATH = environ.get('PATH', '')

PYTHON = (
    split(executable)[1]
    if split(executable)[0] in (PATH.split(';') if platform=='win32' else PATH.split(':'))
    else executable
)

print(
f'''
Syncfile v0.3.1.2
Easy transport from everywhere.

Usage:
  {PYTHON} -m syncfile.<module> [arg1] [arg2] ...

Modules:
    - client
        Runs the client mode of EFS to clone files from server.
        This command will delete anything not in server index. So NEVER run it by root, and use it carefully.
        Run it with `-h` to see more information.
    - server
        Runs the server mode of EFS to generate index file.
        Run it with `-h` to see more information.
'''
)