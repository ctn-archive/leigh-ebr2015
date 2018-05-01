#shows 4 plots comparing bisection errors vs line length for normals and patients and also compares simulations of normals and patients.
#Human data is gathered from "The bisection of horizontal and radial lines: a case study of normal controls and ten patients with left visuospatial neglect"(Halligan)


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


#read in data from csv file.  The csv file is created using combine.py (not subsample.py?)



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


fig = plt.figure(figsize=(16,10))
fig.suptitle('Bisection Error vs. Line Length',fontsize=20)
ax = fig.add_subplot(2,2,1)
ax.plot(([279,254,228,203,178,152,127,102,77,51,25]),([-1.1,-0.88,0.29,-0.34,0.03,-0.02,0.29,0.38,0.52,0.17,0.06]),'ko')
ax.set_title('Normal, Human',fontsize=18)
ax.set_position((.1,0.55,.4,.35))
xlabel('Line Length [cm]',fontsize=16)
ylabel('Error [cm]',fontsize=16)
axhline(y=0,color='k',linestyle='--')

ax2 = fig.add_subplot(2,2,2)
ax2.plot(([279,254,228,203,178,152,127,102,77,51,25]),([49.63,42.29,40.57,36.75,31.9,26.21,20.71,15.21,9.5,3.95,-0.45]),'ko')
ax2.set_title('Neglect, Human',fontsize=18)
ax2.set_position((.55,0.55,.4,.35))
xlabel('Line Length [cm]',fontsize=16)
ylabel('Error [cm]',fontsize=16)
ylim(-14,52)
axhline(y=0,color='k',linestyle='--')

data=readcsvFile('/home/sleigh/Dropbox/Research/Paper/Simulation Data/Spiking Data/Normal_Line_Loc_Size/Simulation 2h9m4s 7M20D/data.csv')
lineLengths=array(range(10,41))
errors=array([0.0]*31)

for i in range(data.shape[0]):
	errors[data[i,2]*2-10]+=data[i,5]*1.0/21.0  #data[i,2] is half the line size. data[i,5] is the motor error.  There are 21 samples at each line size.

ax3 = fig.add_subplot(2,2,3)
ax3.plot(lineLengths,errors,'ko')
ax3.set_title('Normal, Simulation',fontsize=18)
ax3.set_position((.1,0.1,.4,.35))
xlabel('Line Length [pixels]',fontsize=16)
ylabel('Error [pixels]',fontsize=16)
xlim(9,41)
ylim(-0.6,0.25)
axhline(y=0,color='k',linestyle='--')


#data=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_line_loc_size_2e-10_rate2/Simulation 16h42m47s 7M25D/data.csv')
#data=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled6/Simulation 1h48m8s 7M26D/data.csv')
#=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled5/Simulation 23h38m16s 7M25D/data.csv')
data=readcsvFile('/home/sleigh/Desktop/Link to Research/Paper/Simulation Data/Spiking Data/Best Data/Damaged_adapt_rate:2e-10_subsampled3/Simulation 21h30m48s 7M25D/data.csv')
lineLengths=array(range(10,41))
errors=array([0.0]*31)
for i in range(data.shape[0]):
	errors[data[i,2]*2-10]+=data[i,5]/21.0  #data[i,2] is half the line size. data[i,5] is the motor error.  There are 21 samples at each line size.

ax4 = fig.add_subplot(2,2,4)
ax4.plot(lineLengths,errors,'ko')
ax4.set_title('Neglect, Simulation',fontsize=18)
ax4.set_position((.55,0.1,.4,.35))
xlabel('Line Length [pixels]',fontsize=16)
ylabel('Error [pixels]',fontsize=16)
xlim(9,41)
ylim(-3,10.5)
axhline(y=0,color='k',linestyle='--')



plt.show()

