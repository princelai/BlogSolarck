---
title: 计算路线的相似度
date: 2020-03-20T18:05:11+08:00
draft: true
isCJKLanguage: true
toc: false
categories:
- 机器学习和算法
tags:
- 
---




从高德提供的结构[高德地理/逆地理编码](https://lbs.amap.com/api/webservice/guide/api/georegeo)中，我可以轻松获取城市的GPS坐标，比如下面分别是武汉、广州、上海、北京、杭州和西安六个城市的市政府坐标。

> wh = **"114.305214,30.592934"**,
>
> gz = **"113.264219,23.129571"**,
>
> sh = **"121.473657,31.230378"**,
>
> bj = **"116.407417,39.904172"**,
>
> hz = **"120.209947,30.245853"**,
>
> xa = **"108.939992,34.341703"**

<br />

我用六个城市定义三条线路，分别是武汉——广州、上海——北京、杭州——西安。一条线路是要区分起点和终点的，起始点倒转过来被认为是不同的线路。我把这三条线路每一条都放在一个二维数组中，横向第一维是起点，横向第二维是终点，每个坐标是按照[经度，维度]这个顺序放置的。

```python
wh_gz = np.array([[114.305214,30.592934],[113.264219,23.129571]])
sh_bj = np.array([[121.473657,31.230378],[116.407417,39.904172]])
hz_xa = np.array([[120.209947,30.245853],[108.939992,34.341703]])
```

要对比线路，使用GPS坐标是不行的，我需要把两条线路转换为模向量，以上海——北京和武汉——广州这两条线路为例



```
plt.hlines(0,-5,5)
plt.vlines(0,-5,5)
plt.plot([0,3],[0,1])
```



```python
@njit
def calc_path_angle(path1, path2):
    """
    path format would be np.array or list like [start gps, end gps],
    this mean compltet format like [[start lng, start lat],[end lng, eng lat]]
    :param path1:
    :param path2:
    :return:
    """

    if path1.ndim == path2.ndim == 2:
        va, vb = path1[0] - path1[1], path2[0] - path2[1]
        return np.sum(va * vb) / (np.sqrt(np.sum(va ** 2)) * np.sqrt(np.sum(vb ** 2)))
    else:
        return np.nan


def calc_path_angle2(path1, path2):
    """
    path format would be np.array or list like [start gps, end gps],
    this mean compltet format like [[start lng, start lat],[end lng, eng lat]]
    :param path1:
    :param path2:
    :return:
    """

    if path1.ndim == path2.ndim == 2:
        va, vb = path1[0] - path1[1], path2[0] - path2[1]
        return np.mat(va) * np.mat(vb).T / (np.linalg.norm(va) * np.linalg.norm(vb))
    else:
        return np.nan
```



$$a=[x_a,y_a],b=[x_b,y_b]$$

$$cos\theta = \frac{x_ax_b + y_ay_b}{\sqrt{x_a^2 + y_a^2} \times \sqrt{x_b^2 + y_b^2}}$$