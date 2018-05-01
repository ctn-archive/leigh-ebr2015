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

#parent=sys.argv[1]
#parent="/home/sleigh/Dropbox/Research/Paper/Simulation Data/Rossetti 1998/Prism Adaptation"
#parent=os.getcwd()+"/Normal"
parent=os.getcwd()+"/data"
files=os.listdir(parent)
#print files
motorErrors=zeros((18,50))
fileNumber=-1
for file in files:
	data=readcsvFile(parent+'/'+file)
	fileNumber+=1
	samples=0
	for i in range(data.shape[0]):
		if data[i,0]<18: #only gather data from the second iteration over line lengths
			continue
		if data[i,0]>=round(data[i,0]): #only average over the last 0.5 sec of the bisection to eliminate transients
			continue
		motorErrors[35-math.floor(data[i,0]),fileNumber]+=data[i,5]
#		if motorErrors[17,fileNumber]==0:
		if(35-math.floor(data[i,0])==0):
			samples+=1
	#print samples
	for i in range(18):
		motorErrors[i][fileNumber]/=samples

lineLengths=[0]*18
#print len(lineLengths)
for i in range(18):
	lineLengths[i]=(i+1)*4
#print '%f,%f,%f,%f' %(lineLengths[6],lineLengths[13],lineLengths[21],lineLengths[28])
#print motorErrors[6,:]
ax = fig.add_subplot(1,2,1)
ax.errorbar((102,77,51,25),(0.42,0.33,0.12,0.06),yerr=(2.8,2.0,1.3,0.8),color='k',linestyle='-')
#y=(lineLengths[1],lineLengths[2],lineLengths[3],lineLengths[4])
y=(22,50,78,103)
x=(average(motorErrors[0,:])*2,average(motorErrors[5,:])*2,average(motorErrors[10,:])*2,average(motorErrors[17,:])*2)
e=(std(motorErrors[0,:])*2,std(motorErrors[5,:])*2,std(motorErrors[10,:])*2,std(motorErrors[17,:])*2)
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






parent=os.getcwd()+"/DamagedData"
files=os.listdir(parent)
#print files
motorErrors=zeros((18,50))
fileNumber=-1
for file in files:
	data=readcsvFile(parent+'/'+file)
	fileNumber+=1
	samples=0
	for i in range(data.shape[0]):
		if data[i,0]<18: #only gather data from the second iteration over line lengths
			continue
		if data[i,0]>=round(data[i,0]): #only average over the last 0.5 sec of the bisection to eliminate transients
			continue
		motorErrors[35-math.floor(data[i,0]),fileNumber]+=data[i,5]
#		if motorErrors[17,fileNumber]==0:
		if(35-math.floor(data[i,0])==0):
			samples+=1
	#print samples
	for i in range(18):
		motorErrors[i][fileNumber]/=samples

lineLengths=[0]*18
#print len(lineLengths)
for i in range(18):
	lineLengths[i]=(i+1)*4
#print '%f,%f,%f,%f' %(lineLengths[6],lineLengths[13],lineLengths[21],lineLengths[28])
#print motorErrors[6,:]
ax = fig.add_subplot(1,2,2)
ax.errorbar((102,77,51,25),(15.21,9.5,3.95,-0.45),yerr=(11.45,7.34,3.63,2.24),color='k',linestyle='-')
#y=(lineLengths[1],lineLengths[2],lineLengths[3],lineLengths[4])
y=(22,50,78,103)
x=(average(motorErrors[0,:])*2,average(motorErrors[5,:])*2,average(motorErrors[10,:])*2,average(motorErrors[17,:])*2)
e=(std(motorErrors[0,:])*2,std(motorErrors[5,:])*2,std(motorErrors[10,:])*2,std(motorErrors[17,:])*2)
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

'''
#parent=sys.argv[1]
#parent="/home/sleigh/Dropbox/Research/Paper/Simulation Data/Rossetti 1998/Prism Adaptation"
parent=os.getcwd()+"/DamagedData"
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
lineLengths=[0]*40
for i in range(40):
	lineLengths[i]=(i+1)*4
print average(motorErrors,1)[:30]
ax = fig.add_subplot(1,2,2)
ax.errorbar((102,77,51,25),(15.21,9.5,3.95,-0.45),yerr=(11.45,7.34,3.63,2.24),color='k',linestyle='-')
y=(lineLengths[5],lineLengths[11],lineLengths[18],lineLengths[24])
x=(average(motorErrors[5,:])*2,average(motorErrors[11,:])*2,average(motorErrors[18,:])*2,average(motorErrors[24,:])*2)
e=(std(motorErrors[5,:])*2,std(motorErrors[11,:])*2,std(motorErrors[18,:])*2,std(motorErrors[24,:])*2)
ax.errorbar(y,x,yerr=e,color='k',linestyle='--')
#ax.plot(lineLengths[:30],average(motorErrors[:30],1),'ko')
ax.set_title('Neglect',fontsize=18)
ax.set_position((.55,0.12,.4,.75))
xlabel('Line Length [mm]',fontsize=16)
ylabel('Error [mm]',fontsize=16)
#xlim(9,41)
#ylim(-3,10.5)
#xlim(0,105)
#ylim(-4,27)
#axhline(y=0,color='k',linestyle='--')
axhline(y=0,color=('0.8'))


'''
plt.show()




