# MCSMT ( Minecraft Server Manage Tool)

讨论用QQ频道：频道号: r2mjr3649b，频道名：RIAN真会玩，在【项目相关】板块讨论

## 运行方式

.whl文件：
```bash
pip install <whl文件路径> --force-reinstall
```
新版目前只能使用.whl/.tar.gz安装

## 服务端

1. 首先用`python -m mcsmt.server.genconf`生成服务器配置  

2.1. 静态服务端  

2.1.1. 运行`python -m mcsmt.server.gen`,生成引导之后打包传上服务器

2.2. 动态服务端  

2.2.1. 直接启动`python -m mcsmt.server.simplehttp`即可启动便捷式服务器  

2.2.2. 高级模式：linux安装wsgi服务器后，启动simple_server模块内的app程序  

2.2.3. 自动生成：启动`python -m mcsmt.server.wdgen`即可自动监测文件变动，自动生成（目前不稳定）

## 客户端
写一个`Cconfig.json`，像这样：
```json
{
    "requestURL": "http://api.example.com/"
}
```
启动`python -m mcsmt.client.main`即可同步

## 工具

### mod downloader

一个mod下载器，需要自己到docs.curseforge.com申请开发者账号。登陆后左侧api-复制token-粘贴进工具即可。  
启动方式：`python -m mcsmt.mixed.moddown`

### 扩展下载器

`python -m mcsmt.mixed.extdown`