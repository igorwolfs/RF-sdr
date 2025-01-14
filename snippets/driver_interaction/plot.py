import sys
from pathlib import Path, PurePath
import os

##################################################
#################### SETUP #######################
##################################################

curr_filename = Path(__file__).parts[-1].strip(".py")
currDir = Path(__file__).parents[0]

##################################################
################# SETTINGS #######################
##################################################

folder_name = "iio_server"



##################################################
################# CSV LOADING ####################
##################################################

### SAVE IMPEDANCE AND S-PARAMETERS
import csv

Plot_Path = os.path.join(currDir, folder_name + "_plots")
if (not os.path.exists(Plot_Path)):
    os.mkdir (Plot_Path)

# Load frequency / time-series data to be plotted here

##################################################
################# PLOTTING  ######################
##################################################

from pylab import *

Zin = 0
freq = 0
plot(freq/1e9, np.real(Zin), 'k-', linewidth=2, label='$\Re\{Z_{in}\}$')
plot(freq/1e9, np.imag(Zin), 'r--', linewidth=2, label='$\Im\{Z_{in}\}$')
grid()
legend()
ylabel('Zin (Ohm)')
xlabel('Frequency (GHz)')
plt.savefig(os.path.join(Plot_Path, 'impedance.png'))
show()