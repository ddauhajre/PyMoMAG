# PyMoMAG
Very simple macroalgal growth model that evolves a biomass $B$ as follows:
$\partial B / \partial t = GB - MB^2$, where $G,M$ are growth and mortality rates, heavily informed by SBC LTER data from MoHawk Reef (for now).

To run the model:
- edit the configuration file `params.config`
- run from command line as: python3 main.py params.config

Make sure you are using python3 and have appropriate libraries installed.
