'''
Create `forcing' file in netcdf format
for MoMAG model

This is basically just for testing, so forcing here
is created synthetically to build up I/O of PyMoMAG

Forcing file should contain time-series
or (z,t) arrays of the following environmental
variables

nitrate     : no3 --> [mmol N / m^2]
temperature : temp --> [deg C]
light       : PAR --> [W/m^2]
'''
#########################################
#IMPORT MODULES
import numpy as np
from netCDF4 import Dataset as netcdf
from datetime import date
#########################################

#Some parameters to create forcing time-series
#time-interval between forcing
frc_name = 'test'
dt = 86400 #[seconds]
tend = 360 #[days]

#Make time-vector [seconds]
tvec = np.arange(0,(tend*86400)+dt,dt)
nt = len(tvec)

#Make forcing dictionary
frc_dict = {}
keys_frc = ['no3', 'temp', 'PAR']
for ke in range(len(keys_frc)):
    frc_dict[keys_frc[ke]] = np.zeros(nt)

#For now (testing), leave PAR and temp = 0

#Make some quasi-seasonal NO3 cycle
no30 = 2. #mmol / m^2
#Period = 1 year
T = 86400 * 360
frc_dict['no3'] = no30/2. * (1+np.cos((2*np.pi / T)* tvec))

#Write to netcdf
ncout = netcdf(frc_name + '_frc.nc', 'w')
print('')
print ('Writing to netcdf: ' + frc_name + '_frc.nc')
print('')
    
ncout.title='MoMAG forcing (input) file'
ncout.date=date.today().strftime("%B %d, %Y")

#SET DIMENSIONS
ncout.createDimension('frc_time', None)

#CREATE AND WRITE VARIABLES
tvec_nc = ncout.createVariable('frc_time', 'f4', ('frc_time'))
setattr(tvec_nc, 'long_name', 'forcing time')
setattr(tvec_nc, 'units', 'seconds')
tvec_nc[:] = tvec

no3_nc = ncout.createVariable('no3', 'f4', ('frc_time'))
setattr(no3_nc, 'long_name', 'nitrate')
setattr(no3_nc, 'units', 'mmol N / m^2')
no3_nc[:] = frc_dict['no3'][:]

temp_nc = ncout.createVariable('temp', 'f4', ('frc_time'))
setattr(temp_nc, 'long_name', 'temperature')
setattr(temp_nc, 'units', 'deg C')
temp_nc[:] = frc_dict['temp'][:]

PAR_nc = ncout.createVariable('PAR', 'f4', ('frc_time'))
setattr(PAR_nc, 'long_name', 'photosynthetically active radiation')
setattr(PAR_nc, 'units', 'W/m^2')
PAR_nc[:] = frc_dict['PAR'][:]

ncout.close()







