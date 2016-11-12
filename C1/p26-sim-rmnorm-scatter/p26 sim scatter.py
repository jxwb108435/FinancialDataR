# coding=utf-8
# -*- coding:cp936 -*-

import rpy2.robjects as robj
from rpy2.robjects.packages import importr

importr('mnormt')

# pic 1-18
rstr1 = """
da <- read.table('m-ibmsp-2611.txt', header=T)
ibm <- log(da$ibm + 1)
sp <- log(da$sp + 1)

# obtain bivariate returns
rt <- cbind(ibm, sp)

# sample mean
m1 <- apply(rt, 2, mean)
# sample covariance matrix
v1 <- cov(rt)

# sim
x <- rmnorm(1029, mean=m1, varcov=v1)

plot(x[,2], x[,1], xlab='sim-sp', ylab='sim-ibm', cex=0.8)
"""
robj.r(rstr1)

