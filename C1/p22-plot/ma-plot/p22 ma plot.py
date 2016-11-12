# coding=utf-8
# -*- coding:cp936 -*-

import rpy2.robjects as robj
from rpy2.robjects.packages import importr

importr('quantmod')

# ma plot pic 1-14
rstr1 = """
source('ma.R')
getSymbols('AAPL', from='2010-01-02', to='2011-12-08')
x1 <- as.numeric(AAPL$AAPL.Close)

ma(x1, 21)
"""
robj.r(rstr1)
