from .down import downloader
from os import rename
def do_job():
    downloader("https://ghproxy.com/https://github.com/PsBash-Team/MCSMT/releases/download/exts/wget_ext.exe")
    rename("wget_ext.exe","wget.exe")