---
title: "Python脚本性能分析工具的介绍"
date: 2021-09-24T17:20:13+08:00
draft: true
isCJKLanguage: true
toc: true
categories:
- 编程
tags:
- python
---





## 获取数据

由于我有自己的股票数据库，直接从库里提取出单支股票数据，这里用的是601519大智慧，数据总共1813行，43列。查看数据格式：

`df.tail()`

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ts_code</th>
      <th>open</th>
      <th>high</th>
      <th>……</th>
      <th>ret_std</th>
      <th>ADJ_DIFF12</th>
      <th>ADJ_DIFF23</th>
    </tr>
    <tr>
      <th>trade_date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-05-15</th>
      <td>601519.SH</td>
      <td>7.28</td>
      <td>7.37</td>
       <th>……</th>
      <td>7.345512</td>
      <td>-2.356491</td>
      <td>0.036250</td>
    </tr>
    <tr>
      <th>2019-05-16</th>
      <td>601519.SH</td>
      <td>7.00</td>
      <td>7.04</td>
       <th>……</th>
      <td>6.909756</td>
      <td>-2.766857</td>
      <td>-0.178900</td>
    </tr>
    <tr>
      <th>2019-05-17</th>
      <td>601519.SH</td>
      <td>6.87</td>
      <td>7.18</td>
       <th>……</th>
      <td>6.405541</td>
      <td>-3.266414</td>
      <td>-0.405331</td>
    </tr>
    <tr>
      <th>2019-05-20</th>
      <td>601519.SH</td>
      <td>6.70</td>
      <td>6.74</td>
       <th>……</th>
      <td>5.760118</td>
      <td>-3.961804</td>
      <td>-0.654204</td>
    </tr>
    <tr>
      <th>2019-05-21</th>
      <td>601519.SH</td>
      <td>6.31</td>
      <td>7.00</td>
       <th>……</th>
      <td>6.736810</td>
      <td>-3.597550</td>
      <td>-0.696689</td>
    </tr>
  </tbody>
</table>



## 测试函数

### Pandas版本

```python
def detonate(window, df):
    error_ret = 0.7 if window < 20 else 0.12
    onelimitup = df.loc[df.low == df.high].index
    maxidx = df.index.size - window
    result = []
    for i in range(0, maxidx, max(2, window // 10)):
        data = df.close.iloc[i:i + window]
        ret = data.pct_change()
        if any(ret > error_ret):
            continue
        pct = (data.iloc[-1] - data) / data
        if not any(pct >= 1.0):
            continue
        sqrt_day = np.sqrt((data.index[-1] - data.index).days + 1)
        value = pct[:-1] / sqrt_day[:-1]
        value = value.loc[~value.index.isin(onelimitup)]
        if value.empty or (value.max() < 0.1):
            continue
        detonate_date = value.idxmax()
        max_ret = pct.loc[detonate_date]
        max_value = value.loc[detonate_date]
        result.append([detonate_date, max_ret, max_value])
    if len(result) == 0:
        return None
    result_df = pd.DataFrame(result)
    result_df.columns = ['trade_date', 'window_return', 'value_rate']
    # 同日合并取最大
    result_df = result_df.groupby('trade_date').max()
    result_df['ts_code'] = df.ts_code.iloc[-1]
    result_df.set_index(['ts_code', result_df.index], inplace=True)
    result_df = result_df.sort_values('value_rate', ascending=False).iloc[:10]
    return result_df.where(result_df.window_return >= 1.0).dropna()
```



### Numpy版本

```python
def detonate2(window, index, close, low, high):
    error_ret = 0.7 if window < 20 else 0.12
    onelimitup = index[low == high]
    maxidx = index.size - window
    result = np.zeros((30, 3))
    ri = 0
    for i in range(0, maxidx, max(2, window // 5)):
        _close = close[i:i + window]
        _index = index[i:i + window]
        ret = (_close[1:] - _close[:-1]) / _close[:-1]
        if np.any(ret > error_ret):
            continue
        pct = (_close[-1] - _close) / _close
        if not np.any(pct >= 1.0):
            continue
        sqrt_day = np.sqrt((_index[-1] - _index).astype('timedelta64[D]').astype(int) + 1)
        value = pct / sqrt_day
        value = np.where(np.array([i not in onelimitup for i in _index]), value, 0)
        if value.max() < 0.1:
            continue
        detonate_date = _index[value.argmax()]
        max_ret = pct[value.argmax()]
        max_value = value.max()
        result[ri] = np.array([detonate_date, max_ret, max_value])
        ri += 1
        if ri >= 30:
            return result
    return result


def numpy_detonate(df):
    t = detonate2(20, df.index.values, df.close.values, df.low.values, df.high.values)
    result_df = pd.DataFrame(t[t[:, 0] > 0])
    result_df.columns = ['trade_date', 'window_return', 'value_rate']
    result_df['trade_date'] = pd.to_datetime(result_df.trade_date)
    result_df = result_df.groupby('trade_date').max()
    result_df['ts_code'] = df.ts_code.iloc[-1]
    result_df.set_index(['ts_code', result_df.index], inplace=True)
    result_df = result_df.sort_values('value_rate', ascending=False).iloc[:10]
    return result_df.where(result_df.window_return >= 1.0).dropna()
```



## 性能测试

### timeit

如果你使用的是ipython，那么自带的`%timeit`魔术方法就是最简单最直接的一种性能分析方式

```python
%timeit detonate(20, df.loc[:, ['ts_code', 'low', 'high', 'close']])
1.46 s ± 11.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit numpy_detonate(df)
17.7 ms ± 225 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```



### line_profiler



### vprof