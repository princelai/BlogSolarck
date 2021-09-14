---
title: Python协程中的设计模式
date: 2021-09-14T16:56:11+08:00
draft: false
isCJKLanguage: true
toc: false
categories:
- 编程
tags:
- python
- asyncio
---


最近写代码需要用到协程相关内容，遂深入研究了下学到不少知识，记录下来希望能帮到需要的你，下面就是我逐步探索的过程。

</p>

## 起因——有问题的代码

假设我现在要写一个爬虫获取一些数据，我希望使用到协程加快速度，于是我写了如下代码：

```python
import asyncio
from itertools import cycle
import random


async def crawler(w):
    t = random.random() * 5
    print(f"Worker-{w} wait {t:.2f} second to responed")
    await asyncio.sleep(t)
    return t


async def worker(url, w):
    print(f"Worker-{w} crawling {url}")
    r = await crawler(w)
    return r


async def main():
    url = [f"url{i}" for i in range(50)]
    tasks = [worker(u, i) for u, i in zip(url, cycle([1, 2, 3, 4]))]
    gather = await asyncio.gather(*tasks)
    return gather


if __name__ == "__main__":
    result = asyncio.run(main())
```

上面的代码第20行从本地生成url，这里假设我要爬取的链接都是有规律的，可以本地生成

第21行开了4个协程创建任务，第22行将这些任务一股脑全部运行。众所周知，网站都是有反扒的，短时间内大量访问必定会被ban IP,设置了sleep也是没有用的，因为所有任务都是同时开始，所以现在的问题就是如何限制速度？

</p>

## 使用第三方库

Python第三方资源非常多，我这里只是抛砖引玉选择其中一个叫做`paco`的包

```python
import asyncio
import random
import re

import paco


async def crawler(u):
    i = int(re.search(r"\d+", u).group(0))
    await asyncio.sleep(random.random() * 3)
    print(f"crawled {u}")
    return i


async def main():
    urls = [f"url{i}" for i in range(100)]
    gather = await paco.map(crawler, urls, limit=10)
    return gather


if __name__ == "__main__":
    result = asyncio.run(main())
```

代码变动不大，`limit`参数可以限制总的并发数量，然后在每个爬虫里设置sleep，基本达到目的。但如果不想或不能使用外部库，非要用内置怎么完成呢？

</p>



## 信号量

信号量就是一把自带的协程锁，和上面`limit`达到基本一致的目的，修改起来也很简单

```python
import asyncio
import random
import re


async def crawler(u, sem):
    async with sem:
        i = int(re.search(r"\d+", u).group(0))
        await asyncio.sleep(random.random() * 5)
        print(f"crawled {u}")
    return i


async def main():
    sem = asyncio.Semaphore(10)
    urls = [f"url{i}" for i in range(100)]
    tasks = [crawler(u, sem) for u in urls]
    gather = await asyncio.gather(*tasks)
    return gather


if __name__ == "__main__":
    result = asyncio.run(main())
```

在创建`crawler`任务的的时候，将全局或局部信号量传入进去，在爬虫内部使用`async with`创建上下文，当总协程量达到设定的上限时，其余并发的任务都会卡在这里，等某个锁释放后，其余任务会争抢这把锁并继续上锁，如此持续。

