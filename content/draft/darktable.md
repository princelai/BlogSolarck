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


## 中文

获取中文mo文件
```bash
wget -o zh_CN.po https://raw.githubusercontent.com/darktable-org/darktable/master/po/zh_CN.po
```

转换

```bash
yay -S poedit
msgfmt -o darktable.mo zh_CN.po
sudo cp darktable.mo /usr/share/locale/zh_CN/LC_MESSAGES
```

