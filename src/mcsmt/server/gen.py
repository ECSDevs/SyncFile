from json import load,dump
from os import listdir
from hashlib import sha512

def do_job(config_file="config.json"):
    # import config file
    configf = open(config_file)
    config = load(configf)
    configf.close()

    # summon config file for client
    cc = {}
    for obj in config:
        files = listdir(obj[0])
        if obj[2] not in cc:
            cc[obj[2]]=[]
        for file in files:
            if file.split('.')[-1] in obj[1]:
                filename = "%s/%s"%(obj[0],file)
                with open(filename,'rb')as f:
                    hash = sha512(f.read()).hexdigest()
                cc[obj[2]].append([filename,hash])

    # save to file
    ccf = open(config_file,'w')
    dump(cc,ccf)
    ccf.close()