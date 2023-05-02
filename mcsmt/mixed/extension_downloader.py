print("downloading extension wget")
from down import downloadFile
from os import rename
downloadFile("https://ghproxy.com/https://github.com/PsBash-Team/MCSMT/releases/download/exts/wget_ext.exe")
rename("wget_ext.exe","wget.exe")