<!--
 Copyright 2024 ECSDevs
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

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

** 注意：此时将会忽略所有路径中带`ignored`的目录（相对路径） **

对于每个文件，若扩展名符合`extension`，则加入索引。
若文件名不包含`.`，则匹配整个文件名。
若`["extension"]`项为`["*"]`（即包含`*`），忽略该要求。

对于每个索引中的文件，客户端将解析并保存到其`destination`文件夹下.
目录树将被自动创建。