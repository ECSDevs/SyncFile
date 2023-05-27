from httpx import get as webget
from os import path as ospath, system as ossystem
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler
from hashlib import sha512
from .ezdns import doh
from random import randint

# init logger
logger = getLogger(__name__)
logger.propagate = False

# init log handler
logHandler = TimedRotatingFileHandler(f"psbyuDownloaderModule_{__name__}.log",when='d')
logHandler.setLevel("INFO")
logger.addHandler(logHandler)

# status message
precompiledStatusMessages = {
    200:"Ok.",
    404:"Not found.",
    502:"Server Crashed."
}

# check file's sha512 code
def checkhex(path,hex):
    with open(path,'rb')as f:
        if sha512(f.read()).hexdigest() == hex:
            return True
        else:
            return False
        

# Status Code System
class Stat:
    def __init__(self,httpStatusCode,msg="",library=precompiledStatusMessages):
        self.statusCode = httpStatusCode
        self.library = library
        if not msg:
            msg = self.getMessageFromLibrary(self.statusCode,self.library)
        self.message = msg
    def get(self):
        return (self.statusCode,self.message)
    def getMessageFromLibrary(self,code,library=precompiledStatusMessages):
        return library.get(code)
    def genMsg(self):
        self.message = self.getMessageFromLibrary(self.statusCode,self.library)
    def set(self,code=0,msg=''):
        if code:
            self.statusCode = code
            if msg:
                self.message = msg
            else:
                self.genMsg()
        else:
            if msg:
                self.message = msg
            else:
                self.genMsg()


# file downloader
def downloadFile(dlUrl,targetPath=".",host="",hexcode='',preferHostType='A',dns='223.5.5.5'):
    logger.info("start to download %s"%dlUrl.split('/')[-1])
    if not host:
        hosts=doh(dlUrl.split('//')[1].split('/')[0],preferHostType,dns)
        host=hosts[randint(0,len(hosts)-1)]
    chooseChannel(dlUrl,targetPath+'/'+dlUrl.split('/')[-1],host)
    logger.info("downloaded")

# download channel chooser

def chooseChannel(dlUrl,targetPath,host='',hexcode=''):
    downloadStat = Stat(0)
    if ospath.isfile('wget.exe'):
        if host:
            logger.info("You targeted a HOST, so you cant use WGET extension. Using traditional download method.")
        else:
            logger.info('You have WGET extension! using wget to download.')
            stat = ossystem('wget \"%s\" -O \"%s\"'%(dlUrl,targetPath))
            if stat:
                logger.warn("something went wrong. file may lose. trying to use traditional download method.")
            else: 
                downloadStat.set(200)
    else: 
        logger.info("oh no! you didnt download wget extension! using traditional download method. file may broken.")
    if downloadStat.statusCode!=200:
        downloadStat.set(code=downloader(dlUrl,targetPath,hexcode))
    if hexcode:
        if checkhex(targetPath,hexcode):
            logger.error("hexcode not match.")
        else:
            logger.debug("hexcode check passed.")
    if downloadStat.statusCode!=200:
        logger.error("download fail.")
    else:
        logger.debug(f"download success. status_code: {downloadStat.get()}")

# self-build downloader
def downloader(dlUrl,targetPath,host=''):
    logger.debug("trying to open file")
    with open(targetPath,'wb')as f:
        logger.debug("download started using traditional method.")
        r = webget(dlUrl,headers={"Host":host})
        try: f.write(webget(dlUrl).content)
        except Exception as err:
            logger.fatal(f"Unable to Write file. Exception: {err}")
            return 1000
    return r.status_code