# 服务端配置文件

## 介绍

- 用途：`python -m syncfile.server [--config <filepath>]`
- 默认值：`./config.json`
- 等级：核心
::: warning 警告
    您必须拥有该文件才能正常使用 Syncfile Server 。
:::

## 示例

```json
[
    ["source", ["extension"], "destination", ["ignored"]]
]
```

## 行为模式

Syncfile Server 将导入该文件作为config对象，并遍历其内容。

对于每个条目，将自动检索本地`source`目录中的对象（并遍历其，以寻找可能的子目录）。

** 注意：此时将会忽略`source/ignored`目录以及他的所有子目录（文件不受影响） **
