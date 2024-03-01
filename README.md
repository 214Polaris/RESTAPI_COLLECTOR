# API收集与差分工具

## 文件介绍
- `script_json_bytime` 用于收集API，其中会加上时间戳一起收集
- `script_json` 不加入时间戳收集
- `compare.py` 用于比较差分后的文件
- `drawer.py` 用于根据时间戳做聚类，然后绘制聚类后的分布折线图

## 使用方法

直接 `python xxx.py` 即可

目前使用顺序是先使用`script_json_bytime`收集两个平台的API，然后对于同一软件不同平台的结果, 分别跑 `drawer.py`，得到各自的 `cluster_result.json`, 再分别命名为 `a.json` 和
`b.json` 后跑 `compare.py`

目前还在调整阶段，等工具做好后会写一个脚本一次性将以上的内容全部做成脚本启动
