from dns.message import make_query
from dns.query import https

def doh(name,type='A',server="223.5.5.5"):
    response = [_.to_text().split() for _ in https(make_query(name,type),server).answer]
    targets = []
    for res in response:
        for i in range(len(res)):
            if res[i]==type:
                targets.append(res[i+1].split('/')[0])
    return targets

def do_job(name,type='A',ns="223.5.5.5"):
    print(doh(name,type,ns))

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