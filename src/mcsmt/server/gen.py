from json import load, dump
from os import walk, listdir
from hashlib import sha512


def do_job(config="config.json",client="index.json"):
    # import config file
    configf = open(config)
    config = load(configf)
    configf.close()

    # summon config file for client
    # New: allow reverse join
    cc = {}
    for obj in config:
        fx = walk(obj[0]) if obj[3] else [(obj[0], [], [_ for _ in listdir(obj[0])])]
        for root, _, files in fx:
            root = root
            if obj[2]+() not in cc:
                cc[obj[2]] = []
            for file in files:
                if file.split('.')[-1] in obj[1]:
                    filename = root.replace('\\','/')+'/'+file if root!='.' else file
                    with open(filename, 'rb') as f:
                        mhash = sha512(f.read()).hexdigest()
                    cc[obj[2]].append([filename, mhash])

    # save to file
    ccf = open(client, 'w')
    dump(cc, ccf)
    ccf.close()
