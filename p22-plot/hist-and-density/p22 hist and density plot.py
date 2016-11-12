# coding=utf-8
# -*- coding:cp936 -*-
"""
3m 2001-01-02 ~ 2011-09-30 日简单收益率
fBasics basicStats plot
"""

import rpy2.robjects as robj
from rpy2.robjects.packages import importr

importr('fBasics')

# hist plot pic 1-11
rstr1 = """
da <- read.table('d-mmm-0111.txt', header=T)

# obtain 3m simple returns
mmm <- da[, 2]

# histogram
hist(mmm, nclass=30)
"""
robj.r(rstr1)


rstr2 = """
# obtain density estimate
d1 <- density(mmm)
"""
print(robj.r(rstr2))


rstr3 = """
range(mmm)
"""
print(robj.r(rstr3))


# density plot pic 1-12
rstr4 = """
x <- seq(-0.1, 0.1, 0.001)

# creates normal density
y1 <- dnorm(x, mean(mmm), stdev(mmm))

plot(d1$x, d1$y, xlab='rtn', ylab='density', type='l')
lines(x, y1, lty=2)
"""
print(robj.r(rstr4))




