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
logHandler.setLevel("DEBUG") # always debug before stable release
logger.setLevel("DEBUG") # ditto
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
def downloadFile(dlUrl,targetPath=".",ip="",hexcode='',preferIPType='',dns='223.5.5.5',usedns=False):
    logger.info("start to download %s"%dlUrl.split('/')[-1])
    chooseChannel(dlUrl,targetPath+'/'+dlUrl.split('/')[-1],ip,hexcode,preferIPType,dns,usedns)
    logger.info("downloaded")

# download channel chooser

def chooseChannel(dlUrl,targetPath,ip,hexcode,preferIPType,dns,usedns):
    downloadStat = Stat(000)
    if ospath.isfile('wget.exe'):
        logger.info('You have WGET extension! using wget to download.')
        stat = wget_downloader(dlUrl, ip)
        if stat:
            logger.warn("something went wrong. file may lose. trying to use traditional download method.")
            downloadStat.set(000)
        else: 
            downloadStat.set(200)
    else: 
        logger.info("oh no! you didnt download wget extension! using traditional download method. file may broken.")
    if downloadStat.statusCode!=200:
        downloadStat.set(downloader(dlUrl,targetPath,ip,preferIPType,dns,usedns))
    if hexcode:
        if checkhex(targetPath,hexcode):
            logger.error("hexcode not match.")
            downloadStat.set(000)
        else:
            logger.debug("hexcode check passed.")
            downloadStat.set(200)
    if downloadStat.statusCode!=200:
        logger.error("download fail.")
    else:
        logger.debug(f"download success. status_code: {downloadStat.get()}")

def wget_downloader(dlUrl,targetPath,ip,preferIPType,dns,usedns):
    if ip or usedns:
        logger.warn("An unstable test download method is being used: custom IP (or custom DNS resolution method)")
        dom = dlUrl.split('//')[1].split('/')[0].split(":")
        if not ip:
            if not preferIPType:
                preferIPType = 'A'
            ips = doh(dom[0],preferIPType,dns)
            ip = ips[randint(0,len(ips)-1)]
            if preferIPType == 'AAAA':
                ip = '['+ip+']'
        dlUrl2 = dlUrl.split('//'+':'.join(dom)+'/')
        ipdom = dom.copy() ; ipdom[0]=ip
        stripdom = ':'.join(ipdom)
        logger.warn(f"URL in use: {dlUrl2[0]+'//'+stripdom+'/'+dlUrl2[1]} , Headers in use: Host:{dom[0]}")
        return ossystem(f"wget \"{dlUrl2[0]+'//'+stripdom+'/'+dlUrl2[1]}\" -H \"Host:{dom[0]}\" -O \"{targetPath}\"")
    elif preferIPType:
        preferIPTypes = ['A','AAAA']; argCodes = ['-4','-6']
        return ossystem(f"wget \"{dlUrl}\" {argCodes[preferIPTypes.index(preferIPType)]} -O \"{targetPath}\"")
    else:
        return ossystem('wget \"%s\" -O \"%s\"'%(dlUrl,targetPath))

# self-build downloader
def builtin_downloader(dlUrl,targetPath,ip,preferIPType,dns,usedns):
    logger.debug("trying to open file")
    try:
        with open(targetPath,'wb')as f:
            logger.debug("download started using traditional method.")
            if ip or preferIPType or usedns:
                logger.warn("An unstable test download method is being used: custom IP (or custom DNS resolution method)")
                dom = dlUrl.split('//')[1].split('/')[0].split(":")
                if not ip:
                    if not preferIPType:
                        preferIPType = 'A'
                    ips = doh(dom[0],preferIPType,dns)
                    ip = ips[randint(0,len(ips)-1)]
                    if preferIPType == 'AAAA':
                        ip = '['+ip+']'
                dlUrl2 = dlUrl.split('//'+':'.join(dom)+'/')
                ipdom = dom.copy() ; ipdom[0]=ip
                stripdom = ':'.join(ipdom)
                logger.warn(f"URL in use: {dlUrl2[0]+'//'+stripdom+'/'+dlUrl2[1]} , Headers in use: Host:{dom[0]}")
                r = webget(dlUrl2[0]+'//'+stripdom+'/'+dlUrl2[1],headers={"Host":dom[0]},verify=False)
            else:
                r = webget(dlUrl)
            f.write(r.content)
    except Exception as err:
        logger.fatal(f"Unable to Write file. Exception: {err}")
        return 000
    return r.status_code