# coding=utf-8
# -*- coding:cp936 -*-

import rpy2.robjects as robj
from rpy2.robjects.packages import importr

importr('quantmod')

# ohlc plot pic 1-13
rstr2 = """
getSymbols('AAPL', from='2011-01-03', to='2011-06-30')
X <- AAPL[, 1:4]
xx <- cbind(as.numeric(X[,1]), as.numeric(X[,2]), as.numeric(X[,3]), as.numeric(X[,4]))
source('ohlc.R')
ohlc_plot(xx, xl='days', yl='price', title='Apple Stock')
"""
robj.r(rstr2)
