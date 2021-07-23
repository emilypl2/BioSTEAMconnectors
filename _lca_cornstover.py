#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 20:28:14 2021

@author: Yalin Li

Some of the codes are from the lactic and HP biorefineries in
Bioindustrial-Park: BioSTEAM's Premier Biorefinery Models and Results
https://github.com/BioSTEAMDevelopmentGroup/Bioindustrial-Park
"""

import thermosteam as tmo
from biorefineries import cornstover as cs

chems = cs.chemicals

# 100-year global warming potential (GWP) in kg CO2-eq/kg dry material,
# all data from GREET 2020
GWP_CFs = {
    'NH4OH': 2.64 * chems.NH3.MW/chems.NH4OH.MW,
    'CSL': 1.55,
    'CH4': 0.33, # NA NG from shale and conventional recovery
    'Cellulase': 2.24, # enzyme
    'Lime': 1.29,
    'NaOH': 2.11,
    'H2SO4': 0.04344,
    # 'Ethanol': 1.44,
    'Denaturant': 0.84, # gasoline blendstock from crude oil for use in US refineries
    }

# This makes the CF into an array
GWP_CF_array = chems.kwarray(GWP_CFs)
GWP_CF_stream = tmo.Stream('GWP_CF_stream', GWP_CF_array, units='kg/hr')

GWP_CFs['Electricity'] = 0.48 # kg CO2-eq/kWh

# Everything excluding farming
# (farming = soil emissions + field chemicals + field operations),
# the rest from DayCent/assumptions in the spreadsheet
# Table S6 from Wendt et al., Techno-Economic Assessment of a Chopped Feedstock
# Logistics Supply Chain for Corn Stover. Front. Energy Res. 2018, 6.
# https://doi.org/10.3389/fenrg.2018.00090.
GWP_CFs['Cornstover'] = 68.82/1e3