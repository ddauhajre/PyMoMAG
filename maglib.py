#########################################
#IMPORT MODULES
import os
import sys
import numpy as np
import pickle as pickle
from netCDF4 import Dataset as netcdf
from datetime import date
#########################################

      ############################################################
      #             VARIABLE DICTIONARY SETUP
'''
                    ALL DATA RELEVANT TO MODEL IS STORED IN
                    DICTIONARY THAT WILL BE SAVED AS A PICKLE FILE
                    
                    NEED FUNCTIONALITY TO SET UP THIS DICTIONARY
'''
      ############################################################

def add_keys_var_dict(keys_add,keys_type,var_dict={}):
    '''
    var_dict --> dictionary to add keys to (default is empty {} or
                 but can be an actual pre-existing dictionary)

    keys_add ---> list of string of keys to set up dictionary with

    keys_type--> list of data types corresponding to each key (i.e., empty 
                       list or string or numpy array
    '''
    for ke in range(len(keys_add)):
        var_dict[keys_add[ke]] = keys_type[ke]

    return var_dict
    ##################################################

def create_empty_list_key(keys_add,var_dict={}):
    for ke in range(len(keys_add)):
        var_dict[keys_add[ke]] = []
    return var_dict

      
def setup_mag_dict(nt,mdict):
    """
    CREATE LIST OF KEYS / TYPES FOR SOLUTION
    DICTIONARY

    # NECESSARY DIMENSIONS FOR SOLN ARRAYS
    nt --> number of time points

    B --> biomass as a function of time [kg/m^2]
    G --> growth rate as a function of time [1/s]
    M ---> mortality rate as a function of time [1/s]
    RHS_grow --> R.H.S growth term [kg / (s*m ^2)]
    RHS_loss --> R.H.S loss term [kg / (s*m^2)]
    """
    keys = ['B', 'G','M', 'no3', 'temp', 'PAR']
    key_types = [np.zeros(nt) for n in range(len(keys))]
    dict_out = add_keys_var_dict(keys,key_types, mdict)
    return dict_out


      ############################################################
      #             SAVE SOLUTION DICTIONARY WITH PICKLE
      ############################################################

def change_dir_py(dir_name):
     if not os.path.exists(dir_name):
        print('Creating directory: ' + dir_name)
        os.makedirs(dir_name)
     print('Moving into directory: ' + dir_name)
     os.chdir(dir_name)
     ##########################################

def save_to_pickle(var_dict,out_name):
    pickle.dump(var_dict,open(out_name +".p", "wb"))
    print('Saved output as: ' + out_name + '.p')
    #####################################################

def write_to_nc(mdict, sim_name):
    '''
    Write ouptut to netcdf
    '''
    nt = len(mdict['tvec'])
    
    ncout = netcdf(sim_name + '_momag.nc', 'w')
    print('')
    print ('Writing to netcdf: ' + sim_name + '_momag.nc')
    print('')
    
    ncout.title='MoMAG output file'
    ncout.date=date.today().strftime("%B %d, %Y")

    #SET DIMENSIONS
    ncout.createDimension('time', None)

    #CREATE AND WRITE VARIABLES
    tvec_nc = ncout.createVariable('tvec', 'f8', ('time'))
    setattr(tvec_nc, 'long_name', 'time since initialization')
    setattr(tvec_nc, 'units', 'seconds')
    tvec_nc[:] = mdict['tvec'][:]

    B_nc = ncout.createVariable('B', 'f4', ('time'))
    setattr(B_nc, 'long_name', 'biomass')
    setattr(B_nc, 'units', 'kg / m^2')
    B_nc[:] = mdict['B'][:]

    G_nc = ncout.createVariable('Gr', 'f4', ('time'))
    setattr(G_nc, 'long_name', 'growth rate')
    setattr(G_nc, 'units', '[1/s]')
    G_nc[:] = mdict['G'][:]

    M_nc = ncout.createVariable('Mort', 'f4', ('time'))
    setattr(M_nc, 'long_name', 'mortality rate')
    setattr(M_nc, 'units', '[1/s]')
    M_nc[:] = mdict['M'][:]
    

    ncout.close()
    #################################################


      ############################################################
      #             Housekeping subroutines
      ############################################################

def create_tvec(tend,dt):
    '''
    Create time array [seconds]

    Inputs
    tend --> length of time of run [seconds]
    dt   --> time-step interval [seconds]

    Returns
    tvec --> 1D array of model time [seconds since 0]
    '''
    return np.arange(0,tend+dt,dt)


      ############################################################
      #             TIME-STEPPING SUBROUTINES
'''
               Functions to compute R.H.S terms 
               Functions to time-step
'''
      ############################################################

def compute_growth(no3,temp,PAR,Gmax=1.):
    '''
    Compute growht rate [1/s] at a time-step as a function of
    nutrient (no3), light (PAR), and temperature

    G = Gmax *  (Gno3 * GPAR * Gtemp)

    Inputs
    no3 --> float or 1D array [mg N / m^2]
    PAR --> float or 1D array[UNITS]
    temp --> float or 1D array [deg c]

    Returns
    growth rate (G) --> float or 1D array [1/s]
    '''
    #Temporary
    Gno3 = 1
    GPAR = 1
    Gtemp = 1
    return Gmax * Gno3 * GPAR * Gtemp
    ###################################################


def compute_loss(M0=0.0):
    '''
    Compute mortality (loss) rate

    Inputs

    Returns
    loss rate --> float or 1D array [1/s]
    '''
    return M0
    ##############################################


def time_step(mdict):
    '''
    Time step equations
    '''    
    nt = len(mdict['tvec'])

    #Assign some local variables
    no3  = mdict['no3']
    temp = mdict['temp']
    PAR  = mdict['PAR']
    Gmax = mdict['Gmax']
    L0   = mdict['L0']
    
    #Coefficients for 3rd order Adams Bashforth 
    ab3_1 = 23./12.
    ab3_2 = -4./3.
    ab3_3 = 5./12.

    for n in range(nt-1):
        #Compute growth and loss rates at time-step = n
        mdict['G'][n] = compute_growth(no3[n], temp[n], PAR[n],Gmax=Gmax)
        mdict['M'][n] = compute_loss(M0=L0)
        if n<=2:
           #Forward euler for first 2 time-ste[s
           RHS = mdict['G'][n]*mdict['B'][n] - mdict['M'][n]*mdict['B'][n]**2
        else:
            #AB3 time-step
            #Extrapolate R.H.S
            RHS = ab3_1 * (mdict['G'][n] * mdict['B'][n] - mdict['M'][n] * mdict['B'][n]**2) \
                + ab3_2 * (mdict['G'][n-1] * mdict['B'][n-1] - mdict['M'][n-1] * mdict['B'][n-1]**2) \
                + ab3_3 * (mdict['G'][n-2] * mdict['B'][n-2] - mdict['M'][n-2] * mdict['B'][n-2]**2) \

        #Time-step
        print('Time-stepping B at t=' + str(n))
        #print('RHS=') + str(RHS[n])
        mdict['B'][n+1] = mdict['B'][n] + mdict['dt'] * RHS


    #Calculate rates for last time-step
    mdict['G'][n+1] = compute_growth(no3[n+1], temp[n+1], PAR[n+1],Gmax=Gmax)
    mdict['M'][n+1] = compute_loss(M0=L0)
    #Return dictionary with updated arrays
    return mdict
    #############################################
     







