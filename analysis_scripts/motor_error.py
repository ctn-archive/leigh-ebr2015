from numpy import *
from matplotlib import *
import matplotlib.pyplot as plt
from pylab import *


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

f=open('Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled/Simulation 14h27m14s 7M24D/data.csv')

row=f.readline()
headers=stripCommas(row.split())

data=[]
while True:
	row=f.readline()
	if row=='':
		break
	data.append(toFloats(row.split(',')))

datas=array(data)





fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111)
ax.plot(datas[:,0],datas[:,5],'k')
ax.plot(datas[:,0],datas[:,3],'k--')
ax.set_title('Neglect Prism Adaptation Simulation: Line Bisection Motor Error')
xlabel('Time [s]')
ylabel('[pixels]')
ax.legend(('Motor Error','Prism Shift'))
plt.show()

