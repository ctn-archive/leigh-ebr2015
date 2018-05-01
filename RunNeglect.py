#To run from terminal NAVIGATE TO simulator-ui FOLDER and type: java -jar "/home/steven/workspace/simulator-ui/lib/jython.jar" "/home/steven/workspace/simulator-ui/RunNeglect.py" -Xms5000m
#It can be run twice in parallel to make better use of CPU

import NeglectNet
PATH='/home/sleigh/Dropbox/Research/Paper/data/Run Jan 29 2012, PIXELS=120, NEURONS_PER=40/'


#Mainly tested with either 60 PIXELS or 120 PIXELS.  For 60 PIXELS use RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1, for 120 PIXELS use RECEPTIVE_FIELD_WIDTH_MULTIPLIER=4.
#Best results for weber ratio: PIXELS=120, NEURONS_PER_PIXEL=40, RECEPTIVE_FIELD_WIDTH_MULTIPLIER=4? TRAUING_TAU=1
#The same setup shows a strong crossover effect at .3 and .5 damage


#Learning Rate:  
'''
Adaptation is exponential.  For a set learning rate, the adaptation is quick at the start of the prism shift when the error signal is large.
After some adaptation, the error signal is smaller and adaptation slows down.

A learing rate of 0.001 can learn a 10 pixel shift in about 3 seconds and much faster becomes unstable.
A learing rate of 0.0001 can learn a 10 pixel shift in about 6 seconds.
A learing rate of 0.00001 can learn a 10 pixel shift in about 40-50 seconds.
A learing rate of 0.000001 took 75 seconds to learn the first 2 pixels of a 10 pixel shift.  
	If an exponential learning rate is assumed.  (ie, the error decreases as 10*e^(-x/150)), 
	then the Adapt function should have a learning rate of about double this. 0.000002

0.00001 for Adapt will learn a 10 pixel shift in about 50 seconds.  It has been reduced to 0.000001 for further testing.
0.001 seems to be a very fast and stable learning rate and can learn the 10 pixel shift in about 3 seconds.
0.0001 will be tested because learning too fast could result in overfitting, and prism deasaptation is too quick to measure (in the case of Rossetti)

'''

######################################################		
###Define all simulation experiments and parameters
######################################################

#default simulation
'''
NeglectNet.Sim(
	None,  #when using Nengo interface, use world
	1)
'''

#prism adaptation (Warning: can run for over 2 hours or more!)
def Adapt (N=2,dmg=0.0):
	for i in range(N):  #generate N samples
		NeglectNet.Sim(
			None, 
			simulationTime=1800,  
			damage=dmg,
			PIXELS=120,
			NEURONS_PER_PIXEL=40,
			RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1,
			InputLineLocFunc=NeglectNet.CenteredInputLineLoc(1),
			InputLineSizeFunc=NeglectNet.ConstInputLineSize(1),
			InputPrismFunc=NeglectNet.AdaptInputPrism(1),
			learningRate=0.000002,  #This learning rate seems close to normal for this prism adaptation test
			path=PATH+'Adapt D'+str(dmg)+'/',
			showInDataviewer=False)
		print "Done ",1," sample of Adaptation"


#Rossetti's experiment (this experiment also encapsulates the landmark task / amelioration effects from Dankert's paper)
def Rossetti (N=10,dmg=0.0):
	for i in range(N):  #generate N samples
		NeglectNet.Sim(
			None, 
			simulationTime=90,  
			damage=dmg,
			PIXELS=120,
			NEURONS_PER_PIXEL=40,
			RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1,
			InputLineLocFunc=NeglectNet.ErrorVsPosInputLineLoc(1),
			InputLineSizeFunc=NeglectNet.ConstInputLineSize(1),
			InputPrismFunc=NeglectNet.RossettiInputPrism(1),
			learningRate=0.00001,  #use a slightly slower learning rate, otherwise the de-adaptation from prisms is too quick to measure.
			path=PATH+'Rossetti D'+str(dmg)+'/',
			showInDataviewer=False)
		print "Done ",i+1," samples of Rossetti"


#motor bisection error vs line size (Halligan's experiment)
#Try damage=0.3 to see the crossover effect
def Halligan(N=10,dmg=0.0):
	for i in range(N):  #generate ? samples
		NeglectNet.Sim(
			None,
			simulationTime=60,  #60 for 120 PIXELS
			damage=dmg,
			PIXELS=120,
			NEURONS_PER_PIXEL=40,
			RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1,
			InputLineLocFunc=NeglectNet.CenteredInputLineLoc(1),
			InputLineSizeFunc=NeglectNet.HalliganInputLineSize(1),
			InputPrismFunc=NeglectNet.NoInputPrism(1),
			learningRate=0.00001,
			path=PATH+'Halligan D'+str(dmg)+'/',
			showInDataviewer=False)
		print "Done ",i+1," samples of Halligan"


#bisection error vs line location
def bisectvsloc(N=10,dmg=0.0):
	for i in range(N):  #generate N samples
		NeglectNet.Sim(
			None, 
			simulationTime=30,  
			damage=dmg,
			PIXELS=120,
			NEURONS_PER_PIXEL=40,
			RECEPTIVE_FIELD_WIDTH_MULTIPLIER=1,
			InputLineLocFunc=NeglectNet.ErrorVsPosInputLineLoc(1),
			InputLineSizeFunc=NeglectNet.ConstInputLineSize(1),
			InputPrismFunc=NeglectNet.NoInputPrism(1),
			learningRate=0.00001,
			path=PATH+'bisectvsloc D'+str(dmg)+'/',
			showInDataviewer=False)
		print "Done ",i+1," samples of motor error vs location"



'''
#This is a neat simulation and captures the most thorough data, but it takes a long time and the data is probably more thorough than necessary.
#If time permits, it might be neat to make a surf plot of this data with these axes: (line size, line position, motor error)

#To run a simulation of motor bisection error vs line size and position (Halligan's and Vallar's experiment)
def Rando(N=10,dmg=0.0):
for i in range(N):  #generate 10 samples
	NeglectNet.Sim(
		None,
		simulationTime=200,  
		damage=dmg,
		PIXELS=120,
		NEURONS_PER_PIXEL=40,
		RECEPTIVE_FIELD_WIDTH_MULTIPLIER=4,
		InputLineLocFunc=NeglectNet.RandInputLineLoc(1),
		InputLineSizeFunc=NeglectNet.RandInputLineSize(1),
		InputPrismFunc=NeglectNet.NoInputPrism(1),
		learningRate=1e-8,
		path=PATH+'Rand D'+str(dmg)+'/',
		showInDataviewer=False)
	print "Done ",i+1," samples of Rand"
'''



#############################################################
#Actually calling simulations
#############################################################

print "Starting Hemineglect simulations..."

#half of desired data (run in two processes simultaneously for full set of data

'''
These are the most common simulations
for d in [0.0, 0.3, 0.5, 0.7, 0.9]:
	Rossetti(10,d)
	Halligan(10,d)
	bisectvsloc(10,d)
	Adapt(1,d)
'''


'''
#duplicate data found in paper
Halligan(10,0.0)
Halligan(10,0.9)
bisectvsloc(10,0.0)
bisectvsloc(10,0.5)
Rossetti(10,0.0)
Rossetti(10,0.9)
Adapt(5,0.0)
Adapt(5,0.9)
'''



'''
Halligan(10,0.0)
Halligan(10,0.3)
Halligan(10,0.5)
Halligan(10,0.9)
Rossetti(10,0.0)
Rossetti(10,0.5)
Rossetti(10,0.9)
bisectvsloc(10,0.0)
bisectvsloc(10,0.5)
Adapt(5,0.0)
'''
Adapt(5,0.9)


print "Done all simulations."






