# MCSMT ( Minecraft Server Manage Tool)
讨论用QQ频道：频道号: r2mjr3649b，频道名：RIAN真会玩，在【项目相关】板块讨论
## 运行方式
直接运行源代码   
ps:源代码在`src/mcsmt`文件夹  
依赖：requests, flask, watchdog  
扩展插件：wget  
依赖安装方式：  
```bash
pip install -r requirements.txt
```
扩展插件可以直接用`extension_downloader.py`安装。 （whl版本命令：`python -m mcsmt.mixed.extension_downloader`，任何路径下都可用）

**新推荐：使用Pipenv或.whl文件安装**

Pipenv：
```bash
pip install pipenv
pipenv install
```

.whl文件：
```bash
pip install <whl文件路径> --force-reinstall
```

## 服务端（`server`文件夹）
1. 首先用`config_gen.py`生成服务器配置（whl版本命令：`python -m mcsmt.server.config_gen`，任何路径下都可用）
2.1. 静态服务端
2.1.1. 直接启动`server_generate.py`,生成引导之后打包传上服务器（whl版本命令：`python -m mcsmt.server.server_generate`，任何路径下都可用）
2.2. 动态服务端
2.2.1. 直接启动`simple_server.py`即可启动便捷式服务器（whl版本命令：`python -m mcsmt.server.simple_server`，任何路径下都可用）
2.2.2. 高级模式：linux安装wsgi服务器后，启动simple_server模块内的app程序

## 客户端（`client`文件夹）
写一个`Cconfig.json`，像这样：
```json
{
    "requestURL": "http://api.example.com/"
}
```
启动`client.py`即可同步（whl版本命令：`python -m mcsmt.client.client`，任何路径下都可用）
## 工具（`mixed`文件夹）
### mod downloader
一个mod下载器，需要自己到docs.curseforge.com申请开发者账号。登陆后左侧api-复制token-粘贴进工具即可。  
启动方式：`mod_downloader.py`（whl版本命令：`python -m mcsmt.mixed.mod_downloader`，任何路径下都可用）
