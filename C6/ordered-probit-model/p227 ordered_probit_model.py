# coding=utf-8
# -*- coding:cp936 -*-

import rpy2.robjects as robj
from rpy2.robjects.packages import importr

importr('MASS')


rstr1 = """
da <- read.table('taq-cat-t-jan042010.txt', header=T)
da1 <- read.table('taq-cat-cpch-jan042010.txt')

vol <- da$size/100

# category of price change
cpch <- da1[, 1]

# price change
pch <- da1[, 2]

# create categories in R
cf <- as.factor(cpch)

y <- cf[4:37715]
# create indicator for lag-1 cpch
y1 <- cf[3:37714]
# create indicator for lag-2 cpch
y2 <- cf[2:37713]

vol <- vol[2:37716]
# create lag-2 volume
v2 <- vol[2:37713]

cp1 <- pch[3:37714]
cp2 <- pch[2:37713]
cp3 <- pch[1:37712]

m1 <- polr(y~v2+cp1+cp2+cp3+y1+y2, method='probit')

summary(m1)
"""
print(robj.r(rstr1))


rstr2 = """
names(m1)
"""
print(robj.r(rstr2))


rstr3 = """
yhat <- m1$fitted.values
print(yhat[1:5,], digits=3)
"""
print(robj.r(rstr3))
