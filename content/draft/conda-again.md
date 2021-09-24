---
title: "再谈Anaconda的使用"
date: 2021-09-24T17:20:13+08:00
draft: true
isCJKLanguage: true
toc: true
categories:
- 编程
tags:
- anaconda
- conda
- python
---

一直以来我都是使用virtualenv来管理Python版本，并且写了一个脚本程序用来更新三方包和解决依赖问题，只能说是够用，但是并不好用。而我一直没有选择用Conda来管理Python虚拟环境，是由于早期使用的时候没有深入了解，包管理给我的第一印象一样是不智能，比如我使用conda-forge环境安装了一些包和一些依赖，下次update的时候Conda就给我全部使用default频道并降级版本，这哪里是升级，明明是降级啊。

```bash
vim ~/.condarc
```
```apacheconf
channel_priority: flexible
channels:
  - conda-forge
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

### rc文件参数说明
> `channel_priority`有三个可选值：`strict`，`flexible`，`disabled`
> - `strict`:当软件包出现在优先级更高的channels中时，就完全不考虑低channels里的包，高优先级未找到依次向下寻找。
>  - `flexible`:会从低优先级channels寻找包，用来填补缺失的依赖（优先级高的channels优先使用）。老版本的True参数对应该参数。
>  - `disabled`:禁用优先级，只使用最高优先级。
# 参考
[Managing channels](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html#strict-channel-priority)