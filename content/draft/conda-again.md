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

## condarc配置文件
一直以来我都是使用virtualenv来管理Python版本，并且写了一个脚本程序用来更新三方包和解决依赖问题，只能说是能用够用，但是并不好用。而我一直没有选择用Conda来管理Python虚拟环境，是由于早期使用的时候没有深入了解，包管理给我的第一印象一样是不智能，比如我使用conda-forge环境安装了一些包和一些依赖，下次update整体虚拟环境的时候Conda就给我全部使用default频道并降级版本，这哪里是升级，明明是降级啊。究其原因就是channels设置的不对，下面贴出我的正确的`.condarc`文件，然后再一一解释。

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
>  - `flexible`:会从低优先级channel寻找包，用来填补缺失的依赖（优先级高的channel优先使用）。老版本的True参数对应该参数。
>  - `disabled`:禁用优先级，只使用最高优先级。


> `custom_channels`:这里设置非官方渠道的channel，比如上面我在用的[清华](https://mirrors.tuna.tsinghua.edu.cn/anaconda/)镜像。


> `channels`:这也是最重要的一个设置，包管理器就是按照这里的顺序从上到下搜索排序包，例如我喜欢用`conda-forge`这个channel，那我就把他放到第一位，这样只要是能够搜索到的都优先使用这里的包。

这样设置完，每次安装和更新的时候，都会优先从`conda-forge`这个channel安装，如果没有再从下面的其他channel搜索。还有一个要注意的点是我并没有把pytorch加入到`channels`里，所以当我想安装GPU版本的pytorch时，包管理器是找不到结果的，因为这部分我想自己手动，所以安装的时候都要加上`-c pytorch`选项。

## 备份和恢复环境

### pip

### conda

## 参考
[Managing channels](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html#strict-channel-priority)