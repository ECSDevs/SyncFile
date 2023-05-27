from httpx import get as httpget
from json import loads as loadJson
from os import listdir,remove
from ..mixed.down import downloadFile,checkhex
from ..mixed.ezdns import doh
from random import randint


# get config file
with open("Cconfig.json")as f:
    clientcfg = loadJson(f.read())

# init host
host = clientcfg.get("ip")
hosts = clientcfg.get("ips")
if not host:
    if not hosts:
        hosts = doh(clientcfg["requestURL"].split('//')[1].split('/')[0],clientcfg.get("preferDNSRecordType","A"),clientcfg.get("DNS","223.5.5.5"))
    host = hosts[randint(0,len(hosts)-1)]

# get server client.json
config = loadJson(httpget(clientcfg['requestURL']+'client.json',headers={"Host":host}).text)

# match client and server files
downloadlist = []
removelist = []

for t in config:
    files = listdir(t)
    sf = [_[0].split('/')[-1] for _ in config[t]]
    for i in range(len(sf)):
        if sf[i] not in files:
            downloadlist.append([config[t][i][0],t])
            continue
        if not checkhex("%s/%s"%(t,sf[i]),i[1]):
            removelist.append([sf[i],t])
            downloadlist.append([config[t][i][0],t])
            continue
    for clientFile in files:
        if clientFile not in sf:
            removelist.append([clientFile,t])
            continue

# delete files
for i in removelist:
    print("unmatch file found. removing...")
    remove("%s/%s"%(i[1],i[0]))
    print("remove complete.")

# download files
for i in downloadlist:
    downloadFile(clientcfg["requestURL"]+i[0],targetPath=i[1])


# end
print("Suceess updated.") 
