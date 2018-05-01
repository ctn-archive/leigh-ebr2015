from numpy import *
from matplotlib import *
import matplotlib.pyplot as plt
from pylab import *
import matplotlib.font_manager


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


#read in data from csv file.  The csv file is created using combine.py
def readcsvFile(path):
	f=open(path)

	row=f.readline()
	headers=stripCommas(row.split())

	data=[]
	while True:
		row=f.readline()
		if row=='':
			break
		data.append(toFloats(row.split(',')))
	return array(data)


data=readcsvFile('/home/sleigh/Dropbox/Research/Paper/Simulation Data/Spiking Data/Best Data/Normal_adapt_rate:2e-10_subsampled2/Simulation 6h58m19s 7M25D/data.csv')


fig = plt.figure(figsize=(16,5))
fig.suptitle('Prism Adaptation Simulations: Line Bisection Motor Error',fontsize=20)
ax = fig.add_subplot(1,2,1)
ax.plot(data[:,0],data[:,5],'k')
ax.plot(data[:,0],data[:,3],'k--')
ax.set_title('Normal',fontsize=18)
ax.set_position((.1,0.1,.4,.75))
xlabel('Time [s]',fontsize=16)
ylabel('[pixels]',fontsize=16)
ylim(-10,11)

#print average(data[250:300,6])
#print average(data[1750:1800,6])

data=readcsvFile('/home/sleigh/Dropbox/Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled/Simulation 14h27m14s 7M24D/data.csv')

ax = fig.add_subplot(1,2,2)
ax.plot(data[:,0],data[:,5],'k')
ax.plot(data[:,0],data[:,3],'k--')
ax.set_title('Neglect',fontsize=18)
ax.set_position((.55,0.1,.4,.75))
xlabel('Time [s]',fontsize=16)
ylabel('[pixels]',fontsize=16)
ylim(-1,18)
ax.legend(('Motor Error','Prism Shift'))
prop = matplotlib.font_manager.FontProperties(size=5) 
ax.legend(prop=prop) 


#print average(data[250:300,6])
#print average(data[1750:1800,6])
#print average(data[850:900,6])

plt.show()

