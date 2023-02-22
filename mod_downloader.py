import requests, json, os

# config
myConfig = {}
# save my config
def saveConfig():
    configfile = open('moddl.cfg','w')
    json.dump(myConfig,configfile)
    configfile.close()
    print("config saved")
# load my config
def loadConfig():
    try: 
        configfile = open('moddl.cfg')
        myConfig = json.load(configfile)
        configfile.close()
    except: 
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
    r = requests.get(apiUrl, params = params, headers = myConfig['headers'])
    return r.json()

# mod file downloading module
def downloadMod(fileId,modId):
    apiUrl = "https://api.curseforge.com/v1/mods/%s/files/%s"%(modId,fileId)
    data = requests.get(apiUrl,headers=myConfig['headers']).json()["data"]
    print("start to download",data["downloadUrl"].split('/')[-1])
    chooseChannel(data["downloadUrl"])
    print("downloaded")
    return data

# download channel chooser
def chooseChannel(dlUrl):
    if os.path.isfile('wget_ext.exe'):
        print('You have WGET extension! using wget to download.')
        stat = os.system('wget \"%s\"'%(dlUrl))
        if stat:
            print("something went wrong. file may lose. you can try again.")
    else:
        print("oh no! you didnt download wget extension! using traditional download method. file may broken.")
        downloader(dlUrl)

# self-build downloader
def downloader(dlUrl):
    with open(data["downloadUrl"].split('/')[-1],'wb')as f:
        f.write(requests.get(data["downloadUrl"]).content)

# mod description shower
def showDescription(modId):
    apiUrl = "https://api.curseforge.com/v1/mods/%s/description"%modId
    print('this mod\'s description:',requests.get(apiUrl,headers=myConfig['headers']).json()["data"])

# show mod name
def showModName(modId,reqtype):
    apiUrl = "https://api.curseforge.com/v1/mods/%s"%modId
    data = requests.get(apiUrl,headers=myConfig['headers']).json()["data"]
    reqtypes = ["NotKnown","EmbeddedLibrary","OptionalDependency","RequiredDependency","Tool","Incompatible","Include"]
    print(data["name"],"[%s]"%(reqtypes[reqtype]))
    return data

# show requirements
def showRequirements(reqdata):
    print("requirements:")
    for req in reqdata:
        showModName(req["modId"],req["relationType"])

loadConfig()
mcv = input("Minecraft Version? : ")
ml = int(input("ModLoader Type? (see mod_downloader_readme.txt): "))
myConfig["headers"]["x-api-key"] = input("please enter your own api key :")
saveConfig()

print("Warning: Any silent crash could be due to network reasons! Make sure you have access to api.curseforge.com!")

while True:
    cmd1 = input('you want to (download/end): ')
    if cmd1=='end':
        break
    cmd2 = input("mod name: ")
    modinfo = searchMod(cmd2,mcv,ml)["data"]
    for mod in range(len(modinfo)):
        print("[%d]"%mod,modinfo[mod]["name"])
    which = input("select: ")
    if which:
        which = int(which)
    else:
        continue
    showDescription(modinfo[which]["id"])
    for version in modinfo[which]["latestFilesIndexes"]:
        if version["gameVersion"]==mcv and version["modLoader"]==ml:
            filedata = downloadMod(version["fileId"],modinfo[which]["id"])
            break
    showRequirements(filedata["dependencies"])
