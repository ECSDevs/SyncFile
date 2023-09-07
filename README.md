# MCSMT ( Minecraft Server Manage Tool)

[English](README.en.md)

讨论用QQ频道：频道号: r2mjr3649b，频道名：RIAN真会玩，在【项目相关】板块讨论

## 运行方式

.whl文件：
```bash
pip install <whl文件路径> --force-reinstall
```
新版目前只能使用.whl/.tar.gz安装

**2023/9/7更新：全面支持MCSMTApi，使用MCSMT CLI启动**

## 服务端

1. 首先用`python -m mcsmt server genconf`生成服务器配置  

2.1. 静态服务端  

2.1.1. 运行`python -m mcsmt server gen`,生成引导之后打包传上服务器

2.2. 动态服务端  

2.2.1. 直接启动`python -m http.server <port>`即可启动便捷式服务器（2023/9/7修改：内置简易服务器已删除，请使用Python自带服务器或IIS等）  

2.2.3. 自动生成：启动`python -m mcsmt server wdgen`即可自动监测文件变动，自动生成（目前不稳定）

## 客户端
写一个`Cconfig.json`，像这样：
```json
{
    "requestURL": "http://api.example.com/"
}
```
启动`python -m mcsmt client main`即可同步

## 工具

### mod downloader

一个mod下载器，需要自己到docs.curseforge.com申请开发者账号。登陆后左侧api-复制token-粘贴进工具即可。  
启动方式：`python -m mcsmt mixed moddown`

### 扩展下载器

`python -m mcsmt mixed extdown`

## MCSMTApi

从 Alpha Version 3.0.2.12.0 开始，MCSMT开始使用MCSMTApi作为新的调用方式，旧的python模块调用方式已退出。

更多内容参见QQ频道。