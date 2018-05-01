from numpy import *
from matplotlib import *
import matplotlib.pyplot as plt
from pylab import *

#x=('Pre','Pre','Pre','Post','Post','Post')
RR=(26,-15)
RC=(63,42)
RL=(85,71)
MR=(26.24,8.42)
MC=(49.85,30.46)
ML=(75.5,56.7)


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.errorbar((1,1.5),RR,yerr=(24.49,26.94),color='k',linestyle='-')
ax.errorbar((1.08,1.58),RC,yerr=(24.49,19.6),color='k',linestyle='-')
ax.errorbar((1.16,1.66),RL,yerr=(19.6,24.49),color='k',linestyle='-')
ax.errorbar((1.04,1.54),MR,yerr=(19.12,20.73),color='k',linestyle='--')
ax.errorbar((1.12,1.62),MC,yerr=(18.46,19.22),color='k',linestyle='--')
ax.errorbar((1.2,1.7),ML,yerr=(12.61,13.85),color='k',linestyle='--')
ax.set_title('Prism Amelioration',fontsize=18)
axhline(y=0,color=('0.8'))
#axvline(x=0,color=('0.8'))
ax.set_position((.2,0.11,.6,.75))
xlim(0.8,1.8)
ylim(110,-50)
#xlabel('Spatial Discordance [pixels]',fontsize=16)
ylabel('Percent Deviation',fontsize=16)
ax.set_xticks((1.1,1.6))
ax.set_xticklabels(('Pre','Post'),size=16)
lgd=legend(('Rossetti','Ours'),2)
lgd.get_lines()[0].set_ls('-')
lgd.get_lines()[1].set_ls('--')
text(0.84,30,'Right')
text(0.87,67,'Centre')
text(1,100,'Left')
plt.show()

