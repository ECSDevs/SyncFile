import requests
import json
import os
import hashlib

# get config file
with open("Cconfig.json")as f:
    clientcfg = json.load(f)

# get server client.json
config = json.loads(requests.get(clientcfg['requestURL']+'client.json').text)

# defines downloader
def downloader(url,path):
    with open(path,'wb')as f:
        f.write(requests.get(url).content)

def selectdownloader(url,path):
    print("downloading",url.split('/')[-1])
    pt = path+'/'+url.split('/')[-1]
    if 'wget.exe' in os.listdir('.'):
        os.system("wget.exe \"%s\" -o \"%s\""%(url,pt))
    else:
        downloader(url,pt)
    print("download success")

# match client and server files
wait_to_download = []
wait_to_delete = []

for sfk in config:
    cfs = os.listdir(sfk)
    sfn = []
    for sf in config[sfk]:
        sfn.append(sf[0].split('/')[-1])
    for sfno in range(len(sfn)):
        if sfn[sfno] not in cfs:
            wait_to_download.append([config[sfk][sfno][0],sfk])
            continue
        with open("%s/%s"%(sfk,sfn[sfno]),'rb')as f:
            if hashlib.sha512(f.read()).hexdigest() != config[sfk][sfno][1]:
                wait_to_download.append([config[sfk][sfno][0],sfk])
                continue
    for cf in cfs:
        if cf not in sfn:
            wait_to_delete.append([cf,sfk])
            continue

# download files
for i in wait_to_download:
    selectdownloader(clientcfg["requestURL"]+i[0],i[1])

# delete files
for i in wait_to_delete:
    os.remove("%s/%s"%(i[1],i[0]))

# end
print("Suceess updated.") 
