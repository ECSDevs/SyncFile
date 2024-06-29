print(
f'''
Elemental File Sync v0.3.1 FIXED
Easy transport from everywhere.

You shouldn't use this command.
Use `<python> -m filesync.<someModule> [someArgument]` instead.
There's the module list:
    - client
        Runs the client mode of EFS to clone files from server. See GitHub Wiki for more information.
        This command will delete anything not in server index. So NEVER run it by root, and use it carefully.
    - server
        Runs the server mode of EFS to generate index file. See GitHub Wiki for more information.
'''
)