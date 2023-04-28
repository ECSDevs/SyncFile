import requests, os

# file downloader
def downloadFile(dlUrl,targetPath="."):
    print("start to download",dlUrl.split('/')[-1])
    chooseChannel(dlUrl,targetPath+'/'+dlUrl.split('/')[-1])
    print("downloaded")

# download channel chooser
def chooseChannel(dlUrl,targetPath):
    if os.path.isfile('wget_ext.exe'):
        print('You have WGET extension! using wget to download.')
        stat = os.system('wget \"%s\" -o \"%s\"'%(dlUrl,targetPath))
        if stat:
            print("something went wrong. file may lose. you can try again.")
    else:
        print("oh no! you didnt download wget extension! using traditional download method. file may broken.")
        downloader(dlUrl,targetPath)

# self-build downloader
def downloader(dlUrl,targetPath):
    with open(targetPath,'wb')as f:
        f.write(requests.get(dlUrl).content)