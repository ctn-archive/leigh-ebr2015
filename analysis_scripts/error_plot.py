from numpy import *
from matplotlib import *
import matplotlib.pyplot as plt
from pylab import *

class Gaussian:
	def __init__ (self,mean,variance):
		self.mean=mean
		self.variance=variance
	def map (self,x):
		den=(math.sqrt(2.0*math.pi*self.variance))
		num=exp(-((x-self.mean)**2.0)/(2.0*self.variance))
		return num/den



y1=[0]*60
y2=[0]*60
y3=[0]*60
ysum=[0]*60
x=range(-30,30)

#g=Gaussian(30,30)
#for i in range(60):
#	y[i]+=g.map(i)


#right parietal, left representation
for i in range(60):
	for j in range(30):
		for k in range(10):
			g=Gaussian(j,(k+1)*3)
			y1[i]+=g.map(i)*(0.004*(i-30))
			ysum[i]+=g.map(i)*(0.004*(i-30))

#right parietal, right representation
for i in range(60):
	for j in range(30,60):
		for k in range(10):
			g=Gaussian(j,(k+1)*3)
			y1[i]+=g.map(i)*(0.004*(i-30))
			ysum[i]+=g.map(i)*(0.004*(i-30))

#left parietal, right representation
for i in range(60):
	for j in range(30,60):
		for k in range(20):
			g=Gaussian(j,(k+1)*(3.0/6.0))
			y3[i]+=g.map(i)*(0.002*(i-30))
			ysum[i]+=g.map(i)*(0.002*(i-30))



fig = plt.figure(figsize=(16,5))
fig.suptitle('Error Signal Computation',fontsize=20)
ax = fig.add_subplot(121)
ax.plot(x,y1,'k:')
ax.plot(x,y3,'k--')
ax.plot(x,ysum,'k')
ax.set_title('Normal',fontsize=18)
axhline(y=0,color=('0.8'))
axvline(x=0,color=('0.8'))
ax.set_position((.09,0.11,.4,.75))
xlim(-20,20)
ylim(-1,2)
ax.legend(('Right Parietal','Left Parietal','Total'),loc='upper left')
xlabel('Spatial Discordance',fontsize=16)
ylabel('Error Signal',fontsize=16)




y1=[0]*60
y2=[0]*60
y3=[0]*60
ysum=[0]*60

#right parietal, left representation
for i in range(60):
	for j in range(30):
		for k in range(10):
			g=Gaussian(j,(k+1)*3)
			y1[i]+=g.map(i)*(0.004*(i-30))*0.05
			ysum[i]+=g.map(i)*(0.004*(i-30))*0.05

#right parietal, right representation
for i in range(60):
	for j in range(30,60):
		for k in range(10):
			g=Gaussian(j,(k+1)*3)
			y1[i]+=g.map(i)*(0.004*(i-30))*0.05
			ysum[i]+=g.map(i)*(0.004*(i-30))*0.05

#left parietal, right representation
for i in range(60):
	for j in range(30,60):
		for k in range(20):
			g=Gaussian(j,(k+1)*(3.0/6.0))
			y3[i]+=g.map(i)*(0.002*(i-30))
			ysum[i]+=g.map(i)*(0.002*(i-30))




ax = fig.add_subplot(122)
ax.plot(x,y1,'k:')
ax.plot(x,y3,'k--')
ax.plot(x,ysum,'k')
ax.set_title('Neglect',fontsize=18)
axhline(y=0,color=('0.8'))
axvline(x=0,color=('0.8'))
ax.set_position((.56,0.11,.4,.75))
xlim(-20,20)
ylim(-1,2)
xlabel('Spatial Discordance',fontsize=16)
ylabel('Error Signal',fontsize=16)

plt.show()

