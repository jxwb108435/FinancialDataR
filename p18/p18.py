# coding=utf-8
# -*- coding:cp936 -*-
"""
3m 2001-01-02 ~ 2011-09-30 日简单收益率
fBasics basicStats
"""

import rpy2.robjects as robj
from rpy2.robjects.packages import importr

importr('fBasics')

rstring = """
da <- read.table('d-mmm-0111.txt', header=T)

# obtain 3m simple returns
mmm <- da[, 2]

# compute summary statistics
basicStats(mmm)
"""
print(robj.r(rstring))


r_mean = """
mean(mmm)
"""
print(robj.r(r_mean))


r_var = """
var(mmm)
"""
print(robj.r(r_var))


r_stdev = """
stdev(mmm)
"""
print(robj.r(r_stdev))


r_ttest = """
t.test(mmm)
"""
print(robj.r(r_ttest))


r_t3 = """
s3 <- skewness(mmm)

# sample size
T <- length(mmm)

t3 <- s3/sqrt(6/T)
print(t3)
"""
print(robj.r(r_t3))


r_pp = """
# compute p-value
pp <- 2*(1-pnorm(t3))
print(pp)
"""
print(robj.r(r_pp))


r_t4 = """
s4 <- kurtosis(mmm)
# Kurtosis test
t4 <- s4/sqrt(24/T)
print(t4)
"""
print(robj.r(r_t4))


r_JBtest = """
# JB-test
normalTest(mmm, method='jb')
"""
print(robj.r(r_JBtest))
