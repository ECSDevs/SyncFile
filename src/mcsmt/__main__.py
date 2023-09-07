if __name__ == "__main__":
    from sys import argv as sysArgv, exit as safe_exit
    from os.path import isfile
    from json import loads as loadJson

    if isfile("Margs.txt"):
        with open("Mconfig.json")as f:
            argv = [""]+f.read().split()
    else:
        argv = sysArgv

    print("MCSMT Runner Version 0.2.13.0. Arguments:", argv[1::])
    if len(argv) > 1:
        if len(argv) < 3:
            print("Error: No instances have been specified. You specified a subcontracting.")
            safe_exit()
        if not isfile(f'{argv[1]}\\{argv[2]}.py'):
            print("Error: The specified instance does not exist.")
            safe_exit()
        exec(f"from .{argv[1]}.{argv[2]} import do_job")
        argvdic = loadJson(argv[3])
        try:
            do_job(**argvdic)
        except KeyboardInterrupt:
            safe_exit()
