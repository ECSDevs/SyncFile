from json import load, dump
from os import walk, listdir
from hashlib import sha512
from ..utils import safeListGet


def do_job(config="config.json",client="client.json"):
    # import config file
    configf = open(config)
    config = load(configf)
    configf.close()

    # summon config file for client
    # New: allow reverse join
    cc = {}
    for obj in config:
        fx = walk(obj[0]) if safeListGet(obj,3) else [(obj[0], [], [_ for _ in listdir(obj[0])])]
        for root, _, files in fx:
            root = root.replace('\\','/') if root!='.' else ''
            sr = '/'.join(root.split(obj[0])[-1].split('/')[-1:0:-1])
            rp = ('/'+sr)if sr else ''
            if obj[2]+rp not in cc:
                cc[obj[2]+rp] = []
            for file in files:
                if (file.split('.')[-1] in obj[1]) or ('' in obj[1]):
                    filename = (root+'/'+file) if root else file
                    with open(filename, 'rb') as f:
                        mhash = sha512(f.read()).hexdigest()
                    cc[obj[2]+rp].append([filename, mhash])

    for obj in cc:
        cc[obj] = set(cc[obj])

    # save to file
    ccf = open(client, 'w')
    dump(cc, ccf)
    ccf.close()
