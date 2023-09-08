if __name__ == "__main__":
    from sys import argv as sysArgv, exit as safe_exit
    from os.path import isfile, isdir, dirname, abspath
    from os import listdir
    from json import loads as loadJson

    if isfile("Margs.txt"):
        with open("Mconfig.json")as f:
            argv = [""]+f.read().split()
    else:
        argv = sysArgv

    def safeListGet(l:list,i:int,d=None):
        try:
            e = l[i]
        except IndexError:
            e = d
        return e

    if not len(argv) > 1:
        print("No arguments found. exiting...")
        safe_exit()
    if len(argv) < 3 or safeListGet(argv,2,"{}")[0]=='{':
        for i in listdir(dirname(abspath(__file__))):
            if isdir(dirname(abspath(__file__))+"/"+i) \
                and \
                isfile(f'{dirname(abspath(__file__))}/{i}/{argv[1]}.py'):
                argv.insert(1, i)
    elif not isfile(f'{dirname(abspath(__file__))}/{argv[1]}/{argv[2]}.py'):
        print("Error: The specified instance does not exist.")
        safe_exit()
    
    print("MCSMT Runner Version 0.2.13.0. Arguments:", argv[1::])
    exec(f"from .{argv[1]}.{argv[2]} import do_job")
    argvdic = loadJson(argv[3])
    try:
        do_job(**argvdic)
    except KeyboardInterrupt:
        safe_exit()
