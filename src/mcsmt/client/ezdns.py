from dns.message import make_query
from dns.query import https

def doh(name,type='A',server="223.5.5.5"):
    return [_.split()[4] for _ in ''.join([_.to_text() for _ in https(make_query(name,type),server).answer]).split('\n') if _.split()[3]==type]

if __name__=="__main__":
    print(doh(input("hostname:"),input("type:"),input("ns:")))