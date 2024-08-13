# PyMoMAG
Very simple macroalgal growth model that evolves a biomass $B$ as follows:

```math
\frac{dB}{dt} = GB - MB^2
```
where $G,M$ are growth and mortality rates, heavily informed by SBC LTER data from MoHawk Reef (for now).

To run the model:
- put forcing (nitrate, temp, PAR) into a netcdf
  - this can be done for testing (synthetically) with `create_magfrc.py`
- edit the configuration file `params.config`
- run from command line as: `python3 main.py params.config`
- model will write output to a netcdf file

Make sure you are using python3 and have appropriate libraries installed.
