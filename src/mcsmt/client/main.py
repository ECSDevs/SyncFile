from json import loads as loadJson
from os import listdir,remove
from ..mixed.down import downloadFile,checkhex
from ..mixed.ezdns import doh
from random import randint


# get config file
with open("Cconfig.json")as f:
    clientcfg = loadJson(f.read())

# init host
ip = clientcfg.get("ip","")
ips = clientcfg.get("ips",[])
if not ip:
    if ips:
        ip = ips[randint(0,len(ip)-1)]

# check ccfg file
if not clientcfg.get("requestURL"):
    raise Exception("No server URL")
if not ( ("https://" in clientcfg["requestURL"]) or ("http://" in clientcfg["requestURL"]) ):
    clientcfg["requestURL"] = "http://"+clientcfg["requestURL"]
if clientcfg["requestURL"][-1]!='/':
    clientcfg["requestURL"]+='/'


# get server client.json
downloadFile(clientcfg["requestURL"]+'client.json',ip=ip,preferIPType=clientcfg.get("preferIPType","A"),dns=clientcfg.get("dns","223.5.5.5"),usedns=clientcfg.get("useDNS",False))
with open("client.json")as f:
    config = loadJson(f.read())

# match client and server files
downloadlist = []
removelist = []

for t in config:
    files = listdir(t)
    sf = [_[0].split('/')[-1] for _ in config[t]]
    for i in range(len(sf)):
        if sf[i] not in files:
            downloadlist.append([config[t][i][0],t,config[t][i][1]])
            continue
        if not checkhex("%s/%s"%(t,sf[i]),config[t][i][1]):
            removelist.append([sf[i],t])
            downloadlist.append([config[t][i][0],t,config[t][i][1]])
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
    downloadFile(clientcfg["requestURL"]+i[0],i[1],ip,i[2],clientcfg.get("preferIPType",""),clientcfg.get("dns","223.5.5.5"),clientcfg.get("useDNS",False))


# end
print("Suceess updated.") 
