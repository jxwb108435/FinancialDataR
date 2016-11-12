# coding=utf-8
# -*- coding:cp936 -*-

import rpy2.robjects as robj

# pic 1-15
rstr1 = """
da <- read.table('m-ibmsp-2611.txt', header=T)
ibm <- log(da$ibm + 1)
sp <- log(da$sp + 1)

# create time index
tdx <- c(1:nrow(da))/12 + 1926

par(mfcol=c(2,1))

plot(tdx, ibm, xlab='year', ylab='lrtn', type='l')
title(main='(a) IBM returns')

plot(tdx, sp, xlab='year', ylab='lrtn', type='l')
title(main='(b) SP index')
"""
robj.r(rstr1)


# correlation
rstr2 = """
cor(ibm, sp)
"""
print(robj.r(rstr2))


# fit Market Model(linear model)
rstr3 = """
m1 <- lm(ibm ~ sp)
summary(m1)
"""
print(robj.r(rstr3))


# scatter plot  pic 1-16
rstr4 = """
par(mfcol=c(1,1))

# scatter
plot(sp, ibm, cex=0.8)

# linear regression line
abline(0.008, 0.807)
"""
print(robj.r(rstr4))
