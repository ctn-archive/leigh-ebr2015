#shows 2 plots comparing bisection errors vs line position for simulations of normals and patients.


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


#read in data from csv file.  The csv file is created using combine.py (or subsample.py)
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


fig = plt.figure(figsize=(16,5))
fig.suptitle('Bisection Error vs. Line Position',fontsize=20)

data=readcsvFile('/home/sleigh/Dropbox/Research/Paper/Simulation Data/Spiking Data/Normal_Line_Loc_Size/Simulation 2h9m4s 7M20D/data.csv')
linePositions=array(range(-10,11))
errors=array([0.0]*21)
for i in range(data.shape[0]):
	errors[data[i,1]+10]+=data[i,5]*1.0/31.0  #data[i,1] is the line position. data[i,5] is the motor error.  There are 21 samples at each line position.

ax3 = fig.add_subplot(1,2,1)
ax3.plot(linePositions,errors,'ko')
ax3.set_title('Normal, Simulation',fontsize=18)
ax3.set_position((.1,0.1,.4,.75))
xlabel('Line Center [pixels]',fontsize=16)
ylabel('Error [pixels]',fontsize=16)
xlim(-11,11)
ylim(-0.65,0.1)
axhline(y=0,color='k',linestyle='--')


#data=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_line_loc_size_2e-10_rate2/Simulation 16h42m47s 7M25D/data.csv')
#data=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled6/Simulation 1h48m8s 7M26D/data.csv')
#data=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled5/Simulation 23h38m16s 7M25D/data.csv')
data=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled3/Simulation 21h30m48s 7M25D/data.csv')
linePositions=array(range(-10,11))
errors=array([0.0]*21)
for i in range(data.shape[0]):
	errors[data[i,1]+10]+=data[i,5]*1.0/31.0  #data[i,1] is the line position. data[i,5] is the motor error.  There are 21 samples at each line position.

ax4 = fig.add_subplot(1,2,2)
ax4.plot(linePositions,errors,'ko')
ax4.set_title('Neglect, Simulation',fontsize=18)
ax4.set_position((.55,0.1,.4,.75))
xlabel('Line Center [pixels]',fontsize=16)
ylabel('Error [pixels]',fontsize=16)
xlim(-11,11)
ylim(-1.5,12)
axhline(y=0,color='k',linestyle='--')



plt.show()

