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
        if ':' in obj["resourcePath"]:
            cc[obj["targetPath"]].append(obj["resourcePath"])
        fx = walk(obj["resourcePath"])
        for root, _, files in fx:
            root = root.replace('\\','/') if root!='.' else ''
            sr = '/'.join(root.split(obj["resourcePath"])[-1].split('/')[-1:0:-1])
            rp = ('/'+sr)if sr else ''
            if obj["targetPath"]+rp not in cc:
                cc[obj["targetPath"]+rp] = []
            for file in files:
                if (file.split('.')[-1] in obj["fileTypes"]) or ('' in obj["fileTypes"]):
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

if __name__ == "__main__":
    from sys import argv
    argv = argv[1::]
    kwargv  = {}
    for a in argv:
        if ":" in a:
            x = a.split(":")
            kwargv[x[0]]=':'.join(x[1::])
            argv.remove(a)
    do_job(*argv, **kwargv)