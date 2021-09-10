---
title: 微博图床禁止外链？不存在的！
date: 2019-05-22T18:20:11+08:00
draft: false
isCJKLanguage: true
categories:
- 计算机
tags:
- 图床
---


微博图床使用的是最基本的限制第三方引用策略，这个问题倒是很好解决，

编辑pelican`themes/你的主题/templates/base.html`，在两个`<head>`标签之间插入

```html
<meta name="referrer" content="no-referrer" />
```

这样就禁止网页的引用信息，从而让微博无法拿到这个字段，但目前已知的问题是某些流量统计、方可追踪的脚本可能无法正常运行。



微博此举也可能只是警告一下，之后会不会再次加强限制不得而知，所以上上策还是赶紧备份图片，迁移到一个便宜又靠谱的图床去。



## 参考

1. [报！微博图床挂了 ？？](<https://www.v2ex.com/t/557844>)