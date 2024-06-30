# Copyright (C) 2024 originalFactor
# 
# This file is part of MCSMT.
# 
# MCSMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# MCSMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with MCSMT.  If not, see <https://www.gnu.org/licenses/>.

from json import loads as load_json
from os import listdir, remove, mkdir
from .down import downloader, check_hex
from random import randint
from threading import Thread
from time import sleep
from os.path import isfile, exists, isdir

# get config file
def get_client_config(client_config_file_path="./Cconfig.json", enc="UTF-8"):
    try:
        with open(client_config_file_path, encoding=enc) as f:
            client_config = load_json(f.read())
    except FileNotFoundError: 
        raise Exception("config file not found")
    return client_config


# init host
def get_ip(client_config): 
    ip = client_config.get("ip", "")
    ips = client_config.get("ips", [])
    if not ip:
        if ips:
            ip = ips[randint(0, len(ip) - 1)]
    return ip


# check client config file
def check_client_config(client_config):
    if not client_config.get("requestURL"):
        raise Exception("No server URL")
    if not (("https://" in client_config["requestURL"]) or ("http://" in client_config["requestURL"])):
        client_config["requestURL"] = "http://" + client_config["requestURL"]
    if client_config["requestURL"][-1] != '/':
        client_config["requestURL"] += '/'
    return client_config


# get server client.json
def get_online_config(client_config, ip):
    downloader(client_config["requestURL"] + client_config.get("indexPath", 'index.json'), ip=ip, prefer_ip_type=client_config.get("preferIPType", ""), dns=client_config.get("dns", "223.5.5.5"),use_dns=client_config.get("useDNS", False))
    with open(client_config.get("indexPath", 'client.json')) as f:
        config = load_json(f.read())
    return config


# match client and server files
def check_local_files(config,client_config):
    download_list = []
    remove_list = []
    for t in config:
        # add automatic creation of folders
        if not (exists(t) and isdir(t)): mkdir(t)
        files = listdir(t)
        sf = [_[0].split('/')[-1] for _ in config[t]]
        for i in range(len(sf)):
            if sf[i] not in files:
                download_list.append([config[t][i][0], t, config[t][i][1]])
                continue
            # add a condition to keep the config works.
            if not check_hex("%s/%s" % (t, sf[i]), config[t][i][1]) and eval(client_config.get("deleteUnMatched","True")):
                remove_list.append([sf[i], t])
                download_list.append([config[t][i][0], t, config[t][i][1]])
        if eval(client_config.get("deleteFileNotFoundInServer","True")):
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
        type=FileType(),
        help="the path of config file, by default it's `Cconfig.json`."
    )
    parser.add_argument(
        "-e", "--encoding",
        default="utf-8",
        type=str,
        help="the encoding of the config file."
    )
    args = parser.parse_args()
    
    client_config = get_client_config(args.config, args.encoding)
    ip = get_ip(client_config)
    client_config = check_client_config(client_config)
    online_config = get_online_config(client_config, ip)
    download_list, remove_list = check_local_files(online_config,client_config)
    process(remove_list, download_list, client_config, ip)
