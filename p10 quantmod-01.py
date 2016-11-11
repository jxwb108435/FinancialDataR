# coding=utf-8
# -*- coding:cp936 -*-

import rpy2.robjects as robj
from rpy2.robjects.packages import importr

# create an R function
importr('quantmod')

rstring = """
getSymbols('AAPL', from='2005-01-02', to='2010-10-31')
chartSeries(AAPL, theme='white')
"""

robj.r(rstring)
