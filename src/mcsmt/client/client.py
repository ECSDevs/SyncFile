from httpx import get as httpget
from json import loads as loadJson
from os import listdir,remove
from .down import downloadFile,checkhex


# get config file
with open("Cconfig.json")as f:
    clientcfg = loadJson(f.read())

# get server client.json
config = loadJson(httpget(clientcfg['requestURL']+'client.json').text)

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
        if checkhex("%s/%s"%(t,sf[i]),config[t][i][1]):
            downloadlist.append([config[t][i][0],t])
            continue
    for clientFile in files:
        if clientFile not in sf:
            removelist.append([clientFile,t])
            continue

# download files
for i in downloadlist:
    downloadFile(clientcfg["requestURL"]+i[0],targetPath=i[1])

# delete files
for i in removelist:
    print("unmatch file found. removing...")
    remove("%s/%s"%(i[1],i[0]))
    print("remove complete.")

# end
print("Suceess updated.") 
