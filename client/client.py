from requests import get as webget
from json import loads as loadJson
from os import listdir,remove
from hashlib import sha512
from down import downloadFile


# get config file
with open("Cconfig.json")as f:
    clientcfg = loadJson(f.read())

# get server client.json
config = loadJson(webget(clientcfg['requestURL']+'client.json').text)

# match client and server files
wait_to_download = []
wait_to_delete = []

for targetDir in config:
    files = listdir(targetDir)
    serverFiles = []
    for serverFile in config[targetDir]:
        serverFiles.append(serverFile[0].split('/')[-1])
    for serverFilesNo in range(len(serverFiles)):
        if serverFiles[serverFilesNo] not in files:
            wait_to_download.append([config[targetDir][serverFilesNo][0],targetDir])
            continue
        with open("%s/%s"%(targetDir,serverFiles[serverFilesNo]),'rb')as f:
            if sha512(f.read()).hexdigest() != config[targetDir][serverFilesNo][1]:
                wait_to_download.append([config[targetDir][serverFilesNo][0],targetDir])
                continue
    for clientFile in files:
        if clientFile not in serverFiles:
            wait_to_delete.append([clientFile,targetDir])
            continue

# download files
for i in wait_to_download:
    downloadFile(clientcfg["requestURL"]+i[0],targetPath=i[1])

# delete files
for i in wait_to_delete:
    print("unmatch file found. removing...")
    remove("%s/%s"%(i[1],i[0]))
    print("remove complete.")

# end
print("Suceess updated.") 
