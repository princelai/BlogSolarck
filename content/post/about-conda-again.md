---
title: "再谈Anaconda的使用"
date: 2021-09-27T15:40:13+08:00
draft: false
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
一直以来我都是使用virtualenv来管理Python版本，并且写了一个脚本程序用来更新三方包和解决依赖问题，只能说是能用够用，但是并不好用。而我一直没有选择用Conda来管理Python虚拟环境，是由于早期使用的时候没有深入了解，包管理给我的第一印象一样是不智能，比如我使用conda-forge环境安装了一些包和一些依赖，下次update整体虚拟环境的时候Conda就给我全部使用default频道并降级版本，这哪里是升级，明明是降级啊。究其原因就是channels设置的不对，通过这段时间的使用和了解，说说我认为的用Conda创建Python虚拟环境的优点：

- 支持多环境不同Python版本
- 支持不同CUDA版本的GPU环境
- 自动解决安装、升级和卸载的依赖关系
-  兼容pip,自带的虚拟环境备份恢复套件也很好用


以上优点让我彻底抛弃pip+virtualenv的原生环境，解决了我之前日常使用99%的问题或不便，不过想要好用前提还是要先配置正确，下面贴出我的`.condarc`配置文件一一解释：

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


> `channels`:这也是最重要的一个设置，包管理器就是按照这里的顺序从上到下搜索排序包，例如我喜欢用conda-forge这个channel，那我就把他放到第一位，这样只要是能够搜索到的都优先使用这里的包。

这样设置完，每次安装和更新的时候，都会优先从conda-forge这个channel安装，如果没有再从下面的其他channel搜索。还有一个要注意的点是我并没有把pytorch加入到channels里，所以当我想安装GPU版本的pytorch时，包管理器是找不到结果的，因为这部分我想自己手动，所以安装的时候都要加上`-c pytorch`选项。

<br>

## 备份和恢复环境

### pip
使用传统的pip进行备份和恢复，这里使用`pip list`而不是`pip freeze`是因为conda和pip版本号兼容性问题，下面这种方法输出的格式兼容性更好。
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

<br>

## 依赖关系
### conda-tree
conda-tree是一个树状依赖查看工具，功能强大，使用方便。最大的好处是在一个环境里安装了就可以查看其他conda环境的依赖关系，不需要每个环境都安装一遍才能使用。这里只记录一些我常用的命令：

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

#### conda-tree示例
```
$ conda-tree depends -t sqlite --small

sqlite==3.36.0
  ├─ libgcc-ng 11.2.0 [required: >=9.4.0]
  │  ├─ _libgcc_mutex 0.1 [required: 0.1, conda_forge]
  │  └─ _openmp_mutex 4.5 [required: >=4.5]
  │     ├─ _libgcc_mutex 0.1 [required: 0.1, conda_forge]
  │     └─ libgomp 11.2.0 [required: >=7.5.0]
  │        └─ _libgcc_mutex 0.1 [required: 0.1, conda_forge]
  ├─ ncurses 6.2 [required: >=6.2,<6.3.0a0]
  │  └─ libgcc-ng 11.2.0 [required: >=7.5.0]
  │     └─ dependencies of libgcc-ng displayed above
  ├─ readline 8.1 [required: >=8.1,<9.0a0]
  │  ├─ libgcc-ng 11.2.0 [required: >=9.3.0]
  │  │  └─ dependencies of libgcc-ng displayed above
  │  └─ ncurses 6.2 [required: >=6.2,<6.3.0a0]
  │     └─ dependencies of ncurses displayed above
  └─ zlib 1.2.11 [required: >=1.2.11,<1.3.0a0]
     └─ libgcc-ng 11.2.0 [required: >=7.5.0]
        └─ dependencies of libgcc-ng displayed above
```

<br>

当然也可以将树状依赖关系转换成dot格式，最终输出为PDF、SVG或PNG，方便查看。dot转换需要安装graphviz软件，这部分需要自行安装。

```bash
conda-tree -n <env_name> deptree --dot > file.dot # <env_name>环境全部依赖关系
conda-tree depends <package> --dot > file.dot # <package>依赖的包
conda-tree whoneeds <package> --dot > file.dot # 依赖<package>的包
```
```bash
dot -Tpng file.dot -o tree.png
```
或
```bash
dot -Tpdf file.dot -o tree.pdf
```

#### 依赖图展示
![seaborn depends tree](https://chenwrt.com:843/uploads/medium/9c775c05f6c21c1a26d34c4988484d51.png)

### pipdeptree

```bash
pipdeptree -p <package>
pipdeptree -p <package> -r
```
#### pipdeptree示例
```
$ pipdeptree -p numpy -r 

Warning!!! Possibly conflicting dependencies found:
* pylint==2.10.2
 - mccabe [required: >=0.6,<0.7, installed: ?]
------------------------------------------------------------------------
numpy==1.20.3
  - matplotlib==3.4.3 [requires: numpy>=1.16]
  - numba==0.54.0 [requires: numpy>=1.17,<1.21]
  - pandas==1.3.3 [requires: numpy>=1.17.3]
  - scikit-learn==1.0 [requires: numpy>=1.14.6]
  - scipy==1.7.1 [requires: numpy>=1.16.5,<1.23.0]
    - scikit-learn==1.0 [requires: scipy>=1.1.0]

```
最主要的命令就上面两个，其他的功能如freeze、dot可以去[项目主页](https://github.com/naiquevin/pipdeptree)查询。pipdeptree没有依赖，输出美观，作为纯pip环境还是不错的，Conda环境建议还是用conda-tree。

<br>

## GPU环境
现在深度学习在Python上越来越普遍，安装带CUDA的Python虚拟环境也是必备技能，用Conda创建虚拟环境可以把准备环境的工作大大简化。只需要通过命令

```bash
conda create -n torch1 python=3.8
conda activate torch1
conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
```
或者
```bash
conda create -n torch2 python=3.9
conda activate torch2
conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia
```
就能创建一个pytorch环境，无需考虑本机CUDA版本。

Conda创建CUDA环境的好处是只要目标系统的Nvidia驱动版本足够，那么可以向下兼容所有CUDA版本，而且不同的虚拟环境可以安装不同版本的CUDA。例如我本机的Nvidia驱动版本是450.80.02，那么我创建的虚拟环境可以是：

- pytorch+CUDA102,
- pytorch+CUDA111,
- paddlepaddle+CUDA112,
- paddlepaddle+CUDA101

或者同时安装这四个环境也没有问题。详细的CUDA版本与Nvidia驱动匹配表可以在[英伟达网站](https://docs.nvidia.com/deploy/cuda-compatibility/index.html#deployment-consideration-forward)找到。

## 参考
[Managing channels](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html#strict-channel-priority)
