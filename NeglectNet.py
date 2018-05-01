#damage=0
PIXELS=120
NEURONS_PER_PIXEL=40
RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1
TRAINING_TAU=1

#Author: Steven Leigh with guidance from Chris Eliasmith
#Description: See the paper for a good overview of this model.  This code models prism amelioration in neglect patients.  
#A common tool used to measure neglect is line bisection.  This model uses line bisection to measure neglect before and after prism exposure. 
#Note: The layout of the network is different than the layout described in the paper (it was simplified to assist conceptual understanding).

#There are a bunch of different classes defined in the 'create input values' section.  The can be commented in/out depending on what input you want to show the network.
#Also, in the 'create inputs' section, some lines can be commented out if you don't want the input to vary.
	
#Different amounts and types of damage can by applied by tweaking made in the 'damage network' section.

#The probe data from these simulations can be saved as .csv files.  Those files can then be read by the following python scripts:
#	combine.py (combines all the separate .csv files that are created into one big .csv file)
#	subsample.py (only takes data from samples where the line size just changed.  Useful for recording only 1 sample per line location/size.)
#	various .py files in the /graphs/script folder can plot different results from the data using matplotlib (They all work on the output from combine.py or subsample.py)
# see Paper/Rossetti 1998/Perceptual_Comparison.py for the most up to date python script that does calculations with .csv data




import os
import sys
sys.path.append("/home/sleigh/workspace/simulator/bin/")
sys.path.append("/home/sleigh/workspace/simulator-ui/bin/")
sys.path.append("/home/sleigh/workspace/simulator-ui/python/")
for f in os.listdir("/home/sleigh/workspace/simulator/lib/"):
    if f.endswith(".jar"):
        sys.path.append("/home/sleigh/workspace/simulator/lib/%s" %f)

      
from ca.nengo.math import *
from ca.nengo.math.impl import *
from ca.nengo.util import *
from ca.nengo.util.impl import *
from ca.nengo.model.impl import *
from ca.nengo.model import *
from ca.nengo.model.nef.impl import *
from ca.nengo.model.nef import NEFEnsemble
from ca.nengo.model.neuron.impl import *
from ca.nengo.model.neuron import *
from ca.nengo.model.plasticity.impl import *
from ca.nengo.io import *
import java
import nef
import math
import random
import array
from java.io import *

import ccm
#log=ccm.log()


######################################################
###Global Variables
######################################################
#PIXELS=60  #number of dimension of input (pixels) in the visual pathway


######################################################
###Functions
######################################################
#Computes the Center Of Mass of the line
#x: vector of points representing line
#datum: centre point of that vector
def COM(x,datum):
	total=0.0
	weightedSum=0.0
	for i in range(len(x)):
		total+=x[i]
		weightedSum+=x[i]*(i-datum)
	return weightedSum/(total+0.001)

#Vector Generator
#Generates pixel representations of various lines
class LineEvalPointVG(VectorGenerator):
	def genVectors(self,number,dimension):
		output= []
		for i in range(100):
			output.append([])
			#loc=random.randint(10,PIXELS-11)
			size=random.uniform(0.1,PIXELS-30)
			#size=-1
			loc=-1
			while((PIXELS/2)-loc<-12 or (PIXELS/2)-loc>12):			
				loc=random.randint(1,PIXELS-1)
			'''
			while(size<0 or size>min(loc,PIXELS-loc)):  #second constraint ensures that line does not extend out of field of view
				#size=random.uniform(0.1,min(loc,PIXELS-loc))
				#System.out.println(size)
				#size=ExponentialPDF(TRAINING_TAU).sample()[0]*10  #There are many more samples of small line sizes than large.  This will achieve the weber ratio effect.  There is a justification for this, although, this exact pdf was chosen and tuned to get the right results.
			
			#size=random.uniform(0.1,min(loc,PIXELS-loc))
			'''
			for j in range(dimension):			
				output[i].append(GenLine(2,j).map([loc,size]))
		return output

#Eval Point Vector Generator.  
#Only generates vectors that represents potential finger positions (ie. lines two pixels wide).
class FingerEvalPointVG(VectorGenerator):
	def genVectors(self,number,dimension):
		output= []
		for i in range(number):
			output.append([])
			loc=random.randint(3,PIXELS-4)
			for j in range(dimension):
				output[i].append(GenLine(2,j).map([loc,2])) 
		return output

#Vector Generator
#creates gaussian encoders for parietal neurons(see paper for specificaitons)
class GaussianEncoderVG(VectorGenerator):
	def genVectors(self,number,dimension):
		output= []
		neuron=-1
		for i in range(dimension):  #encoders for right parietal		
			for k in range (NEURONS_PER_PIXEL/2):#neurons per PIXEL
				gaussian=GaussianPDF(i,(k+1)*3*RECEPTIVE_FIELD_WIDTH_MULTIPLIER)
				output.append([])
				neuron+=1
				for j in range(dimension):  
					output[neuron].append(gaussian.map([j]));

		for i in range(dimension/2,dimension):  #encoders for left parietal		
			for k in range (NEURONS_PER_PIXEL):#neurons per PIXEL
				gaussian=GaussianPDF(i,(k+1)*(3.0/12.0)*RECEPTIVE_FIELD_WIDTH_MULTIPLIER)  
				neuron+=1
				output.append([])
				for j in range(dimension):  
					output[neuron].append(gaussian.map([j]));
		return output

#sets a percent of all connection weights to 0.
#w:connection weights
#percent: percent to damage
def dmgDecoders(w,percent):
	#total=1200
	total=len(w)
	damaged=0.0
	while damaged/total < percent:
		j=random.randint(0,total-1)
		if w[j][0]!=0:
			w[j][0]=0
			damaged+=1
	print damaged	
	return w

#sets a percent of only connection weights of the right parietal cortex to 0.
#w:connection weights
#percent: percent to damage
def dmgRightParietalDecoders(w,percent):
	#total=600
	total=len(w)/2
	damaged=0.0
	while damaged/total < percent:
		j=random.randint(0,len(w)/2)
		if w[j][0]!=0:
			w[j][0]=0
			damaged+=1
	print damaged	
	return w

#sets a percent of only connection weights of the left parietal cortex to 0.
#w:connection weights
#percent: percent to damage
def dmgLeftParietalDecoders(w,percent):
	#total=600
	total=len(w)/2
	damaged=0.0
	while damaged/total < percent:
		j=random.randint(len(w)/2,len(w)-1)
		if w[j][0]!=0:
			w[j][0]=0
			damaged+=1
	print damaged	
	return w


######################################################
###Origin functions
######################################################
#Computes the Actual Center Of Mass for the intput line
class ActCOM (AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,x):
		return COM(x,PIXELS/2)

#Computes the imperfect Center of Mass for a line.
#The error term added is normally distributed with SD of 1/20 the size of the line.
class ProportionalErrorCOM (AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,x):
		total=0
		for i in range(len(x)):
			total+=x[i]
		return GaussianPDF(COM(x,PIXELS/2),(total/60)*(total/60)).sample()[0]


#the size and middle of the line are specified by 2 input values.  This function converts those into the multidimensional representation of the line (into pixels).
#index: pixel index who's value given the line size and location is returned
class GenLine(AbstractFunction): 
	def __init__(self,dim,index):
		AbstractFunction.__init__(self,dim)
		self.index=index
	#x: 2 element array. x[0]:line location,  x[1]: line size
	def map(self,x): 
		if self.index>(x[0]-(x[1]/2)) and self.index<(x[0]+(x[1]/2)):
			return 1.0
		elif math.ceil(x[0]-(x[1]/2) - self.index)==1.0:
			return 1-(x[0]-(x[1]/2) - self.index)
		elif math.floor(x[0]+(x[1]/2) - self.index)==-1.0:
			return 1+(x[0]+(x[1]/2) - self.index)
		return 0.0

#generates the visual representation of the finger position from the middle estimate and PrismControl
class FingPos (AbstractFunction):
	def __init__(self,index,dim):
		AbstractFunction.__init__(self,dim)
		self.index=index
	#x[0]: finger position coming from motor map + prism shift amount (this addition is computed in connection transform)	
	def map(self,x):
		#perform a linear interpolation to map the scalar finger location onto a set of pixels
		if int(self.index)==math.floor(x[0]):
			return 1-(x[0]-self.index)
		if int(self.index)==math.ceil(x[0]):
			return 1-(self.index-x[0])
		#if the finger goes off the side of space, clip it to the farthest pixel
		if x[0]>PIXELS/2 and self.index==PIXELS/2 -1:  
			return 1;
		if x[0]<-PIXELS/2 and self.index==-PIXELS/2 :
			return 1;
		return 0

class PosThresh (AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,x):
		if (x[0]>-10):  #adding some overlap in the error signals creates a crossover effect
			return x[0]+10
		return 0
		
class NegThresh (AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,x):
		if(x[0]<10):
			return x[0]-10
		return 0
######################################################	
###create input values
######################################################
#These next three classes can be used together to simulate the input for prism exposure on a single line. 
#Typically run for 1800 sec (5 min for normalization, 10 min for adaptation, 15 min for observing immediate after-effects)
#Important note: The line is actually centred the entire time, it is only shifted to simulate the effect of prisms.  The finger representation is also shifted to simulate the effect of prisms as well.
#					If you don't move the location of the line and only change the prism control, it is as if the actual line position has changed in the opposite direction of the prism shift (but the retinal
#						representation remains the same.

#shifts prism 10 degrees and back again
class AdaptInputPrism(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,t):
		if t[0]<300:
			return 0
		if t[0]<900:
			return 10
		return 0
'''	
#shifts line 10 degrees and back again
class AdaptInputLineLoc(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,t):
		if t[0]<300:
			return 0
		if t[0]<900:
			return 10
		return 0
'''	

#iterates through all line sizes from 10 to 40 (inclusive), and all line locations from -10 to 10 (inclusive).  run for 1305 sec
'''
class ErrorVsPosAndSizeInputLineLoc(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.loc=-10
	def map(self,t):
		if t[0]%62==0:
			self.loc+=1
		if self.loc>10:
			self.loc=-1
		if t[0]<1:
			self.loc=-10
		return self.loc
		
class ErrorVsPosAndSizeInputLineSize(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.size=5
	def map(self,t):
		if t[0]%2==0:
			self.size+=0.5
		if self.size>20:
			self.size=5
		if t[0]<1:
			self.size=5
		return self.size
'''


#iterates through each line 2 times so that learning and stabilization can be done on the first iteration. 
#presents line in pseudo-random fashion.
#run for (5 line sizes)*(3 sec per line)*(2 iterations)=30 sec.
class ErrorVsPosInputLineLoc(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.loc=-10
		self.line_loc_list=range(-10,11,5)  #5 line positions
	def map(self,t):
		if t[0]%3==0:
			if len(self.line_loc_list)<1:
				self.line_loc_list=range(-10,11,5)
			self.loc=self.line_loc_list.pop(random.randint(0,len(self.line_loc_list)-1))
		#if self.loc>10:
		#	self.loc=-10
		return self.loc

'''
#Used for Rossetti 1998 amelioration data
class RossettiInputLineLoc(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.loc=-20
	def map(self,t):
		if t[0]%1==0:
			self.loc+=10
		if self.loc>10:
			self.loc=-10
		if t[0]<6:
			return self.loc
		if t[0]<30:
			return 10 + self.loc
		return self.loc
'''
	
#class RossettiInputLineSize(AbstractFunction):
#	def __init__(self,dim):
#		AbstractFunction.__init__(self,dim)
#	def map(self,t):
#		return 15

class RossettiInputPrism(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,t):
		if t[0]<15:
			return 0
		if t[0]<45:
			return 10
		return 0

#Used for Halligan's data
#run for (10 lines) *(3 seconds per line)*(2 iterations)= 60 seconds
#iterates through centered lines with various sizes
#iterates through each line 2 times so that learning and stabilization can be done on the first iteration
#lines are presented in pseudo-random order as is done in Halligan's experiment.  
#line sizes are drawn randomly without replacement
class HalliganInputLineSize(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.size=0
		self.line_sizes=range(1,PIXELS,13)  #10 line sizes
	def map(self,t):
		if t[0]%2==0:  #change line size once every 3 seconds
			if len(self.line_sizes)<1:
				self.line_sizes=range(1,PIXELS,13) 
			self.size=self.line_sizes.pop(random.randint(0,len(self.line_sizes)-1))
		#if self.size<1:
		#	self.size=PIXELS/2
		return self.size



#Used to gather data for Halligan's and Vallar's data together.
#Chooses random line sizes and locations
#Run for any integer number of seconds
class RandInputLineSize(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.size=1
	def map(self,t):
		if t[0]%1==0:  #pick random line size once every second
			self.size=random.randint(1,PIXELS-20)
		return self.size

class RandInputLineLoc(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.loc=0
	def map(self,t):
		if t[0]%1==0:
			self.loc=random.randint(-10,10)
		return self.loc




#General inputs used for multiple different simulations
class CenteredInputLineLoc(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
		self.loc=0
	def map(self,t):
		return 0

#line size remains at 20? for the entire time
class ConstInputLineSize(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,t):
		return 4

class NoInputPrism(AbstractFunction):
	def __init__(self,dim):
		AbstractFunction.__init__(self,dim)
	def map(self,t):
		return 0

######################################################		
###Main function for setting up and running the hemineglect network
######################################################
#TODO add in the rest of the simulation parameters. (left/right damage. error func damage?)
def Sim(w,
	simulationTime,
	damage=0,
	PIXELS=120,
 	NEURONS_PER_PIXEL=40,
 	RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1,
 	InputLineLocFunc=CenteredInputLineLoc(1),
 	InputLineSizeFunc=ConstInputLineSize(1),
 	InputPrismFunc=NoInputPrism(1),
 	learningRate=1e-5,
	path='/home/sleigh/Desktop/Link to Research/Paper/data/',
	showInDataviewer=False):



	'''
	w=world
	simulationTime=0.02
	damage=0
	PIXELS=120
	NEURONS_PER_PIXEL=40
	RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1
	InputLineLocFunc=CenteredInputLineLoc(1)
	InputLineSizeFunc=ConstInputLineSize(1)
	InputPrismFunc=NoInputPrism(1)
	learningRate=0.0001
	path='/home/sleigh/Desktop/Link to Research/Paper/data/'
	showInDataviewer=False
	'''

	net=nef.Network('Hemineglect')
	NodeThreadPool.setNumThreads(3)
	#net.add_to(w)  #include this line if you are using the Nengo interface.  If the script is being run through the terminal comment this line out.

	######################################################		
	###create inputs
	######################################################

	inputArray=[]
	for i in range(-PIXELS/2,PIXELS/2):
		inputArray.append(GenLine(2,i))	

	lineFunc=net.make('Line Generation',PIXELS,2,mode='direct')
	lineFuncOut=lineFunc.addDecodedOrigin('Line Func Out',inputArray,'AXON')

	lineInput=FunctionInput('Line Input',[InputLineLocFunc,InputLineSizeFunc],Units.UNK)  
	net.network.addNode(lineInput)
	#net.make_input('Line Input',values=[0,20]) #use this if you don't want the size and location changing.  Good for user modulation in interactive mode.

	#prismInput=FunctionInput('Prism Input',[InputPrism(1)],Units.UNK)  #use this line for prism adaptation input scenario
	prismInput=FunctionInput('Prism Input',[InputPrismFunc],Units.UNK)
	net.network.addNode(prismInput) #use this line for prism adaptation input scenario
	#net.make_input('Prism Input',values=[0]) #use this line for input scenario where prisms are not used (eg. when simulating lines at various locations and sizes to evaluate bisection without prisms)


	######################################################
	###create ensembles
	######################################################
	print 'Creating parietalLine ensemble'
	ef=NEFEnsembleFactoryImpl()
	ef.setEncoderFactory(GaussianEncoderVG())
	ef.setEvalPointFactory(LineEvalPointVG())
	#ef.setApproximatorFactory(WeightedCostApproximator.Factory(0.2))  #more noise can make the ensemble more robust to decoder damage
	ef.setNodeFactory(LIFNeuronFactory(0.02,0.001,IndicatorPDF(200,400),IndicatorPDF(0.0,1.0)))
	parietalLine=ef.make('Parietal Line',PIXELS*NEURONS_PER_PIXEL,PIXELS)
	net.network.addNode(parietalLine)
	parietalLineOut = parietalLine.addDecodedOrigin('Middle',[ProportionalErrorCOM(PIXELS)],'AXON')
	parietalLine.setMode(SimulationMode.DEFAULT)

	print 'Creating parietalFinger ensemble'
	ef.setEncoderFactory(GaussianEncoderVG())
	ef.setEvalPointFactory(FingerEvalPointVG())
	#ef.setApproximatorFactory(WeightedCostApproximator.Factory(0.1))  #more noise can make the ensemble more robust to decoder damage
	ef.setNodeFactory(LIFNeuronFactory(0.02,0.001,IndicatorPDF(200,400),IndicatorPDF(0.0,1.0)))
	parietalFinger=ef.make('Parietal Finger',PIXELS*NEURONS_PER_PIXEL,PIXELS)
	net.network.addNode(parietalFinger)
	parietalFingerOut = parietalFinger.addDecodedOrigin('Middle',[ActCOM(PIXELS)],'AXON')
	#parietalFingerOut.setDecoders(MU.transpose([MU.makeVector(-0.12,0.0004,-0.0004)+MU.makeVector(0.0004,0.0004,0.12)+
	#MU.makeVector(0.0002,0.0002,0.12)]))
	parietalFinger.setMode(SimulationMode.DEFAULT)

	print'Creating additional ensembles'
	#comChan = net.make('Com Channel',100,1,radius = PIXELS/2,mode='spike',quick=False)
	motor = net.make('Motor Map',neurons=100,dimensions=1,radius = PIXELS/2, mode='spike',quick=False)
	finger = net.make('Finger',20,1,mode='direct',quick=True)

	#rightError = net.make('Rightward Error',100,1,radius = PIXELS/2,mode='spike',quick=True)
	ef=NEFEnsembleFactoryImpl()
	ef.nodeFactory.intercept=IndicatorPDF(-.2,1)
	rightError = ef.make('Rightward Error',100,[PIXELS/2])
	net.network.addNode(rightError)
	rightError.setEncoders([[-1.0]]*100)  #set encoders for error functions to be unidirectional
	rightErrorOut = rightError.addDecodedOrigin('Thresh',[NegThresh(1)],'AXON')

	ef=NEFEnsembleFactoryImpl()
	ef.nodeFactory.intercept=IndicatorPDF(-0.2,1)
	leftError = ef.make('Leftward Error',100,[PIXELS/2])
	net.network.addNode(leftError)
	leftError.setEncoders([[1.0]]*100)  #set encoders for error functions to be unidirectional
	leftErrorOut = leftError.addDecodedOrigin('Thresh',[PosThresh(1)],'AXON')

	#leftError = net.make('Leftward Error',100,1,radius = PIXELS/2,mode='spike',quick=True)	
	#leftError.setEncoders([[1.0]]*100)
	#leftErrorOut = leftError.addDecodedOrigin('Thresh',[PosThresh(1)],'AXON')
	add = net.make('Add',100,1,radius=PIXELS/2,mode='spiking',quick=False)
	#shiftFinger = net.make('Shift Finger',61,PIXELS+1,mode='direct',quick=True)

	actualCOM=net.make('True Center of Mass',PIXELS,PIXELS,mode='direct')
	actualCOMOut = actualCOM.addDecodedOrigin('Middle',[ActCOM(PIXELS)],'AXON')
	perceptualError=net.make('True Perceptual Error',1,1,mode='direct')
	motorError=net.make('True Motor Error',1,1,mode='direct')
	motorErrorIn=motorError.addDecodedTermination('Motor In',[[1]],0.01,False)

	#these are the ensembles that run in spiking mode
	parietalLine.fixMode()
	parietalFinger.fixMode()
	#comChan.fixMode()
	motor.fixMode()
	rightError.fixMode()
	leftError.fixMode()
	add.fixMode()


	######################################################
	###add Origins that are defined by N->M dimensional functions (currently not supported in nef.py)
	######################################################
	#w=MU.prod(motor.encoders,MU.transpose(MU.prod(comChan.getOrigin('X').decoders,1.0/(PIXELS/2.0))))
	#motor.addTermination('Desired Pos',w,0.005,False)
	motor.addDecodedTermination('Desired Pos',[[1]],0.005,False)
	motorModError=motor.addDecodedTermination('Mod Error',[[-1]],0.005,True)

	FingArray = []
	for i in range(-PIXELS/2,PIXELS/2):
		FingArray.append(FingPos(i,1))
	fingerOut = finger.addDecodedOrigin("Finger Out",FingArray,"AXON")


	######################################################
	###make connections
	######################################################
	print 'Making connections'
	net.connect('Line Input',lineFunc)
	net.connect('Prism Input',lineFunc,[[1],[0]])
	net.connect(lineFuncOut,actualCOM)
	net.connect(actualCOMOut,perceptualError,weight=-1)
	net.connect(actualCOMOut,motorError,weight=-1)
	net.connect(parietalLineOut,perceptualError)
	net.connect(motor.getOrigin('X'),motorErrorIn)
	net.connect('Prism Input',motorError)
	net.connect(lineFuncOut,parietalLine)
	net.connect(motor,finger)
	net.connect('Prism Input',finger)
	net.connect(fingerOut,parietalFinger)
	net.connect(parietalFinger.getOrigin('Middle'),rightError,weight=-1)
	net.connect(parietalFinger.getOrigin('Middle'),leftError,weight=-1)
	net.connect(parietalLine.getOrigin('Middle'),rightError)
	net.connect(parietalLine.getOrigin('Middle'),leftError)
	net.connect(rightError.getOrigin('Thresh'),add)
	net.connect(leftError.getOrigin('Thresh'),add)
	net.connect(add,motor.getTermination('Mod Error'))
	#net.connect(comChan.getOrigin('AXON'),motor.getTermination('Desired Pos'))
	#net.connect(parietalLine.getOrigin('Middle'),comChan)
	net.connect(parietalLine.getOrigin('Middle'),motor.getTermination('Desired Pos'))


	######################################################
	###add plasticity
	######################################################
	'''
	learnIn=InSpikeErrorFunction(motor)
	learnIn.setLearningRate(learningRate)  #2e-10 seems close to normal.  I mostly used 1e-8 for quicker learning allowing quicker simulations
	learnOut=OutSpikeErrorFunction(motor)
	learnOut.setLearningRate(learningRate)  #2e-10 seems close to normal
	rule=SpikePlasticityRule(learnIn,learnOut,'AXON','Mod Error')
	motor.setPlasticityRule('Desired Pos',rule)
	'''
	vectorSpikeRule=VectorSpikeRule(motor.getOrigin('X'),motorModError , learningRate, 0.0000001, 0.9999, True)

	######################################################
	###damage network
	######################################################
	print 'Applying damage (if any) to network'
	#Uncomment these lines to simulate various types of damage.  The amounts can also be changed(change .95 is percent of damage)
	#Usually, I have damaged right decoders for parietalLineOut and parietalFingerOut to 95% to simulate neglect
	#parietalLineOut.setDecoders(dmgDecoders(parietalLineOut.getDecoders(),.05))  #damage all decoders
	parietalLineOut.setDecoders(dmgRightParietalDecoders(parietalLineOut.getDecoders(),damage))  #damage only decoders of right parietal neurons
	#parietalLineOut.setDecoders(dmgLeftParietalDecoders(parietalLineOut.getDecoders(),.95))  #damage only decoders of left parietal neurons

	#parietalFingerOut.setDecoders(dmgDecoders(parietalFingerOut.getDecoders(),.1))  #damage all decoders
	parietalFingerOut.setDecoders(dmgRightParietalDecoders(parietalFingerOut.getDecoders(),damage))  #damage only decoders of right parietal neurons
	#parietalFingerOut.setDecoders(dmgLeftParietalDecoders(parietalFingerOut.getDecoders(),.95))  #damage only decoders of left parietal neurons
	#rightErrorOut.setDecoders(dmgDecoders(rightErrorOut.getDecoders(),.95))
	#leftErrorOut.setDecoders(dmgDecoders(leftErrorOut.getDecoders(),.95))

	#Damage error signals
	leftError.getOrigin('Thresh').setDecoders(dmgDecoders(leftError.getOrigin('Thresh').getDecoders(),damage))
	#rightError.getOrigin('Thresh').setDecoders(dmgDecoders(rightError.getOrigin('Thresh').getDecoders(),damage))


	######################################################
	###probes
	######################################################
	#add probes
	p1=net.network.getSimulator().addProbe("Line Input",'input',1)
	p2=net.network.getSimulator().addProbe("Prism Input",'input',1)
	#p4=net.network.getSimulator().addProbe("True Motor Error",motorError.X,1)
	#p5=net.network.getSimulator().addProbe("True Perceptual Error",perceptualError.X,1)
	p3=net.network.getSimulator().addProbe("Parietal Line",'Middle',1)
	p4=net.network.getSimulator().addProbe("Motor Map",'X',1)
	p5=net.network.getSimulator().addProbe("Parietal Finger",'Middle',1)
	p6=net.network.getSimulator().addProbe("Leftward Error",'Thresh',1)
	p7=net.network.getSimulator().addProbe("Rightward Error",'Thresh',1)
	p8=net.network.getSimulator().addProbe("Add",'X',1)


	#Increasing the sampling rate can result in some .csv output files being >100mB (for the 15 min simulation).  
	#Outputs are subsampled to decrease data sizes (1000Hz simulation steps, to 100Hz sample steps).
	probes=net.network.getSimulator().getProbes()
	for i in probes:
		i.setSamplingRate(100)  #100 samples per second


	######################################################
	###simulate
	######################################################
	print 'Starting simulation'
	#set everything to run in direct mode, unless its mode is fixed to run in spiking mode (all ensembles that are supposed to be in the brain are fixed in spiking mode)
	net.network.setMode(SimulationMode.DIRECT)

	sim=net.network.getSimulator()
	#sim.run(0.0,36.0,0.001)
	#sim.run(0.0,80,0.001) #used for halligans data
	#sim.run(0.0,36,0.001) #used for halligans data
	##sim.run(0.0,(PIXELS),0.001) #used for halligans data
	#sim.run(0.0,6.0,0.001)
	#sim.run(0.0,1800.0,0.001) #use for adaptation
	#sim.run(0.0,1305.0,0.001) #use for lines of various locations and sizes
	sim.run(0.0,simulationTime,0.001)


	######################################################
	###save simulation data
	######################################################
	print 'Exporting simulation data'
	if showInDataviewer:
		ca.nengo.ui.lib.util.UIEnvironment.getInstance().captureInDataViewer(net.network)  #makes data show up in data viewer


	#save data to csv file
	data=[]
	data.append(MU.transpose(p1.getData().getValues())[0])
	data.append(MU.transpose(p1.getData().getValues())[1])
	data.append(MU.transpose(p2.getData().getValues())[0])
	data.append(MU.transpose(p3.getData().getValues())[0])
	data.append(MU.transpose(p4.getData().getValues())[0])
	data.append(MU.transpose(p5.getData().getValues())[0])
	data.append(MU.transpose(p6.getData().getValues())[0])
	data.append(MU.transpose(p7.getData().getValues())[0])
	data.append(MU.transpose(p8.getData().getValues())[0])

	timeseries=TimeSeriesImpl(p1.getData().getTimes(),MU.transpose(data),[Units.UNK]*9)
	exporter=DelimitedFileExporter()
	#files=os.listdir('/home/sleigh/Desktop/Link to Research/Paper/data/')
	if not os.path.exists(path):
		os.makedirs(path)
	files=os.listdir(path)
	#f=File('/home/sleigh/Desktop/Link to Research/Paper/data/'+str(iter)+'.csv')  #change this line to where ever you want the .csv files stored
	#f=File('/home/sleigh/Desktop/Link to Research/Paper/data/'+str(len(files))+'.csv')
	f=File(path+str(len(files))+'.csv')
	f.createNewFile()
	exporter.export(timeseries,f)


	'''
	motorErrors=[0]*(PIXELS/2)
	raw_motor_Errors=p4.getData().getValues()
	times=p1.getData().getTimes()

	samples=0
	for i in range(len(times)):
		if times[i]<((PIXELS/2)): #only gather data from the second iteration over line lengths
			continue
		if times[i]>=round(times[i]): #only average over the last 0.5 sec of the bisection to eliminate transients
			continue
		motorErrors[int((PIXELS)-1-math.floor(times[i]))]+=raw_motor_Errors[i][0]
	#		if motorErrors[17,fileNumber]==0:
		if((PIXELS)-1-math.floor(times[i])==0):
			samples+=1
	#print samples
	for i in range(60):
		if i<len(motorErrors):
			motorErrors[i]/=samples
			setattr(log,'processed_motor_error_%02d'%i,motorErrors[i])
		else:
			setattr(log,'processed_motor_error_%02d'%i,0)


	'''
	'''


	log.time=times
	log.line_loc=MU.transpose(p1.getData().getValues())[0]
	log.line_size=MU.transpose(p1.getData().getValues())[1]
	log.prism_input=MU.transpose(p2.getData().getValues())[0]
	log.motor_error=MU.transpose(p4.getData().getValues())[0]
	log.perceptual_error=MU.transpose(p5.getData().getValues())[0]
	'''
	print 'Simulation complete'
