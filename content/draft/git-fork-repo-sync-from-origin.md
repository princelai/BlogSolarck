---
title: "Git Fork Repo Sync From Origin"
date: 2021-09-24T17:53:26+08:00
draft: true
isCJKLanguage: true
toc: true
categories:
- 电脑与网络
tags:
- git
- hugo
---

# 问题——git子模块更新问题
最近正在将博客从pelican迁移到Hugo，最终选择了主题[even](https://github.com/olOwOlo/hugo-theme-even)，为了管理方便和规范，我选择了submodule模式clone该项目。在将原作者主题项目添加到本地项目后，才发现别人的项目无法修改提交，于是我fork原作后重新添加，现在修改是可以了，但新的问题是我如何能和原作保持同步更新呢？

# 设置upstream
在经过一番搜索和学习之后，找到了解决办法，将子模块设置一个新的上游，然后fetch、merge后就可以了，非常简单，代码如下：

```bash
# 这里最好设置https地址，而不是ssh地址，原因是vercel这类平台在拉submodule的时候不支持
git remote add upstream https://github.com/olOwOlo/hugo-theme-even.git

# 从上游拉取新代码
git fetch upstream

# 从上游master分支合并到本地
git merge upstream/master
```

最后两步的fetch和merge可以合并为一个pull命令
```bash
# 从上游master分支合并到本地
git pull upstream master
```

# 参考
1. [How do I update or sync a forked repository on GitHub?](https://stackoverflow.com/questions/7244321/how-do-i-update-or-sync-a-forked-repository-on-github)
2. [同步复刻](https://docs.github.com/cn/github/collaborating-with-pull-requests/working-with-forks/syncing-a-fork)
