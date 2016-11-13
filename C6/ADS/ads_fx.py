# coding=utf-8
# -*- coding:cp936 -*-
import rpy2.robjects as robj
from rpy2.robjects import pandas2ri
import pandas as pd
import numpy as np
from pandas.tseries.offsets import Micro


pandas2ri.activate()

file = '/home/lin/ggprice/16-11-11 16:29:10.csv'


def get_ts(_file, _s):

    _df = pd.read_csv(_file, names=['date', 'EURUSD', 'EURJPY', 'EURAUD', 'USDJPY']).dropna()
    
    del _df['EURJPY'], _df['EURAUD'], _df['USDJPY']
    
    _df['EURUSD'] = _df['EURUSD'].apply(lambda x: x.split(':')[1])
    # delete row with ''
    _df = _df.drop(_df.ix[_df.EURUSD == ''].index)
    _df['EURUSD'] = _df['EURUSD'].astype(float)
    
    _df['time'] = pd.DatetimeIndex(_df['date'].apply(lambda x: x.split('.')[0]))
    _df['micros'] = _df['date'].apply(lambda x: x.split('.')[1]).astype(int) + 1
    _df['micros'] = _df['micros'].apply(lambda _x: Micro(_x))
    _df.index = _df['time'] + _df['micros']  # index as Datetime
    
    del _df['date']
    del _df['time']
    del _df['micros']

    # pandas.core.frame.DataFrame
    _ts = pd.DataFrame(_df['EURUSD'].resample(_s).bfill())
    _ts['change'] = _ts['EURUSD'] - _ts['EURUSD'].shift()

    _ts['A'] = 1
    _ts.loc[_ts.change == 0, 'A'] = 0

    _ts['D'] = 0
    _ts.loc[_ts.change > 0, 'D'] = 1
    _ts.loc[_ts.change < 0, 'D'] = -1

    _ts['A_lag1'] = _ts['A'].shift(1)  # 'A': Ai; 'A_lag1': Aim1
    _ts['D_lag1'] = _ts['D'].shift(1)  # 'D': Di; 'D_lag1': Dim1
    
    return _ts.dropna()


def get_prob(_ts):
    f1 = """
    function(y, x){
        glm(y ~ x, family='binomial')
    }
    """
    rf1 = robj.r(f1)

    # model for A
    m1 = rf1(_ts.dropna()['A'].values, _ts.dropna()['A_lag1'].values)
    beta0 = m1[0][0]
    beta1 = m1[0][1]

    # model for D
    di = _ts.dropna()['D'][_ts.A == 1]
    di = (di + abs(di)) / 2  # transform di to binary
    m2 = rf1(di.values, _ts.dropna()['D_lag1'][_ts.A == 1].values)
    r0 = m2[0][0]
    r1 = m2[0][1]

    def ads(_var0, _var1, _v_prev):
        _result = _var0 + _var1 * _v_prev
        return np.exp(_result) / (1 + np.exp(_result))

    a_latest = _ts.tail(1)['A'].values[0]
    d_latest = _ts.tail(1)['D'].values[0]

    # p 价格有变化的概率 （按最后价格条件和参数计算出的条件概率）
    p = ads(beta0, beta1, a_latest)
    # g 确定价格有变化后，价格上升的概率 （按最后价格条件和参数计算出的条件概率）
    g = ads(r0, r1, d_latest)

    # 无价格变化概率 （条件概率）
    hold = 1 - p
    # 价格上升概率 （条件概率）
    up = p * g
    # 价格下降概率 （条件概率）
    down = p * (1 - g)
    # 忽略价格无变化概率， 计算上 up/(up+down) 下 down/(up+down) 概率
    return hold, up, down, up/(up+down), down/(up+down)


ts = get_ts(file, '30S')


range_tick = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60]

for _range in range_tick:
    print(_range)

    ts['p_hold'] = 0
    ts['p_up'] = 0
    ts['p_down'] = 0
    ts['p_ig_up'] = 0
    ts['p_ig_down'] = 0

    pred_length = _range
    for _i in range(600):

        _r = get_prob(ts.ix[_i: pred_length+_i])

        ts.loc[ts.index[_i + pred_length], 'p_hold'] = _r[0]
        ts.loc[ts.index[_i + pred_length], 'p_up'] = _r[1]
        ts.loc[ts.index[_i + pred_length], 'p_down'] = _r[2]
        ts.loc[ts.index[_i + pred_length], 'p_ig_up'] = _r[3]
        ts.loc[ts.index[_i + pred_length], 'p_ig_down'] = _r[4]

    print('finished !!!')

    up_up = len(ts.ix[(ts.p_up > 0.5) & (ts.D == 1)])
    up_hold = len(ts.ix[(ts.p_up > 0.5) & (ts.D == 0)])
    up_down = len(ts.ix[(ts.p_up > 0.5) & (ts.D == -1)])

    print('range:', _range)
    print(up_up, up_hold, up_down, len(ts.ix[ts.p_ig_up != 0]))
