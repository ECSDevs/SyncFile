import requests
import json
import os
import hashlib
import down

# get config file
with open("Cconfig.json")as f:
    clientcfg = json.load(f)

# get server client.json
config = json.loads(requests.get(clientcfg['requestURL']+'client.json').text)

# match client and server files
wait_to_download = []
wait_to_delete = []

for targetDir in config:
    files = os.listdir(targetDir)
    serverFiles = []
    for serverFile in config[targetDir]:
        serverFiles.append(serverFile[0].split('/')[-1])
    for serverFilesNo in range(len(serverFiles)):
        if serverFiles[serverFilesNo] not in files:
            wait_to_download.append([config[targetDir][serverFilesNo][0],targetDir])
            continue
        with open("%s/%s"%(targetDir,serverFiles[serverFilesNo]),'rb')as f:
            if hashlib.sha512(f.read()).hexdigest() != config[targetDir][serverFilesNo][1]:
                wait_to_download.append([config[targetDir][serverFilesNo][0],targetDir])
                continue
    for clientFile in files:
        if clientFile not in serverFiles:
            wait_to_delete.append([clientFile,targetDir])
            continue

# download files
for i in wait_to_download:
    down.downloadFile(clientcfg["requestURL"]+i[0],targetPath=i[1])

# delete files
for i in wait_to_delete:
    print("unmatch file found. removing...")
    os.remove("%s/%s"%(i[1],i[0]))
    print("remove complete.")

# end
print("Suceess updated.") 
