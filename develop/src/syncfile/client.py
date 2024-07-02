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
from random import randint
from threading import Thread
from time import sleep
from os.path import isfile, exists, isdir, split
from typing import List, Dict, Union
from pydantic import BaseModel, field_validator


# classes

# config model
class ClientConfig(BaseModel):
    host : str = 'http://127.0.0.1:8000/'
    indexPath : str = 'index.json'
    localIndex : str = 'dumped_index.json'
    ip : Union[str, List[str], None] = None
    preferV6 : bool = False
    dns : str = '223.5.5.5'
    doh : bool = False
    update : bool = True
    removeNotfound : bool = True
    workers : int = 5

    @field_validator('host')
    @classmethod
    def correct(cls, v):
        pass


# init host
def get_ip(client_config:Dict[str,Union[str,int,bool,List[str]]])->str: 
    ip:str = client_config.get("ip", "")
    ips:List[str] = client_config.get("ips", [])
    if not ip:
        if ips:
            ip:str = ips[randint(0, len(ip) - 1)]
    return ip


# check client config file
def check_client_config(client_config:Dict[str,Union[str,int,bool,List[str]]])->Dict[str,Union[str,int,bool,List[str]]]:
    if not client_config.get("requestURL"):
        raise Exception("No server URL")
    if not (("https://" in client_config["requestURL"]) or ("http://" in client_config["requestURL"])):
        client_config["requestURL"] = "http://" + client_config["requestURL"]
    if client_config["requestURL"][-1] != '/':
        client_config["requestURL"] += '/'
    return client_config


# get server client.json
def get_online_config(client_config:Dict[str,Union[str,int,bool,List[str]]], ip:str)->Dict[str,Dict[str,str]]:
    downloader(
        download_url=client_config["requestURL"] + client_config.get("indexPath", 'index.json'), 
        ip=ip, 
        prefer_ip_type=client_config.get("preferIPType", ""), 
        dns=client_config.get("dns", "223.5.5.5"),
        use_dns=client_config.get("useDNS", False),
        save_as=client_config.get("indexSaveAs", "dumped_index.json")
    )
    with open(client_config.get("indexSaveAs", 'dumped_index.json')) as f:
        config:Dict[str,Dict[str,str]] = load_json_file(f)
    return config


# match client and server files
def check_local_files(config:Dict[str,Dict[str,str]],client_config:Dict[str,Union[str,int,bool,List[str]]]):
    download_list = []
    remove_list = []
    for t in config:
        # add automatic creation of folders
        if not (exists(t) and isdir(t)): mkdir(t)
        files = listdir(t)
        for filepath in config[t].keys():
            if split(filepath)[1] not in files:
                download_list.append([filepath, t, config[t][filepath]])
                continue
            # add a condition to keep the config works.
            if not check_hex("%s/%s" % (t, sf[i]), config[t][i][1]) and client_config.get("deleteUnMatched",True):
                remove_list.append([sf[i], t])
                download_list.append([config[t][i][0], t, config[t][i][1]])
        if eval(client_config.get("deleteFileNotFoundInServer",True)):
            for clientFile in files:
                # fixed unexpected deletion of folders
                if isfile(f'{t}/{clientFile}') and (clientFile not in sf):
                    remove_list.append([clientFile, t])
    return download_list, remove_list


# Processing the list after comparison
def process(remove_list, download_list, client_config, ip):
    # removed the condition of `deleteUnMatched`
    for i in remove_list:
        remove("%s/%s" % (i[1], i[0]))
    workers = client_config.get("downloadWorkers", 1)
    workerlist = []
    while len(download_list) or len(workerlist):
        for i in download_list:
            if len(workerlist) < workers:
                workerlist.append(
                    Thread(
                        target=downloader, 
                        args=(
                            client_config["requestURL"] + i[0], 
                            i[1], ip, i[2], 
                            client_config.get("preferIPType", ""),
                            client_config.get("dns", "223.5.5.5"), 
                            client_config.get("useDNS", False)
                        )
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
    
    client_config = load_json_file(args.config)
    ip = get_ip(client_config)
    client_config = check_client_config(client_config)
    online_config = get_online_config(client_config, ip)
    download_list, remove_list = check_local_files(online_config,client_config)
    process(remove_list, download_list, client_config, ip)
