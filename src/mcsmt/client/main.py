from json import loads as load_json
from os import listdir, remove
from ..mixed.down import downloader, check_hex
from random import randint
from threading import Thread
from time import sleep

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
    downloader(client_config["requestURL"] + client_config.get("indexPath", 'client.json'), ip=ip, prefer_ip_type=client_config.get("preferIPType", ""), dns=client_config.get("dns", "223.5.5.5"),use_dns=client_config.get("useDNS", False))
    with open(client_config.get("indexPath", 'client.json')) as f:
        config = load_json(f.read())
    return config


# match client and server files
def check_local_files(config,client_config):
    download_list = []
    remove_list = []
    for t in config:
        files = listdir(t)
        sf = [_[0].split('/')[-1] for _ in config[t]]
        for i in range(len(sf)):
            if sf[i] not in files:
                download_list.append([config[t][i][0], t, config[t][i][1]])
                continue
            if not check_hex("%s/%s" % (t, sf[i]), config[t][i][1]):
                remove_list.append([sf[i], t])
                download_list.append([config[t][i][0], t, config[t][i][1]])
                continue
        if eval(client_config.get("deleteFileNotFoundInServer","True")):
            for clientFile in files:
                if clientFile not in sf:
                    remove_list.append([clientFile, t])
                    continue
    return download_list, remove_list


# Processing the list after comparison
def process(remove_list, download_list, client_config, ip):
    if eval(client_config.get("deleteUnMatched","True")):
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
def do_job(client_config_file_path="./Cconfig.json", client_config_encoding="UTF-8"):
    client_config = get_client_config(client_config_file_path, client_config_encoding)
    ip = get_ip(client_config)
    client_config = check_client_config(client_config)
    online_config = get_online_config(client_config, ip)
    download_list, remove_list = check_local_files(online_config,client_config)
    process(remove_list, download_list, client_config, ip)
