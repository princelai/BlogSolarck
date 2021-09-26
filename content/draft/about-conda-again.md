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
一直以来我都是使用virtualenv来管理Python版本，并且写了一个脚本程序用来更新三方包和解决依赖问题，只能说是能用够用，但是并不好用。而我一直没有选择用Conda来管理Python虚拟环境，是由于早期使用的时候没有深入了解，包管理给我的第一印象是不智能，比如我使用conda-forge渠道安装了一些包和一些依赖，下次update整体虚拟环境的时候Conda就给我全部使用default频道并降级版本，这哪里是升级，明明是降级啊。究其原因就是channels设置的不对，下面贴出我的正确的`.condarc`文件，然后再一一解释。

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


> `custom_channels`:这里设置非官方渠道的channel，比如上面我在用的[清华](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)镜像或者[中科大](https://mirrors.ustc.edu.cn/help/anaconda.html)镜像。


> `channels`:这也是最重要的一个设置，包管理器就是按照这里的顺序从上到下搜索排序包，例如我喜欢用`conda-forge`这个channel，那我就把他放到第一位，这样只要是能够搜索到的都优先使用这里的包。

这样设置完，每次安装和更新的时候，都会优先从`conda-forge`这个channel安装，如果没有再从下面的其他channel搜索。还有一个要注意的点是我并没有把pytorch加入到`channels`里，所以当我想安装GPU版本的pytorch时，包管理器是找不到结果的，因为这部分我想自己手动，所以安装的时候都要加上`-c pytorch`选项。

## 备份和恢复环境

### pip
使用传统的pip进行备份和回复，这里使用`pip list`而不是`pip freeze`是因为conda和pip版本兼容性问题，下面这种方法输出的格式兼容性更好。
```bash
pip list --format=freeze >! requirements.txt
```
```bash
conda create -n <env_name> python=3.x
pip install -r requirements.txt
```
### conda
conda备份就简单明了许多，导出环境，从环境文件创建并安装所有包。
```bash
conda env export -f environment.yml
```
```bash
conda create --file environment.yml
```
### conda-tree
conda-tree是一个好用的小工具，详细参数可以查看其[项目主页](https://github.com/rvalieris/conda-tree)，最主要的功能是可以输出一个最精简依赖列表，也就是输出依赖树上所有叶子节点和孤包，根据这些包就能自动把全部依赖安装上。
```bash
conda-tree -n <env_name> leaves --export >! condatree.txt
```
```bash
conda create -n <env_name> python=3.x --file condatree.txt
```

## 依赖关系
### conda-tree
`conda-tree`是一个树状依赖查看工具，功能强大，使用方便。最大的好处是在一个环境里安装了就可以查看其他conda环境的依赖关系，不需要每个环境都安装一遍才能使用。这里只记录一些我常用的命令：
1. \<package\>包的依赖列表
```bash
conda-tree depends <package>
```

2. \<package\>包的被依赖列表
```bash
conda-tree whoneeds <package>
```

3. \<env_name\>环境\<package\>包的依赖树
```bash
conda-tree -n <env_name> depends -t <package>
```

4. \<env_name\>环境全部依赖树
```bash
conda-tree -n <env_name> deptree --full
```
<br>

当然也可以将树状依赖关系转换成dot格式，最终输出为PDF、SVG或PNG，方便查看。dot转换需要安装`graphviz`软件，这部分需要自行安装。

```bash
conda-tree -n <env_name> deptree --dot > file.dot # <env_name>环境全部依赖关系
conda-tree depends <package> --dot > file.dot # <package>依赖的包
conda-tree whoneeds <package> --dot > file.dot # 依赖<package>的包
```
```bash
dot -Tpng file.dot -o tree.png
```
```bash
dot -Tpdf file.dot -o tree.pdf
```
### pipdeptree

## GPU环境
也就是需要安装CUDA的Python虚拟环境。现在深度学习在Python上越来越普遍，用Conda创建虚拟环境可以把工作大大简化。Conda创建CUDA环境的好处是只要目标系统的Nvidia驱动版本足够，那么可以向下兼容所有CUDA版本，而且不同的虚拟环境可以安装不同版本的CUDA。例如我本机的Nvidia驱动是，那么我创建的虚拟环境可以是pytorch+CUDA102,pytorch+CUDA111,paddlepaddle+CUDA112,paddlepaddle+CUDA101等等。

## 参考
[Managing channels](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html#strict-channel-priority)
