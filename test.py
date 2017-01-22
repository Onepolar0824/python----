# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
print('本程序由@张 三金编写\n电邮:onepolar0824@foxmail.com\nwechat:amd4000')
g=input('请输入股票代码:_')

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
df = ts.get_stock_basics()
date = df.ix[g]['timeToMarket'] #上市日期YYYYMMDD
print(date)

k=input('请输入开始日期（格式YYYY-MM-DD）:_')
q=input('请输入结束日期（格式YYYY-MM-DD）:_')

a=ts.get_k_data(g, start=k, end=q) #两个日期之间的前复权数据
print(a)

#重新排序数据，由远到近，这是计算ma的第一步
a.sort('date', inplace=True)


# ========== 计算移动平均线

ma_list = [18, 34, 60]

# 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
for ma in ma_list:
    a['MA_' + str(ma)] = pd.rolling_mean(a['close'], ma)

# 计算指数平滑移动平均线EMA
for ma in ma_list:
    a['EMA_' + str(ma)] = pd.ewma(a['close'], span=ma)

# 将数据按照交易日期从近到远排序
a.sort('date', ascending=False, inplace=True)

# ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
#a.to_csv('sh600600_ma_ema.csv', index=False)

x=input('请输入均线参数'+str(ma_list))

a['PL_EMA_18']=100*(a['close']-a['EMA_'+str(x)])/a['close']

#a.to_csv('sh600600_ma_ema_PL.csv', index=False)
plt.hist(a['PL_EMA_18'],bins=600)
plt.xlabel('PL')
plt.ylabel('Times')
plt.title(g)
plt.show()
