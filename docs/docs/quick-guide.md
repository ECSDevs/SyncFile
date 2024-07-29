---
sidebar: heading
sidebarDepth: 2
---

# 快速上手指南

带你一文速通 syncfile 之论文篇。

## 介绍

syncfile 是 Elementary (前元素云) 开源软件团队的成员 ECSDevs 独立编写的 Python 脚本程序。
该程序能够较为简单的在设备间**克隆**文件。是替代SMB协议的可选方案。

本方案适用于多个小文件的克隆，大文件克隆性能不佳。（取决于服务端侧使用的HTTP服务器解决方案）

## 技术特征

适用于互联网中的克隆，允许自定义DoH解析器、自定义IP、负载均衡等功能。
使用`httpx`网络模块，比`requests`性能更好。

## 实现原理

在被克隆（称为“服务端”）侧，根据用户确立的规则文件`config.json`，生成索引文件`client.json`，包含目标路径、文件路径、文件SHA512（前1MB摘要）。

服务端通过三方HTTP服务器提供服务，客户端根据配置文件`Cconfig.json`，拉取服务端索引，并根据索引拉取文件。

## 安装

想要安装 syncfile ？您仅需要一个 Python 环境以及一个 pip。
[推荐的Python POSIX环境](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

对于Windows，仅需要[安装Python](https://www.python.org/downloads/windows/)，并勾选“Add to PATH”以及“Pip”。

然后，您需要打开一个终端，可以是`bash`、`zsh`、`powershell`等，亦或者`cmd.exe`。
输入如下命令：
```sh
# 对于以推荐的方式安装的Python
pip install syncfile
# 对于Linux/Unix系统，使用系统Python3
python3 -m pip install syncfile
# 确保安装了Pip
python3 -m ensurepip
# 使用系统包管理器
# debian
sudo apt install python3-pip
# archlinux
sudo pacman -Sy python3-pip
# redhat
sudo yum install python3-pip
```

## 上手

syncfile常规使用非常简单，仅有两个功能。

### 服务端

解释：被“克隆”的机器。提供HTTP服务，故称为“服务端”

步骤：
1. 准备好需要被“克隆”的资源文件（最好集中在同一目录，推荐目录结构如下所示）
```
/ # 项目目录
| - resources
  | - someResource.txt
| - config.json
| - client.json # 自动生成
# 不建议有其他文件，该目录需要被整个开放到网络中，没有密码。
```
2. 编写`config.json`文件，如下
```json
// 本文件为示例，请根据实际需求修改
[
    ["resources", ["*"], "resources"]
]
```
3. 在终端运行如下指令
```sh
python -m syncfile.server
```
4. 运行一个HTTP服务器，将本目录暴露在网络中，例：
```sh
python -m http.server 8080
```

### 客户端

解释： “克隆”的机器，访问HTTP服务器，故称“客户端”

步骤：
1. 在需要同步的目录，新建`Cconfig.json`文件，示例：
```json
// 基本的配置文件，更多可选参数在文档中
{
    "requestURL": "http://127.0.0.1:8080/"
}
```
2. 打开终端，运行如下指令：
```sh
python -m syncfile.client
```
3. 成功同步远端`resources`目录到本地同名目录！

## 卸载

对于任何系统，仅需使用pip包管理器移除，如：
```sh
<python> -m pip uninstall syncfile
```
其中`<python>`是您的Python解释器路径。

## 更多

您可以访问[Github](https://github.com/ECSDevs/SyncFile)获取更多信息、反馈Bugs、参与讨论等。

如果您想要寻找更多的官方中文参考文档，请查看[参考文档](/reference/introduction.md)
