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
Elemental File Sync v0.3.1 FIXED
Easy transport from everywhere.

Usage:
  {PYTHON} -m filesync.<module> [arg1] [arg2] ...

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