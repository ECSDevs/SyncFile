# Copyright 2024 ECSDevs
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from httpx import get as webget
from os import path, system, mkdir, environ
from sys import platform
from hashlib import sha512
from random import choice
from dns.message import make_query
from dns.query import https
from typing import List, Union, Tuple, Dict
from logging import getLogger
logger = getLogger(__name__)
from enum import Enum

# DNS over HTTPS
def doh(name:str,type:str='A',server:str="223.5.5.5")->List[str]:
    response = [_.to_text().split() for _ in https(make_query(name,type),server).answer]
    targets = []
    for res in response:
        for i in range(len(res)):
            if res[i]==type:
                targets.append(res[i+1].split('/')[0])
    return targets

# check file's sha512 code
def check_hex(file_path:str, sha512hex:str)->bool:
    if not path.exists(file_path): return False
    with open(file_path, 'rb') as f:
        return sha512(f.read()).hexdigest() == sha512hex

# file downloader
def downloader(
        url:str, 
        output:str="./", 
        ip:Union[str,None]=None, 
        sha512hex:Union[str,None]=None, 
        v6:bool=False, 
        dns:str='223.5.5.5', 
        use_dns:bool=False, 
    ):
    global wgetStatus
    filename = (path.split(url)[1] if output[-1]=='/' else path.split(output)[1])
    directory = path.split(output)[0]
    if not directory: directory = '.'
    local_path = f'{directory}/{filename}'
    logger.info(f"Start downloading {local_path}")
    # to prevent download without creating folder
    if not (path.exists(directory) and path.isdir(directory)):
        mkdir(directory)
    # check and create info
    headers = {
        "User-Agent": "GitHub.com/ECSDevs/Syncfile v0.3.1.2 (based on WGET and HTTPX)"
    }
    verify = True
    if ip or v6 or use_dns:
        url, domain  = process_ip(
            url, 
            ip, 
            (AvaliableIPTypes.v6 if v6 else AvaliableIPTypes.v4),
            dns
        )
        headers["Host"] = domain
        verify = False
    # check use wget or built-in:
    if wgetStatus==WgetAvaliableStatus.never_checked: ask_wget_avaliable()
    status_code = (
        wget_downloader
        if wgetStatus!=WgetAvaliableStatus.unavaliable else
        builtin_downloader
    )(url, local_path, headers, verify)
    if status_code!=200: logger.error(f"{local_path} Download status invalid.")
    elif sha512hex and not check_hex(local_path, sha512hex): logger.error(f"{local_path} hash value doesn't match.")
    else: logger.info("Download completed")

class WgetAvaliableStatus(Enum):
    local = 'local'
    sys = 'system'
    unavaliable = 'unavaliable'
    never_checked = None

wgetStatus : WgetAvaliableStatus = WgetAvaliableStatus.never_checked
wget_path : Union[str, None] = None

# Check is wget avaliable? (Prefer using wget)
def ask_wget_avaliable():
    global wgetStatus, wget_path
    logger.info("Checking if the system has WGET support...")
    if path.exists('wget.exe' if platform=='win32' else 'wget'): 
        wgetStatus = WgetAvaliableStatus.local
        wget_path = ('.\wget.exe' if platform=='win32' else './wget')
        return
    path_list = environ['PATH'].split(';' if platform=='win32' else ':')
    for PATH in path_list:
        if path.exists(f'{PATH}/{"wget.exe" if platform=="win32" else "wget"}'):
            wgetStatus =  WgetAvaliableStatus.sys
            return
    wgetStatus = WgetAvaliableStatus.unavaliable

class AvaliableIPTypes(Enum):
    v6 = 'AAAA'
    v4 = 'A'

def process_ip(dl_url:str, ip:str, preferred_ip_type:AvaliableIPTypes, dns:str)->Tuple[str]:
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

def wget_downloader(dl_url:str, target_path:str, headers:Dict[str,str], verify:bool=True, *args)->int:
    global wgetStatus
    logger.info(f"{target_path} download started using wget extension.")
    return (0 
        if system(' '.join([
        ("wget" if wgetStatus==WgetAvaliableStatus.sys else "./wget"),
        f'"{dl_url}"',
        "-O",
        f'"{target_path}"',
        ' '.join([
            f'--header="{key}: {value}"'
            for key, value in headers.items()
        ]),
        ("" if verify else "--no-check-certificate"),
        *args
    ])) else
    200)

def builtin_downloader(dl_url:str, target_path:str, headers:Dict[str,str], verify:bool=True, *args, **kwargs)->int:
    try:
        logger.debug(f"{target_path} download started using traditional method.")
        r = webget(dl_url, headers=headers, verify=verify, *args, **kwargs)
        if r.status_code==200:
            logger.debug(f"Trying to open {target_path} and write response...")
            try:
                with open(target_path, 'wb') as f:
                    f.write(r.content)
            except Exception as err:
                logger.error(f"Unable to write {target_path}. FileSystem Exception: {err}.")
        else:
            logger.error(f"Unable to download {target_path}. HTTP Status Code {r.status_code}.")
    except Exception as err:
        logger.error(f"Unable to download {target_path}. Network Exception: {err}.")
        return 000
    return r.status_code
