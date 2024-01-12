from httpx import get as webget
from .down import downloader as downloadFile
from json import load, dump
from os.path import exists
from ..logger import logger as l

class Game:
    def __init__(self,version:str,modLoader:str,gameID:int):
        self.version = version
        l.info(f'set Game.version = {version}')
        self.modLoader = modLoader.lower()
        l.info(f'set Game.modLoader = {modLoader}')
        self.id = gameID
        l.info(f'set Game.id = {gameID}')

class Minecraft(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, gameID=432)
        curseforgeModLoaderId = [ "any", "forge", "cauldron", "liteloader", "fabric", "quilt" ]
        self.enableCurseforge = True if self.modLoader in curseforgeModLoaderId else False
        l.info(f'set Minecraft.enableCurseforge = {self.enableCurseforge}')
        self.cfMLID = curseforgeModLoaderId.index(self.modLoader) if self.enableCurseforge else 0
        l.info(f'set Minecraft.cfMLID = {self.cfMLID}')
        modrinthModLoaders = ["fabric", "forge", "liteloader", "modloader", "neoforge", "quilt", "rift"]
        self.enableModrinth = True if self.modLoader in modrinthModLoaders else False
        l.info(f'set Minecraft.enableModrinth = {self.enableModrinth}')
        self.mrMLID = [["categories:"+self.modLoader]] if self.enableModrinth else []
        l.info(f'set Minecraft.mrMLID = {self.mrMLID}')
        

class Curseforge:
    dependencyTypes = ["NotKnown","EmbeddedLibrary","OptionalDependency","RequiredDependency","Tool","Incompatible","Include"]
    def cfEnabled(func):
        def wrapper(self, *args, **kwargs):
            if self.game.enableCurseforge:
                return func(self, *args, **kwargs)
            else:
                return {}
        return wrapper
    def __init__(self,game:Game):
        self.headers = {
            "Accept": "application/json",
            "x-api-key": "$2a$10$OQ.NA2.krpIOK1E7kBHSZ.8bDfkOIAqaKjxo8pGh35qUBRRqt/TGa"
        }
        l.info(f'set Curseforge.headers = {self.headers}')
        self.game = game
        l.info(f'set Curseforge.game = {self.game}')
    @cfEnabled
    def searchMod(self,modname,page=0):
        apiUrl = "https://api.curseforge.com/v1/mods/search"
        params = {
            'gameId': self.game.id,
            'gameVersion': self.game.version,
            'modLoaderType': self.game.modLoader,
            'searchFilter': modname,
            'pageSize': 5,
            'index': page*5
        }
        r = webget(apiUrl, params = params, headers = self.headers)
        l.info(f'HTTP GET {apiUrl} params {params} result {r.text}')
        return r.json()["data"]
    @cfEnabled
    def getFile(self,data):
        for fileIndex in data["latestFilesIndexes"]:
            if fileIndex["gameVersion"]==self.game.version and fileIndex["modLoader"]==self.game.modLoader:
                fileId = fileIndex["fileId"]
                break
        for file in data["latestFiles"]:
            if file["id"]==fileId:
                dt = file
                break
        l.info(f'getFile {dt}')
        return dt
    @cfEnabled
    def getDescription(self,modId):
        apiUrl = "https://api.curseforge.com/v1/mods/%s/description"%modId
        r = webget(apiUrl,headers=self.headers).json()
        l.info(f'HTTP GET {apiUrl} result {r}')
        return r["data"]
    @cfEnabled
    def getMod(self,modId):
        apiUrl = "https://api.curseforge.com/v1/mods/%s"%modId
        data = webget(apiUrl,headers=self.headers).json()
        l.info(f'HTTP GET {apiUrl} result {data}')
        return data["data"]
    @cfEnabled
    def parseRequirements(self,requirementData):
        result = []
        for requirement in requirementData:
            result.append({"data": self.getMod(requirement["modId"]), "dependencyType": Curseforge.dependencyTypes[requirement["relationType"]]})
        l.info(f'Dependency parse result {result}')
        return result
    
    # Requirement Types ["NotKnown","EmbeddedLibrary","OptionalDependency","RequiredDependency","Tool","Incompatible","Include"]

class Modrinth:
    def mrEnabled(func):
        def wrapper(self, *args, **kwargs):
            if self.game.enableModrinth:
                return func(self, *args, **kwargs)
            else:
                return {}
        return wrapper
    def __init__(self,game:Minecraft):
        self.headers = {
            "User-Agent": "ECSDevs/MCSMT/3.0.3 (originalFactor@qq.com)"
        }
        l.info(f'set Modrinth.headers = {self.headers}')
        self.game = game
        l.info(f'set Modrinth.game = {self.game}')
    @mrEnabled
    def searchMods(self,modname,page=0):
        url = "https://api.modrinth.com/v2/search"
        params = {
            "query": modname,
            "facets": self.game.mrMLID + [["versions:"+self.game.version]],
            "offset": 5*page,
            "limit": 5
        }
        res = webget(url,params,headers=self.headers).json()
        l.info(f'HTTP GET {url} params {params} result {res}')
        return res["hits"]
    @mrEnabled
    def getVersions(self,project_id):
        url = f'https://api.modrinth.com/v2/project/{project_id}/version'
        params = {
            "loaders": self.game.modLoader,
            "game_versions": self.game.version
        }
        response = webget(url,params,headers=self.headers).json()
        l.info(f'HTTP GET {url} params {params} result {response}')
        return response
    @mrEnabled
    def getMod(self, project_id):
        url = f"https://api.modrinth.com/v2/project/{project_id}"
        response = webget(url,headers=self.headers).json()
        l.info(f'HTTP GET {url} result {response}')
        return response
    @mrEnabled
    def parseDependencies(self,  dependencies):
        ds = []
        for depend in dependencies:
            ds += [depend]
            if depend["dependency_type"]=="required":
                ds += self.parseDependencies(self.getVersion(depend["version_id"])["dependencies"])
        l.info(f'Dependency parse result {set(ds)}')
        return set(ds)
    @mrEnabled
    def getVersion(self, version_id):
        url = f'https://api.modrinth.com/v2/version/{version_id}'
        response = webget(url,headers=self.headers).json()
        l.info(f'HTTP GET {url} result {response}')
        return response

def do_job():
    print("Warning: Any silent crash could be due to network reasons! Make sure you have access to api.curseforge.com!")
    mc = Minecraft(input("Minecraft Version: "), input("Mod Loader(Any,Forge,Cauldron,LiteLoader,Fabric,Quilt,Neoforge,ModLoader,Rift): "))
    cf = Curseforge(mc)
    mr = Modrinth(mc)
    try:
        while True:
            name = input("Mod Name: ")
            page = 0
            while True:
                modinfoCF = cf.searchMod(name,page)
                modinfoMR = mr.searchMods(name,page)
                for mod in range(len(modinfoCF)):
                    print(f"[{mod}] {modinfoCF[mod]['name']}")
                for mod in range(len(modinfoMR)):
                    print(f"[{mod+len(modinfoCF)}] {modinfoMR[mod]['name']}")
                x = input("Select: ")
                if x:
                    break
                page += 1
            if not x.isdigit() or int(x)<0:
                continue
            if int(x)<len(modinfoCF):
                print(cf.getDescription(modinfoCF[int(x)]["id"]))
                file = cf.downloadMod(modinfoCF[int(x)])
                downloadFile(file["downloadUrl"])
                for dependency in cf.parseRequirements(file):
                    print(f'''{dependency["data"]["name"]} ({dependency["dependencyType"]})''')
                    if dependency["dependencyType"]=="RequiredDependency":
                        downloadFile(dependency["data"]["downloadUrl"])
                print('''Automaticly downloaded RequiredDependency.''')
                continue
            print(modinfoMR[int(x)]["description"])
            version = mr.getVersions(modinfoMR[int(x)]["project_id"])
            downloadFile(version["files"][0]["url"],sha512hex=version["files"][0]["hash"]["sha512"])
            for dependency in mr.parseDependencies(version["dependencies"]):
                print(f'{mr.getMod(dependency["project_id"])["name"]} ({dependency["dependency_type"]})')
                if dependency["dependency_type"] == "required":
                    dependencyVersion = mr.getVersion(dependency["version_id"])
                    downloadFile(dependencyVersion["url"],sha512hex=dependencyVersion["files"][0]["hash"]["sha512"])
            print('''Automaticly downloaded RequiredDependency.''')
    except KeyboardInterrupt:
        print("用户退出")
