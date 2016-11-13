import rpy2.robjects as robj
from rpy2.robjects import pandas2ri
import pandas as pd
import numpy as np


pandas2ri.activate()

df = pd.read_csv('taq-cat-cpch-jan042010.txt', sep='\s+', header=None, names=['type', 'change'])

df['A'] = 1
df.loc[df.change == 0, 'A'] = 0

df['D'] = 0
df.loc[df.change > 0, 'D'] = 1
df.loc[df.change < 0, 'D'] = -1

df['S'] = abs(df['type'] - 4)

df['A_lag1'] = df['A'].shift(1)  # 'A': Ai; 'A_lag1': Aim1
df['D_lag1'] = df['D'].shift(1)  # 'D': Di; 'D_lag1': Dim1
df['S_lag1'] = df['S'].shift(1)  # 'S': Si; 'S_lag1': Sim1

f1 = """
function(y, x){
    glm(y ~ x, family='binomial')
}
"""
rf1 = robj.r(f1)

# model for A
m1 = rf1(df.dropna()['A'].values, df.dropna()['A_lag1'].values)
beta0 = m1[0][0]
beta1 = m1[0][1]


# model for D
di = df.dropna()['D'][df.A == 1]
di = (di + abs(di)) / 2  # transform di ti binary
m2 = rf1(di.values, df.dropna()['D_lag1'][df.A == 1].values)
r0 = m2[0][0]
r1 = m2[0][1]


def ads(_var0, _var1, _v_prev):
    _result = _var0 + _var1 * _v_prev
    _r = np.exp(_result) / (1 + np.exp(_result))
    return _r

a_latest = df.tail(1)['A'].values[0]
d_latest = df.tail(1)['D'].values[0]

# p 价格有变化的概率 （按最后价格条件和参数计算出的条件概率）
p = ads(beta0, beta1, a_latest)
# g 确定价格有变化后，价格上升的概率 （按最后价格条件和参数计算出的条件概率）
g = ads(beta0, beta1, d_latest)


# 无价格变化概率 （条件概率）
hold = 1 - p
print('hold:', hold)
# 价格上升概率 （条件概率）
up = p * g
print('up:', up)
# 价格下降概率 （条件概率）
down = p * (1 - g)
print('down:', down)


# 忽略价格无变化概率， 计算上下降概率
print('up_ignore_hold:', up/(up+down))
print('up_ignore_hold:', down/(up+down))
