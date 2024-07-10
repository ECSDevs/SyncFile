# Copyright (C) 2024 originalFactor
# 
# This file is part of Syncfile.
# 
# Syncfile is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Syncfile is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Syncfile.  If not, see <https://www.gnu.org/licenses/>.

from json import load as load_json_file
from os import listdir, remove, mkdir
from .down import downloader, check_hex
from random import choice
from multiprocessing import Process
from time import sleep
from os.path import exists, isdir, split, isfile
from typing import List, Dict, Union
from pydantic import BaseModel, field_validator


# classes

# config model
class ClientConfig(BaseModel):
    host : str = 'http://127.0.0.1:8000/' # server url
    indexPath : str = 'index.json' # index url
    localIndex : str = 'dumped_index.json' # local index save path
    ip : Union[str, List[str], None] = None # ip or ips
    preferV6 : bool = False # like v6?
    dns : str = '223.5.5.5' # DoH server
    doh : bool = False # force use DoH
    update : bool = True # delete unmatched
    removeNotfound : bool = True # delete not found in index.json
    workers : int = 5 # downloaders running in same time

    @field_validator('host')
    @classmethod
    def correctHost(cls, v:str)->str:
        if not(v.startswith('https://') or v.startswith('http://')):
            v = 'http://' + v
        if not v.endswith('/'):
            v += '/'
        return v
    
    @field_validator('indexPath')
    @classmethod
    def correntIndexPath(cls, v:str)->str:
        if v.startswith('/'): v = v[1:]
        return v
    
    def get_ip(self)->Union[str, None]:
        return (choice(self.ip) if isinstance(self.ip, list) else self.ip) if self.ip else None


# Struct of Index
Index = Dict[str, Dict[str, str]]

# get server client.json
def get_online_config(client_config:ClientConfig)->Index:
    downloader(
        url=client_config.host + client_config.indexPath, 
        ip=client_config.get_ip(), 
        v6=client_config.preferV6, 
        dns=client_config.dns,
        use_dns=client_config.doh,
        output=client_config.localIndex
    )
    with open(client_config.localIndex) as f:
        config = load_json_file(f)
    return config



# match client and server files
def check_local_files(config:Index,client_config:ClientConfig):
    download_list = []
    remove_list = []
    for targetDir, srvfiles in config.items():
        # add automatic creation of folders
        if not (exists(targetDir) and isdir(targetDir)): mkdir(targetDir)
        localfiles = listdir(targetDir)
        for filepath, filehash in srvfiles.items():
            filename = split(filepath)[1]
            localPath = f'{targetDir}/{filename}'
            if filename not in localfiles:
                download_list.append([filepath, localPath, filehash])
                continue
            # add a condition to keep the config works.
            if not check_hex(localPath, filehash) and client_config.update:
                remove_list.append(localPath)
                download_list.append([filepath, localPath, filehash])
            localfiles.remove(filename)
        if client_config.removeNotfound:
            remove_list += list([f'{targetDir}/{_}' for _ in localfiles if isfile(f'{targetDir}/{_}')])
    return download_list, remove_list


# Processing the list after comparison
def process(remove_list:List[str], download_list:List[List[str]], config:ClientConfig):
    # removed the condition of `deleteUnMatched`
    for i in remove_list:
        remove(i)
    workerlist = []
    while len(download_list) or len(workerlist):
        for i in download_list:
            if len(workerlist) < config.workers:
                workerlist.append(
                    Process(
                        target=downloader, 
                        kwargs={
                            'url': config.host + i[0], 
                            'output': i[1], 
                            'ip': config.get_ip(), 
                            'sha512hex': i[2], 
                            'v6': config.preferV6,
                            'dns': config.dns, 
                            'use_dns': config.doh
                        }
                    )
                )
                workerlist[-1].start()
                download_list.remove(i)
        for i in workerlist:
            if not i.is_alive():
                workerlist.remove(i)
        sleep(0.1)

# work
if __name__=="__main__":
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(
        prog="EFS Client Mode",
        description="Like Git but without Version Control.",
        usage="Pull something from server."
    )
    parser.add_argument(
        "-c", "--config",
        default="Cconfig.json",
        type=FileType('r'),
        help="the path of config file, by default it's `Cconfig.json`."
    )
    args = parser.parse_args()
    
    client_config = ClientConfig(**(load_json_file(args.config)))
    online_config = get_online_config(client_config)
    download_list, remove_list = check_local_files(online_config,client_config)
    process(remove_list, download_list, client_config)
