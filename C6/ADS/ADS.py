import rpy2.robjects as robj

r1 = """
da<-read.table('taq-cat-cpch-jan042010.txt')
pch<-da[,2]
idx<-c(1:37715)[pch>0]
jdx<-c(1:37715)[pch<0]
A<-rep(0,37715)
A[idx]=1
A[jdx]=1
D<-rep(0,37715)
D[idx]=1
D[jdx]=-1
S<-abs(da[,1]-4)
Ai<-A[2:37715]
Aim1<-A[1:37714]
Di<-D[2:37715]
Dim1<-D[1:37714]
Si<-S[2:37715]
Sim1<-S[1:37714]
m1<-glm(Ai~Aim1, family = 'binomial')
summary(m1)
"""
print(robj.r(r1))


r2 = """
di<-Di[Ai==1]
dim1<-Dim1[Ai==1]
di<-(di+abs(di))/2
m2<-glm(di~dim1, family = 'binomial')
summary(m2)
"""
print(robj.r(r2))


r3 = """
si<-Si[Di==1]
sim1<-Sim1[Di==1]
source("GeoSize.R")
m3<-GeoSize(si,sim1)
"""
print(robj.r(r3))


r4 = """
nsi<-Si[Di==-1]
nsim1=Sim1[Di==-1]
m4=GeoSize(nsi,nsim1)
"""
print(robj.r(r4))
