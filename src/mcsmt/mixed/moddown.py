from httpx import get as webget
from .down import downloader as downloadFile
from json import load, dump

# config
myConfig = {}
# save my config
def saveConfig(config_path,encoding="UTF-8"):
    configfile = open(config_path,'w',encoding=encoding)
    dump(myConfig,configfile)
    configfile.close()
    print("config saved")
# load my config
def loadConfig(config_path,enc):
    global myConfig
    try: 
        configfile = open(config_path,encoding=enc)
        myConfig = load(configfile)
        configfile.close()
    except FileNotFoundError:
        print("no config file found. loaded default config.")
        myConfig = dConfig
    else:
        if not myConfig:
            myConfig = dConfig


# default config
dConfig = {
    'headers' : {
        'Accept': 'application/json',
        'x-api-key': ''
    },
    'gameId' : "432"
}

# mod searching module
def searchMod(modname,ver,ml):
    apiUrl = "https://api.curseforge.com/v1/mods/search"
    params = {
        'gameId': myConfig['gameId'],
        'gameVersion': ver,
        'modLoaderType': ml,
        'searchFilter': modname
    }
    r = webget(apiUrl, params = params, headers = myConfig['headers'])
    return r.json()

# mod file downloading module
def downloadMod(fileId,modId):
    apiUrl = "https://api.curseforge.com/v1/mods/%s/files/%s"%(modId,fileId)
    data = webget(apiUrl,headers=myConfig['headers']).json()["data"]
    downloadFile(data["downloadUrl"])
    return data

# mod description shower
def showDescription(modId):
    apiUrl = "https://api.curseforge.com/v1/mods/%s/description"%modId
    print('this mod\'s description:',webget(apiUrl,headers=myConfig['headers']).json()["data"])

# show mod name
def showModName(modId,reqtype):
    apiUrl = "https://api.curseforge.com/v1/mods/%s"%modId
    data = webget(apiUrl,headers=myConfig['headers']).json()["data"]
    reqtypes = ["NotKnown","EmbeddedLibrary","OptionalDependency","RequiredDependency","Tool","Incompatible","Include"]
    print(data["name"],"[%s]"%(reqtypes[reqtype]))
    return data

# show requirements
def showRequirements(reqdata):
    print("requirements:")
    for req in reqdata:
        showModName(req["modId"],req["relationType"])


def do_job(config_path="./moddl.cfg",config_enc="UTF-8",**kwargs):
    loadConfig(config_path,config_enc)
    for i in kwargs:
        myConfig[i]=eval(kwargs[i])
    if myConfig.get("xapikey"):
        myConfig["headers"]["x-api-key"] = myConfig["xapikey"]
        del myConfig["xapikey"]
    saveConfig(config_path,config_enc)
    print("Warning: Any silent crash could be due to network reasons! Make sure you have access to api.curseforge.com!")
    for name in myConfig["modl"]:
        modinfo = searchMod(name,myConfig['mcv'],myConfig['ml'])["data"]
        print("NAME:",modinfo[0]["name"])
        showDescription(modinfo[0]["id"])
        for version in modinfo[0]["latestFilesIndexes"]:
            if version["gameVersion"]==myConfig['mcv'] and version["modLoader"]==myConfig['ml']:
                filedata = downloadMod(version["fileId"],modinfo[0]["id"])
                showRequirements(filedata["dependencies"])
                break

# loadConfig()
# mcv = input("Minecraft Version? : ")
# ml = int(input("ModLoader Type? (see mod_downloader_readme.txt): "))
# myConfig["headers"]["x-api-key"] = input("please enter your own api key :")
# saveConfig()
#
# print("Warning: Any silent crash could be due to network reasons! Make sure you have access to api.curseforge.com!")
#
# while True:
#     cmd1 = input('you want to (download/end): ')
#     if cmd1=='end':
#         break
#     cmd2 = input("mod name: ")
#     modinfo = searchMod(cmd2,mcv,ml)["data"]
#     for mod in range(len(modinfo)):
#         print("[%d]"%mod,modinfo[mod]["name"])
#     which = input("select: ")
#     if which:
#         which = int(which)
#     else:
#         continue
#     showDescription(modinfo[which]["id"])
#     for version in modinfo[which]["latestFilesIndexes"]:
#         if version["gameVersion"]==mcv and version["modLoader"]==ml:
#             filedata = downloadMod(version["fileId"],modinfo[which]["id"])
#             break
#     showRequirements(filedata["dependencies"])
