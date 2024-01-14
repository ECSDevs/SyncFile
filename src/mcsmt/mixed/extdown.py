from .down import downloader
from os import rename
def do_job():
    downloader("https://ghproxy.com/https://github.com/PsBash-Team/MCSMT/releases/download/exts/wget_ext.exe")
    rename("wget_ext.exe","wget.exe")
    
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