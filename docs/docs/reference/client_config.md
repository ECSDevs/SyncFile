# 客户端配置文件

## 示例（默认值）

```json
{
    "host": "http://127.0.0.1:8000/", // 服务端所在地址，将自动补全前端`http://`和末尾`/`
    "indexPath": "index.json", // 索引文件地址，通过该字段可兼容老版MCSMT
    "localIndex": "dumped_index.json", // 客户端索引缓存，不建议和`indexPath`相同
    "ip": null, // 指定域名解析，可为IPv6或IPv4，字符串（单个）或列表（负载均衡）均可
    "preferV6": false, // 未指定IP时将此项改为真将触发强制V6解析，将调用内置DoH并负载均衡
    "dns": "223.5.5.5", // DoH解析服务器，确保其提供该服务
    "doh": false, // 未指定IP时强制触发内置DoH解析IPv4
    "update": true, // Hash值不匹配的删除并下载新版
    "removeNotfound": true, // 删除索引中不存在的文件
    "workers": 5, // 同时下载的进程数
}
```