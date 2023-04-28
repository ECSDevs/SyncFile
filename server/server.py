import json
import os
import hashlib

# import config file
configf = open("config.json")
config = json.load(configf)
configf.close()

# summon config file for client
cc = {}
for obj in config:
    files = os.listdir(obj[0])
    if obj[2] not in cc:
        cc[obj[2]]=[]
    for file in files:
        if file.split('.')[-1] in obj[1]:
            filename = "%s/%s"%(obj[0],file)
            with open(filename,'rb')as f:
                hash = hashlib.sha512(f.read()).hexdigest()
            cc[obj[2]].append([filename,hash])

# save to file
ccf = open("client.json",'w')
json.dump(cc,ccf)