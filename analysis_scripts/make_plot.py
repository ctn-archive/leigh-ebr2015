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


fig = plt.figure(figsize=(16,10))
fig.suptitle('Bisection Error vs. Line Length',fontsize=20)
ax = fig.add_subplot(2,2,1)
#ax.plot(([279,254,228,203,178,152,127,102,77,51,25]),([-1.1,-0.88,0.29,-0.34,0.03,-0.02,0.29,0.38,0.52,0.17,0.06]),'ko')
ax.plot(([102,77,51,25]),([0.38,0.52,0.17,0.06]),'ko')
ax.set_title('Normal, Human',fontsize=18)
ax.set_position((.1,0.55,.4,.35))
xlabel('Line Length [mm]',fontsize=16)
ylabel('Error [mm]',fontsize=16)
xlim(0,105)
ylim(-1.4,0.6)
axhline(y=0,color='k',linestyle='--')

ax2 = fig.add_subplot(2,2,2)
#ax2.plot(([279,254,228,203,178,152,127,102,77,51,25]),([49.63,42.29,40.57,36.75,31.9,26.21,20.71,15.21,9.5,3.95,-0.45]),'ko')
ax2.plot(([102,77,51,25]),([15.21,9.5,3.95,-0.45]),'ko')
ax2.set_title('Neglect, Human',fontsize=18)
ax2.set_position((.55,0.55,.4,.35))
xlabel('Line Length [mm]',fontsize=16)
ylabel('Error [mm]',fontsize=16)
xlim(0,105)
ylim(-4,16)
axhline(y=0,color='k',linestyle='--')



#parent=sys.argv[1]
#parent="/home/sleigh/Dropbox/Research/Paper/Simulation Data/Rossetti 1998/Prism Adaptation"
parent=os.getcwd()+"/Normal"
files=os.listdir(parent)
#print files
motorErrors=zeros((40,50))
fileNumber=-1
for file in files:
	data=readcsvFile(parent+'/'+file)
	fileNumber+=1
	samples=0
	for i in range(data.shape[0]):
		if data[i,0]<40: #only gather data from the second iteration over line lengths
			continue
		if data[i,0]>=round(data[i,0]): #only average over the last 0.5 sec of the bisection to eliminate transients
			continue
		motorErrors[79-math.floor(data[i,0]),fileNumber]+=data[i,5]
		if motorErrors[38,fileNumber]==0:
			samples+=1

	for i in range(40):
		motorErrors[i][fileNumber]/=samples

lineLengths=[0]*40
for i in range(40):
	lineLengths[i]=(i+1)*3.4
print '%f,%f,%f,%f' %(lineLengths[6],lineLengths[13],lineLengths[21],lineLengths[28])
print motorErrors[6,:]
ax3 = fig.add_subplot(2,2,3)
ax3.plot((lineLengths[6],lineLengths[13],lineLengths[21],lineLengths[28]),(average(motorErrors[6,:]),average(motorErrors[13,:]),average(motorErrors[21,:]),average(motorErrors[28,:])),'ko')
ax3.set_title('Normal, Simulation',fontsize=18)
ax3.set_position((.1,0.1,.4,.35))
xlabel('Line Length [mm]',fontsize=16)
ylabel('Error [mm]',fontsize=16)
xlim(0,105)
ylim(-1.4,0.6)
axhline(y=0,color='k',linestyle='--')


#parent=sys.argv[1]
#parent="/home/sleigh/Dropbox/Research/Paper/Simulation Data/Rossetti 1998/Prism Adaptation"
parent=os.getcwd()+"/Damaged95"
files=os.listdir(parent)
#print files
motorErrors=zeros((40,50))
fileNumber=-1
for file in files:
	data=readcsvFile(parent+'/'+file)
	fileNumber+=1
	samples=0
	for i in range(data.shape[0]):
		if data[i,0]<40: #only gather data from the second iteration over line lengths
			continue
		if data[i,0]>=round(data[i,0]): #only average over the last 0.5 sec of the bisection to eliminate transients
			continue
		motorErrors[79-math.floor(data[i,0]),fileNumber]+=data[i,5]
		if motorErrors[38,fileNumber]==0:
			samples+=1

	for i in range(40):
		motorErrors[i][fileNumber]/=samples
#print ''
#print average(motorErrors,1)

for i in range(40):
	lineLengths[i]=(i+1)*3.4
#print average(motorErrors,1)[:30]
ax4 = fig.add_subplot(2,2,4)
ax4.plot(lineLengths[:30],average(motorErrors[:30],1),'ko')
ax4.set_title('Neglect, Simulation',fontsize=18)
ax4.set_position((.55,0.1,.4,.35))
xlabel('Line Length [mm]',fontsize=16)
ylabel('Error [mm]',fontsize=16)
#xlim(9,41)
#ylim(-3,10.5)
xlim(0,105)
ylim(-4,16)
axhline(y=0,color='k',linestyle='--')



plt.show()




