# evue

> Evue是一个高性能的跨平台应用开发框架，可以运行在windows/linux/macos/web/ios/andriod/rtos多种平台，一次开发，多端运行!

 查看 [English](https://github.com/scriptiot/evue/blob/master/README.md) 英文说明.

 阅读 [《EVUE 进化蜕变，下一代全平台UI开发利器》](https://www.yuque.com/dragondjf/ltn95z/krmcxd?singleDoc)了解更多介绍

## 特性

![brief](doc/images/brief.png)

+ Just python as you like 
+ multi-user for web
+ dark/light theme support
+ responsive support
+ ...

## 框架

+ Evue 架构

> Evue 是一个基于html/css的高性能的gui应用框架，与平台和ui引擎无关

![evue](doc/images/evue.png)


+ Evuecompiler 编译器架构

> evue编译器的功能主要是将evue文件编译为python/javascript代码；

![evuecompiler](doc/images/evuecompiler.png)

+ Evue 全平台运行
    + Evue for flutter (windows/linux/macos/web/ios/andriod)
    + Evue for lvgl（rtos on mcu like Asr3603/F1C100/F1C200/esp32/stm32/...）
> you can run evue on any platfom as you like!

+ Evue 支持适配任何ui引擎
    + Evue for flutter
    + Evue for lvgl
    + Evue for Qt
    + Evue for PySide2
    + ...
> you can compile evue to any ui code as you like!

## 安装
使用 [pip](https://github.com/scriptiot/evue)安装evue.

```bash
pip install evue
```

or
```bash
git clone https://github.com/scriptiot/evue.git
cd evue
python setup.py install # also `pip install ."
```

## 快速开始

+ [evue_website](https://github.com/scriptiot/evue/tree/master/examples/evue_website)

```python
cd examples
python evuebroswer.py ./evue_website/project.json
or
python evuebroswer.py ./evue_website/app.py
```

![evue_website](doc/images/evue_website.gif)

+ [evue_login](https://github.com/scriptiot/evue/tree/master/examples/evue_login)

```python
cd examples
python evuebroswer.py ./evue_login/project.json
or
python evuebroswer.py ./evue_login/app.py
```
![evue_login](doc/images/evue_login.gif)

## Evue Studio

> Evue Studio 是一个服务开发者快速创建/编译/发布基于evue的应用的开发者平台。

![designer](doc/images/designer.png)

[下载最新的evue studio](https://gitee.com/scriptiot/evue/releases/download/0.1.6/evuestudio-20221215150224-9cd20e3.7z)

+ 解压evuestudio-20221215150224-9cd20e3.7z
+ 双击 `evuedesigner.exe`

## Evue for iot
> Evue for iot 是一个基于evue的商业产品`quicknode`, 轻量级evue解决方案，可以运行在各种mcu上。

![quicknode](doc/images/quicknode.gif)

更多介绍请阅读 [quicknode产品介绍](doc/EVUE%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8DPDF%E7%89%88.pdf)

[下载最新的quicknode](https://gitee.com/scriptiot/evue/releases/download/0.1.6/quicknode-qbc-20221215142421-693fbf88.zip)

+ 解压quicknode-qbc-20221215142421-693fbf88.zip
+ 双击 `quicknode.bat` or `quicknode_chart.bat` 

[帮助手册](https://www.yuque.com/bytecode/eu1sci/edzq05)

## 社区讨论

+ [Discussions](https://github.com/scriptiot/evue/discussions)
+ [Issues](https://github.com/scriptiot/evue/issues)


## 社区达人招募

+ `无论您是社区技术达人、设计师、产品经理、运营者，欢迎为evue项目贡献自己的一份力量! 您将在贡献者名单上榜上有名！`
+ `如果你喜欢，请发送email到【ding465398889@163.com】或者添加微信dragondjf！`

## 联系我们

> 如果需要更多的技术支持或者商务合作, 请发送email/微信/QQ获取更多详细的支持!

+ Email : ding465398889@163.com
+ WeChat: dragondjf
>![dragondjf](doc/images/dragondjf.jpg)
+ Evue for IOT
>![dragondjf](doc/images/QQ.jpg)


## 致敬

+ [evm](https://github.com/scriptiot/evm)
+ [lvgl](https://github.com/lvgl/lvgl)
+ [flet](https://github.com/flet-dev/flet)
+ [flutter](https://github.com/flutter/flutter)
