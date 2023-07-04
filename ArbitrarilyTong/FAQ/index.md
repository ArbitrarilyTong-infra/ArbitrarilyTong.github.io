# 常见问题集合

## 为什么我刷入后无限重启？
如果您是从别的系统刷入任意桐，请检查data分区是否已经清除，如果没有，请清除您的data分区

## ArbitrarilyTong设置闪退/翻译字符串错乱
这是因为你刷包刷多了Data又没清除留下的缓存

删除 `/data/system/package_cache/` 下的所有文件即可