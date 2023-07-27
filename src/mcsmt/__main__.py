if __name__ == "__main__":
    from sys import argv, exit as safe_exit
    from os.path import isfile

    print("MCSMT Runner Version 0.2.12.0", argv)
    if len(argv) > 1:
        if len(argv) < 3:
            print("Error: No instances have been specified. You specified a subcontracting.")
            safe_exit()
        if '/' in argv[0]:
            isf = '/'.join(argv[0].split('/')[:-1:]) + f'/{argv[1]}/{argv[2]}.py'
        elif '\\' in argv[0]:
            isf = '\\'.join(argv[0].split('\\')[:-1:]) + f'\\{argv[1]}\\{argv[2]}.py'
        print(isf)
        if not isfile(isf):
            print("Error: The specified instance does not exist.")
            safe_exit()
        exec(f"from .{argv[1]}.{argv[2]} import do_job")
        argvdic = {}
        for i in argv[3::]:
            if ':' in i:
                tmp = i.split(':')
                argvdic[tmp[0]] = tmp[1]
        try:
            do_job(**argvdic)
        except KeyboardInterrupt:
            safe_exit()
