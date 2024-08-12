'''
Call this file as python3 main.py xyz.config
where 'xyz.config' is the configuration file to edit
'''

#########################
import numpy as np
import matplotlib.pyplot as plt
import maglib as maglib
import sys as sys
import configparser
#########################
'''
Solving ODE for biomass B
dB / dt = G*B - L * B^2

B --> vert. integrated biomass [kg / m^2]
G --> growth rate [1/s]
L --> loss rate [1/s]
'''
####################################
#Read in arguments from params file
###################################
param_file = sys.argv[1]
#Read in Inputs from .opt (config) file
config=configparser.ConfigParser()
#Preserves lower/upper case strings
config.optionxform=str
#Create dictionary of user-inputted parameters
config.read(param_file)

###################################
#Assign some stuff from param file
###################################
B0    = float(config['PARAM']['B0'])
L0    = float(config['PARAM']['L0'])
Gmax  = float(config['PARAM']['Gmax'])
tend  = float(config['PARAM']['tend']) * 86400. #convert to sec
dt   = float(config['PARAM']['dt'])


##################################################
#Initialize dictionary with all relevant variables
mdict = {}
#Setup time vector
mdict['tvec'] = maglib.create_tvec(tend,dt)
#Get number of time-steps
nt = len(mdict['tvec'])
##################################################

##################################################
#Setup dictionary with relevant arrays
'''
mdict will contain 1D arrays of
B --> biomass
no3 --> nitrate conc.
temp --> temperature
'''
mdict = maglib.setup_mag_dict(nt,mdict)
mdict['Gmax'] = Gmax
mdict['L0'] = L0
mdict['dt'] = dt

#Initialize biomass
mdict['B'][0] = B0
##################################################

#######################
#Time-step
######################
mdict = maglib.time_step(mdict)


#######################
#Write variables to netcdf
######################
maglib.write_to_nc(mdict, config['PARAM']['sim_name'])


#######################
#Plot
######################
plt.ion()
plt.figure()
plt.plot(mdict['tvec']/86400.,mdict['B'],color='k',linewidth=3)
plt.xlabel('Time [days]',fontsize=14)
plt.ylabel('B [kg/m^2]',fontsize=14)







