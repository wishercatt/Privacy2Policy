### Privacy2Policy

下载ltp 3.4.0 模型放在 ./data/model目录
[模型地址](http://ltp.ai/download.html)




pyltp需要自编译 (有编译好的64位pyltp放在./data/dependencies/目录)
```
pip install ./data/dependencies/pyltp-0.2.1-cp37-cp37m-win_amd64.whl
```


使用
-i 指定mhtml文件/文件夹
-m 指定标记文件/文件夹
-p 记录分析结果
-s 分析指定句子
```
Privacy2Policy.py -l ./input/mhtml -m ./input/markfiles -p
```