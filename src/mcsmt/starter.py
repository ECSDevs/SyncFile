from sys import argv as sysArgv, exit as safe_exit
from os.path import isfile, abspath
from json import loads as loadJson
from . import *

def main():
    
    try:
        with open("type.tag")as f:
            tpe = f.read()
    except FileNotFoundError:
        tpe = "full"
    print(f"MCSMT Runner Version 0.2.13.2{tpe}. ")
    mixed.down.downloader("http://files.psbyu.net/mcsmtNotifications.rt")
    try:
        with open("mcsmtNotifications.rt", encoding="utf-8")as f:
            print(f.read())
    except FileNotFoundError:
        print("MCSMT在线公告获取失败，请检查您的网络连接。这不会影响您使用该软件，也许是我们的问题。")

    if isfile("Margs.txt"):
        with open("Mconfig.json") as f:
            argv = [""] + f.read().split()
    else:
        argv = sysArgv
    if not len(argv) > 1:
        print("No arguments found. exiting...")
        safe_exit()
    if len(argv) < 3 or utils.safeListGet(argv, 2, "{}")[0] == '{':
        for i in info.mcsmt_modules:
            if argv[1] in info.mcsmt_modules[i]:
                argv.insert(1, i)
                break
        else:
            argv.insert(1,'')
    if argv[1] not in info.mcsmt_modules or argv[2] not in info.mcsmt_modules[argv[1]]:
        print("Error: The specified instance does not exist.")
        safe_exit()

    argvdic = loadJson(utils.safeListGet(argv,3,'{}'))
    
    print("Running with arguments:", argv[1::])
    try:
        exec(f"{argv[1]}.{argv[2]}.do_job(**argvdic)")
    except KeyboardInterrupt:
        safe_exit()
