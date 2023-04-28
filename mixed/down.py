from requests import get as webget
from os import path as ospath, system as ossystem

# file downloader
def downloadFile(dlUrl,targetPath="."):
    print("start to download",dlUrl.split('/')[-1])
    chooseChannel(dlUrl,targetPath+'/'+dlUrl.split('/')[-1])
    print("downloaded")

# download channel chooser
def chooseChannel(dlUrl,targetPath):
    if ospath.isfile('wget_ext.exe'):
        print('You have WGET extension! using wget to download.')
        stat = ossystem('wget \"%s\" -o \"%s\"'%(dlUrl,targetPath))
        if stat:
            print("something went wrong. file may lose. you can try again.")
    else:
        print("oh no! you didnt download wget extension! using traditional download method. file may broken.")
        downloader(dlUrl,targetPath)

# self-build downloader
def downloader(dlUrl,targetPath):
    with open(targetPath,'wb')as f:
        f.write(webget(dlUrl).content)