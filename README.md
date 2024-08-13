# PyMoMAG
Very simple macroalgal growth model that evolves a biomass $B$ as follows:

```math
\frac{dB}{dt} = GB - MB^2
```
where $G,M$ are growth and mortality rates, heavily informed by SBC LTER data from MoHawk Reef (for now).

Before running MAG:
- put forcing (nitrate, temp, PAR) into a netcdf
  - this can be done for testing (synthetically) with `create_magfrc.py`
  -   just run python3 create_magfrc.py from a command line, this will create a netcdf file called `test_frc.nc`

To run MAG:
- edit the configuration file `params.config`
- run from command line as: `python3 main.py params.config`
- model will write output to a netcdf file

Make sure you are using python3 and have appropriate libraries installed.
