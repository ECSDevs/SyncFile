import requests

# curseforge token info
class curseAPI():
    headers = {
    'Accept': 'application/json',
    'x-api-key': '$2a$10$/PIkSX.Dmzoh4sWT0ZTXDejBQsQELeBPXNRlR3msi/8lflWaX/1iu'
    }
    gameId = "432"

# mod searching module
def searchMod(modname,ver,ml):
    apiUrl = "https://api.curseforge.com/v1/mods/search"
    params = {
        'gameId': curseAPI.gameId,
        'gameVersion': ver,
        'modLoaderType': ml,
        'searchFilter': modname
    }
    r = requests.get(apiUrl, params = params, headers = curseAPI.headers)
    return r.json()

# mod file downloading module
def downloadMod(fileId,modId):
    apiUrl = "https://api.curseforge.com/v1/mods/%s/files/%s"%(modId,fileId)
    data = requests.get(apiUrl,headers=curseAPI.headers).json()["data"]
    print("start to download",data["downloadUrl"].split('/')[-1])
    with open(data["downloadUrl"].split('/')[-1],'wb')as f:
        f.write(requests.get(data["downloadUrl"]).content)
    print("downloaded")
    return data

# mod description shower
def showDescription(modId):
    apiUrl = "https://api.curseforge.com/v1/mods/%s/description"%modId
    print('this mod\'s description:',requests.get(apiUrl,headers=curseAPI.headers).json()["data"])

# show mod name
def showModName(modId,reqtype):
    apiUrl = "https://api.curseforge.com/v1/mods/%s"%modId
    data = requests.get(apiUrl,headers=curseAPI.headers).json()["data"]
    reqtypes = ["NotKnown","EmbeddedLibrary","OptionalDependency","RequiredDependency","Tool","Incompatible","Include"]
    print(data["name"],"[%s]"%(reqtypes[reqtype]))
    return data

# show requirements
def showRequirements(reqdata):
    print("requirements:")
    for req in reqdata:
        showModName(req["modId"],req["relationType"])

mcv = input("Minecraft Version? : ")
ml = int(input("ModLoader Type? (see mod_downloader_readme.txt): "))

while True:
    cmd1 = input('you want to (download/end): ')
    if cmd1=='end':
        break
    cmd2 = input("mod name: ")
    modinfo = searchMod(cmd2,mcv,ml)["data"]
    for mod in range(len(modinfo)):
        print("[%d]"%mod,modinfo[mod]["name"])
    which = int(input("select: "))
    showDescription(modinfo[which]["id"])
    for version in modinfo[which]["latestFilesIndexes"]:
        if version["gameVersion"]==mcv and version["modLoader"]==ml:
            filedata = downloadMod(version["fileId"],modinfo[which]["id"])
            break
    showRequirements(filedata["dependencies"])
