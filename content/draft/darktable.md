---
title: darktable中文
date: 2021-09-09T15:31:11+08:00
draft: true
isCJKLanguage: true
categories:
- 摄影
tags:
- darktable
---


## 简介
darktable是一款类似Lightroom的全平台图像编辑管理开源软件，尤其是在Linux平台（主要是没其他可选），目前是我的主要照片编辑管理软件。

不过目前官方没有自带中文语言，对于有很多专业光学词汇的软件使用起来还是有些困难，不过幸好官方同样提供了网友共同翻译的语言文件，需要简单转换后就能使用上中文版的darktable

<br>

## 获取中文mo文件
首先需要在[darktable项目主页](https://github.com/darktable-org/darktable/tree/master/po)下载你需要的语言文件，比如我需要简体中文对应的文件就是zh_CN.po

```bash
wget -o zh_CN.po https://raw.githubusercontent.com/darktable-org/darktable/master/po/zh_CN.po
```

<br>

## 转换
使用系统自带的msgfmt命令（由gettext包提供）就可以将po文件转换为系统可使用的二进制mo文件
```bash
msgfmt -o darktable.mo zh_CN.po
```

<br>

## 移动到相应位置
得到mo文件需要将其移动（复制）到darktable能识别的位置就大功告成
```bash
sudo cp darktable.mo /usr/share/locale/zh_CN/LC_MESSAGES
```

根据我一个月的使用情况来看，安装了中文补丁后，在快速切换某些界面时候会卡住几秒然后自动退出，不过幸好编辑图片的流程顺序参数都存储在相应的xml文件里，数据倒是不会丢失，只不过体验不太好。

<br>


## 编辑检查po文件
如果想方便的编辑、查找po文件内容，那么poedit软件是个不错的工具
```bash
yay -S poedit
```

