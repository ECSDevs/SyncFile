from httpx import get as webget
from os import path as ospath, system as ossystem
from logging import getLogger

logger = getLogger("net.psbyu.github.lghilb-yu.psbash.mcsmt.client.modules.downloader")

precompiledStatusMessages = {
    200:"Ok.",
    404:"Not found.",
    502:"Server Crashed."
}

class Stat:
    def __init__(self,httpStatusCode,msg="",library=precompiledStatusMessages):
        self.statusCode = httpStatusCode
        self.library = library
        if not msg:
            msg = self.getMessageFromLibrary(self.code,self.library)
        self.message = msg
    def get(self):
        return (self.statusCode,self.message)
    def getMessageFromLibrary(code,library=precompiledStatusMessages):
        return library.get(code)
    def genMsg(self):
        self.message = self.getMessageFromLibrary(self.statusCode,self.library)
    def set(self,code=0,msg=''):
        if not code:
            if msg:
                self.message = msg
            else:
                self.genMsg
                

# file downloader
def downloadFile(dlUrl,targetPath=".",host=""):
    print("start to download",dlUrl.split('/')[-1])
    if not host:
        host = dlUrl.split("//")[1].split("/")[0]
    chooseChannel(dlUrl,targetPath+'/'+dlUrl.split('/')[-1],host)
    print("downloaded")

# download channel chooser
cChannelStat = Stat(0)
def chooseChannel(dlUrl,targetPath,host):
    if ospath.isfile('wget.exe'):
        print('You have WGET extension! using wget to download.')
        stat = ossystem('wget \"%s\" -O \"%s\"'%(dlUrl,targetPath))
        if stat:
            print("something went wrong. file may lose. trying to use traditional download method.")
        else: 
            cChannelStat.statusCode = 
    else: 
        print("oh no! you didnt download wget extension! using traditional download method. file may broken.")
    downloader(dlUrl,targetPath)

# self-build downloader
def downloader(dlUrl,targetPath):
    with open(targetPath,'wb')as f:
        r = webget(dlUrl)
        if r.status_code!=200:

        f.write(webget(dlUrl).content)