# MCServerManageTools

这个项目是为了更加方便的使用Minecraft而开发的。

通过部署Server Pack，能够管理Client Pack.

## Server Pack教程

在[Github Releases](https://github.com/PsBashTeam/MCSMT/releases/latest)下载`serverpack_<version>.zip`

解压后得到以下文件：
- server.exe
- server_function.exe
- config_gen.exe

先运行`config_gen.exe`生成得到`config.json`

运行`server.exe`生成得到`client.json`

此时可以选择提交/上传到web服务器或者运行`server_function.exe`启动服务器

## Client Pack 教程

同样在GitHub Releases下载`client_pack_<version>.zip`

解压后得到以下文件：
- starter.exe
- client.exe
- Cconfig.json

一般情况下，只需要用到后两个。

先编辑`Cconfig.json`，使`requestURL`的值是您服务器的URL。
    如果您在使用我们的`server_function.exe`，其地址为`http://127.0.0.1:7809`且无法更改。该程序仅用于测试，请上传到web服务器使用。如果您一定要使用该程序，请使用反向代理程序。

然后启动`client.exe`即可

### （可选）Starter.exe

该文件能够作为启动器启用。

当用户打开它，会先启动`client.exe`，等待执行完毕后再启动`mcl.exe`。

该文件很容易被误认为是病毒。比如Windows Defender.

## Config_gen.exe 特性详解
该文件能够帮助你自动生成`config.json`

## Server.exe 特性详解
该文件能够根据你的`config.json`里的规则，通过SHA512算法输出`client.json`

## Server_function.exe 特性详解
创建一个web服务器，HTTP地址（不可修改）是`http://127.0.0.1:7809/`，根目录是当前文件夹。一般作为测试服务器使用

## Client.exe 特性详解
通过`Cconfig.json`定义api伺服器地址。通过api伺服器上的`client.json`执行对资源的管理操作。验证算法为`SHA512`.

