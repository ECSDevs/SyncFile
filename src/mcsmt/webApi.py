from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List
from . import *
from .logger import logger

# initialize application
app = FastAPI(
    title="MCSMT WebApi",
    description="An API for controlling MCSMT features and receive logs or data."
)

# read and clear client log
def read_and_clear_log()->str:
    try:
        with open("MCSMT.log", "r") as file:
            content = file.read()
    except FileNotFoundError:
        return ""
    with open("MCSMT.log", "w") as file:
        file.write("")
    return content

@app.get("/client/getlog", 
         response_model=str,
         response_description="Content of client log", 
         tags=["Client"])
def get_client_log():
    '''
    Read local "MCSMT.log" file and return, then clear it.
    '''
    return read_and_clear_log()

@app.get("/mixed/ezdns", 
         response_model=List,
         response_description="DNS lookup result", 
         tags=["Mixed"])
def ezdns(
    domain:str=Query(...,description="Domain name to query"), 
    type:str=Query("A",description="Record type to query"), 
    ns:str=Query("223.5.5.5",description="NameServer to query")
    ):
    '''
    Do DNS lookup use DNS over HTTPS.
    '''
    return mixed.ezdns.doh(domain, type, ns)

@app.get("/mixed/downloader",
         response_description="No response", 
         tags=["Mixed"])
def downloader(url:str = Query(description="URL to download from")):
    '''
    Download file from external URL.
    '''
    mixed.down.downloader(url)
    return None

# global quick-use objects
mcObjs = {}
cfModCached = {}

class modSearcherResponseModel(BaseModel):
    name:str = Field(description="Mod name", example="Just Enough Items")
    id:str = Field(description="Mod ID", example="cf_XXXXXX")
@app.get("/mixed/moddown",
         response_model=List[modSearcherResponseModel],
         response_description="Mod List",
         tags=["Mixed"])
def mod_searcher(
    mod:str=Query(description="Mod name to search"),
    ver:str=Query(description="Minecraft version for mod to search"),
    loader:str=Query(description="Mod loader for mod to search"),
    page:int=Query(0,description="Page number to search")
    ):
    '''
    Search mod from curseforge or modrinth.
    '''
    global mcObjs
    if not mcObjs.get(ver):
        mcObjs[ver] = {}
    if not mcObjs[ver].get(loader):
        mcObjs[ver][loader] = {}
    if not mcObjs[ver][loader].get("minecraft"):
        mcObjs[ver][loader]["minecraft"] = mixed.moddown.Minecraft(ver,loader)
    if not mcObjs[ver][loader].get("curseforge"):
        mcObjs[ver][loader]["curseforge"] = mixed.moddown.Curseforge(mcObjs[ver][loader]["minecraft"])
    if not mcObjs[ver][loader].get("modrinth"):
        mcObjs[ver][loader]["modrinth"] = mixed.moddown.Modrinth(mcObjs[ver][loader]["minecraft"])
    result = []
    for _ in mcObjs[ver][loader]["curseforge"].searchMod(mod,page):
        result.append({"name":_['name'], 'id':'cf_'+str(_['id'])})
        cfModCached[_['id']] = _
    for _ in mcObjs[ver][loader]["modrinth"].searchMods(mod,page):
        result.append({"name":_['title'], 'id':'mr_'+_['project_id']})
    return result

@app.get("/mixed/moddown/download",
         response_description="No response", 
         tags=["Mixed"])
def mod_downloader(
    ver:str=Query(description="Minecraft version for mod to download"),
    loader:str=Query(description="Mod loader for mod to download"),
    id:str=Query(description="Mod ID to download")
    ):
    '''
    Download mod from curseforge or modrinth.
    '''
    
    # parse id
    source, id = id.split('_')
    if source == "cf":
        source = "curseforge"
    elif source == "mr":
        source = "modrinth"
    
    # get objects
    if not mcObjs.get(ver):
        mcObjs[ver] = {}
    if not mcObjs[ver].get(loader):
        mcObjs[ver][loader] = {}
    if not mcObjs[ver][loader].get("minecraft"):
        mcObjs[ver][loader]["minecraft"] = mixed.moddown.Minecraft(ver,loader)
    if not mcObjs[ver][loader].get(source):
        mcObjs[ver][loader][source] = (
            mixed.moddown.Curseforge(mcObjs[ver][loader]["minecraft"])
            if source == "curseforge" else
            mixed.moddown.Modrinth(mcObjs[ver][loader]["minecraft"])
            if source == "modrinth" else
            None
        )
    executor = mcObjs[ver][loader][source]
    
    # main process
    if source == "curseforge":
        if not cfModCached.get(id):
            cfModCached[id] = executor.getMod(id)
        mod = cfModCached[id]
        file = executor.getFile(mod)
        mixed.down.downloader(file["downloadUrl"])
        for dependency in executor.parseRequirements(file["dependencies"]):
            logger.warn(f'''!DEPENDENCY! {dependency["data"]["name"]} ({dependency["dependencyType"]})''')
            if dependency["dependencyType"]=="RequiredDependency":
                mixed.down.downloader(dependency["data"]["downloadUrl"])
    elif source == "modrinth":
        version = executor.getVersions(id)
        mixed.down.downloader(version["files"][0]["url"],sha512hex=version["files"][0]["hash"]["sha512"])
        for dependency in executor.parseDependencies(version["dependencies"]):
            logger.warn(f'{executor.getMod(dependency["project_id"])["name"]} ({dependency["dependency_type"]})')
            if dependency["dependency_type"] == "required":
                dependencyVersion = executor.getVersion(dependency["version_id"])
                mixed.down.downloader(dependencyVersion["url"],sha512hex=dependencyVersion["files"][0]["hash"]["sha512"])
    
    return None
   