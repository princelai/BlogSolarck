---
title: Python中多项式拟合及外推方法
date: 2021-09-06T17:27:11+08:00
draft: false
isCJKLanguage: true
toc: false
categories:
- 机器学习和算法
tags:
- python
- numpy
- scipy
---

曲线拟合是我常用的工具之一，当数据是简单序列数据时，没有必要使用机器学习和深度学习方法，幸好`numpy`和`scipy`都提供了相关的函数可以简单快速调用，下面就是我对两种方法使用记录。

</p>

首先创造一组我要用到的简单序列，该序列是一组指数近7天的值，我最终要得到的结果是根据已有的7个值的趋势，预测下一个值。

```python
import pandas as pd

ser = pd.Series([0.911,0.824,0.829,0.825,0.81,0.816,0.84])
```

| 索引序号 | 值    |
| -------- | ----- |
| 1        | 0.911 |
| 2        | 0.824 |
| 3        | 0.829 |
| 4        | 0.825 |
| 5        | 0.81  |
| 6        | 0.816 |
| 7        | 0.84  |

</p>

## 使用polyfit拟合

```python
import numpy as np

z = np.polyfit(range(1, ser.size + 1), ser, 2)
p = np.poly1d(z)
```

上面这段代码就是拟合的全部，先是使用`polyfit`进行多项式拟合，多项式的最高次为2,即拟合$y=ax^2+bx+c$这个多项式，返回值为全部多项式的系数，也就是前面多项式中的`a,b,c`三项。

而`poly1d`则是一个封装函数，用来方便使用多项式拟合，例如我上面得到$z = [0.8,-2.5,1.7]$，那么p就相当于自动将系数代入后的函数$p(x) = 0.8x^2-2.5x+1.7$

外推出趋势的下一个值可以使用

```python
p(ser.size + 1)
```



</p>

## 使用curve_fit拟合

当你想自定义多项式时，上面的方法就不太适用，不过`scipy`也提供了相应的方法，首先是要自定义多项式函数：

```python
def poly_fit(x, a, b, c, d, e):
    y = a * np.log(x) + b / x + c * x ** 2 + d * x + e
    return y
```

上面我自定义的多项式函数在二次多项式基础上增加$\log(x)$和$\frac{1}{x}$这两项，共计5个拟合参数。



</p>

调用`curve_fit`方法

```python
from scipy.optimize import curve_fit

popt, pcov = curve_fit(poly_fit, np.arange(1, ser.size + 1), ser)
```

`popt`就是我需要的系数数组

外推下一个预测值方法和上面的类似

```pyhton
poly_fit(ser.size + 1,*popt)
```



## 画图

最后可以将结果画出来验证

```python
plt.plot(ser, label='raw')
plt.plot(p(np.arange(1, ser.size + 2)), linestyle='-.', label='pf')
plt.plot(poly_fit(np.arange(1, ser.size + 2), *popt), linestyle='--', label='cf')
plt.legend(loc='upper center')
plt.show()
```

![Figure_1.png](https://chenwrt.com:843/uploads/big/db7f07f07638a72edd114bdff7db281d.jpg)
