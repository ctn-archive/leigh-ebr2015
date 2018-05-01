#computes the mean and 95% confidence interval

from numpy import *
from matplotlib import *
import matplotlib.pyplot as plt
from pylab import *
import os
import math


def stripCommas (stringArray):
	result=[]
	for i in stringArray:
		result.append(i.strip(','))
	return result

def toFloats (stringArray):
	result=[]
	for i in stringArray:
		result.append(float(i.strip(',')))
	return result


#read in data from csv file.  The csv file is created using combine.py (or subsample.py)
def readcsvFile(path):
	f=open(path)

	#row=f.readline()
	#headers=stripCommas(row.split())

	data=[]
	while True:
		row=f.readline()
		if row=='':
			break
		data.append(toFloats(row.split(',')))
	return array(data)


fig = plt.figure(figsize=(16,5))
fig.suptitle('Bisection Error vs. Line Length',fontsize=20)


scale=1.5

ax = fig.add_subplot(1,2,1)
ax.errorbar((102,77,51,25),(0.42,0.33,0.12,0.06),yerr=(2.8,2.0,1.3,0.8),color='k',linestyle='-')
y=(20*scale,40*scale,60*scale)
x=(-0.061227*scale,0.039220*scale,-0.055156*scale)  #40 neurons per pixel, 60 pixels, training tau=1, 0 damage
e=(0.343327*scale,0.489566*scale,0.781549*scale)
#x=(0.067395*scale,0.187258*scale,0.144473*scale)  #20 neurons per pixel, 60 pixels, training tau=1, 0 damage
#e=(0.390356*scale,0.443837*scale,0.660560*scale)

ax.errorbar(y,x,yerr=e,color='k',linestyle='--')
ax.set_title('Normal',fontsize=18)
ax.set_position((.1,0.12,.4,.75))
xlabel('Line Length [mm]',fontsize=16)
ylabel('Error [mm]',fontsize=16)
#xlim(0,105)
#ylim(-1.4,0.6)
#lgd=legend(('Human','Simulation'),2)
#lgd.get_lines()[0].set_ls('-')
#lgd.get_lines()[1].set_ls('--')
axhline(y=0,color=('0.8'))







ax = fig.add_subplot(1,2,2)
ax.errorbar((102,77,51,25),(15.21,9.5,3.95,-0.45),yerr=(11.45,7.34,3.63,2.24),color='k',linestyle='-')
#y=(22,50,78)
x=(1.026433*scale,2.053506*scale,3.369108*scale)
e=(2.174265*scale,4.015544*scale,5.478798*scale)
ax.errorbar(y,x,yerr=e,color='k',linestyle='--')
ax.set_title('Neglect',fontsize=18)
ax.set_position((.55,0.12,.4,.75))
xlabel('Line Length [mm]',fontsize=16)
ylabel('Error [mm]',fontsize=16)
#xlim(0,105)
#ylim(-1.4,0.6)
#lgd=legend(('Human','Simulation'),2)
#lgd.get_lines()[0].set_ls('-')
#lgd.get_lines()[1].set_ls('--')
axhline(y=0,color=('0.8'))




plt.show()




