from httpx import get as webget
from os import path, system
from hashlib import sha512
from random import choice
from dns.message import make_query
from dns.query import https
from logging import getLogger
logger = getLogger(__name__)

# DNS over HTTPS
def doh(name,type='A',server="223.5.5.5"):
    response = [_.to_text().split() for _ in https(make_query(name,type),server).answer]
    targets = []
    for res in response:
        for i in range(len(res)):
            if res[i]==type:
                targets.append(res[i+1].split('/')[0])
    return targets

# check file's sha512 code
def check_hex(file_path, sha512hex):
    with open(file_path, 'rb') as f:
        return sha512(f.read()).hexdigest() == sha512hex

# file downloader
def downloader(download_url, target_path=".", ip="", sha512hex='', prefer_ip_type='', dns='223.5.5.5', use_dns=False):
    logger.info(f"Start downloading {download_url.split('/')[-1]}")
    choose_channel(download_url, target_path + '/' + download_url.split('/')[-1], ip, sha512hex, prefer_ip_type, dns, use_dns)
    logger.info("Download completed")

# download channel chooser
def choose_channel(download_url, target_path, ip, sha512hex, prefer_ip_type, dns, use_dns):
    download_stat = 000
    if path.isfile('wget.exe'):
        logger.info('Okay! You have WGET to accelerate expansion! Downloading using wget!')
        stat = wget_downloader(download_url, target_path, ip, prefer_ip_type, dns, use_dns)
        if stat:
            logger.warning("There is a problem. The file may be lost. Attempting to download using traditional methods.")
            download_stat = 000
        else:
            download_stat = 200
    else:
        logger.info("Oh no! You didnt download the wget extension! Using traditional download methods. The file may be damaged.")
    if download_stat != 200:
        download_stat = builtin_downloader(download_url, target_path, ip, prefer_ip_type, dns, use_dns)
    if sha512hex:
        if check_hex(target_path, sha512hex):
            logger.error("SHA512 does not match. The file may be damaged.")
            download_stat = 000
        else:
            logger.debug("SHA512 matched.")
            download_stat = 200
    if download_stat != 200:
        logger.error("Download failed.")
    else:
        logger.debug(f"Download successful. Status code: {download_stat}")

def process_ip(dl_url, ip, preferred_ip_type, dns):
    logger.warning("An unstable test download method is being used: custom IP (or custom DNS resolution method)")
    dom = dl_url.split('//')[1].split('/')[0].split(":")
    if not ip:
        if not preferred_ip_type:
            preferred_ip_type = 'A'
        if not dns:
            dns = "223.6.6.6"
        ips = doh(dom[0], preferred_ip_type, dns)
        if not ips:
            logger.fatal(f'Fatal occurred: specified domain {dom[0]} doesnt point to any {preferred_ip_type} record.')
            raise Exception(f"{__name__} Unable to continue running. The specified domain name {dom[0]} does not point to any {preferred_ip_type} records.")
        ip = choice(ips)
    if ':' in ip:
        ip = f"[{ip}]"
    dl_url = dl_url.split('//' + ':'.join(dom) + '/')
    ip_domain = dom.copy()
    ip_domain[0] = ip
    dl_url = dl_url[0] + '//' + ':'.join(ip_domain) + '/' + dl_url[1]
    logger.warning(f"URL in use: {dl_url} , Headers in use: Host:{dom[0]}")
    return dl_url, dom[0]

def wget_downloader(dl_url, target_path, ip, prefer_ip_type, dns, use_dns):
    if ip or use_dns:
        dl_url, dom = process_ip(dl_url, ip, prefer_ip_type, dns)
        return system(f"wget \"{dl_url}\" --header=\"Host:{dom}\" --no-check-certificate -O \"{target_path}\"")
    elif prefer_ip_type:
        prefer_ip_types = ['A', 'AAAA']
        arg_codes = ['-4', '-6']
        return system(f"wget \"{dl_url}\" {arg_codes[prefer_ip_types.index(prefer_ip_type)]} -O \"{target_path}\"")
    else:
        return system('wget \"%s\" -O \"%s\"' % (dl_url, target_path))

def builtin_downloader(dl_url, target_path, ip, prefer_ip_type, dns, use_dns):
    logger.debug("Attempting to open file.")
    target_path_dir = '/'.join(target_path.split('/')[:-1:])
    try:
        if not path.exists(target_path_dir) or not path.isdir(target_path_dir):
            path.mkdir(target_path_dir)
        with open(target_path, 'wb') as f:
            logger.debug("download started using traditional method.")
            if ip or prefer_ip_type or use_dns:
                dl_url, dom = process_ip(dl_url, ip, prefer_ip_type, dns)
                r = webget(dl_url, headers={"Host": dom}, verify=False)
            else:
                r = webget(dl_url)
            f.write(r.content)
    except Exception as err:
        logger.fatal(f"Unable to Write file. Exception: {err}")
        return 000
    return r.status_code
