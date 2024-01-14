from json import load, dump
from os.path import exists

def do_job():
    if exists("config.json"):
        with open("config.json")as f:
            config=load(f)
    else:
        config=[]

    while True:
        try:
            conf = {
                "resourcePath":input("resourcePath:"),
                "fileTypes":[],
                "targetPath":input("outputPath:")
                }
            while True:
                try:
                    conf["fileTypes"].append(input("fileType: "))
                except KeyboardInterrupt:
                    break
            config.append(conf)
        except KeyboardInterrupt:
            break

    with open("config.json",'w')as f:
        dump(config,f)

if __name__ == "__main__":
    from sys import argv
    argv = argv[1::]
    kwargv  = {}
    for a in argv:
        if ":" in a:
            x = a.split(":")
            kwargv[x[0]]=':'.join(x[1::])
            argv.remove(a)
    do_job(*argv, **kwargv)