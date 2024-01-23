from sys import argv as sysArgv, exit as safe_exit
from os.path import isfile
from json import loads as loadJson
from . import *
from .webApiRunner import do_job as webApi
from .utils import safeListGet
from threading import Thread
from time import sleep
from .info import mcsmt_modules

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

    argv = sysArgv
    if isfile("Margs.txt"):
        with open("Mconfig.json") as f:
            argv += f.read().split()

    
    print("Starting HTTP Service...")
    httpService = Thread(target=webApi,daemon=True)
    httpService.start()
    print("HTTP Service Started.")
    
    if not len(argv) > 1:
        try:
            print("HTTP Service Only mode is turned on. Press Ctrl-C to stop.")
            while True:
                if not httpService.is_alive():
                    break
                sleep(0.1)
        except KeyboardInterrupt:
            pass
        print("HTTP Service Stopped.")
        safe_exit()

    if len(argv) < 3 or safeListGet(argv, 2, "{}")[0] == '{':
        for i in mcsmt_modules:
            if argv[1] in mcsmt_modules[i]:
                argv.insert(1, i)
                break
        else:
            argv.insert(1,'')
    if argv[1] not in mcsmt_modules or argv[2] not in mcsmt_modules[argv[1]]:
        print("Error: The specified instance does not exist.")
        safe_exit()

    argvdic = loadJson(safeListGet(argv,3,'{}'))
    
    print("Running with arguments:", argv[1::])
    try:
        exec(f"{argv[1]}.{argv[2]}.do_job(**argvdic)")
    except KeyboardInterrupt:
        safe_exit()
