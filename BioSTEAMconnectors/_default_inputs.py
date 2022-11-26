#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

'''Default input values in FDCIC'''

from . import Variable

__all__ = (
    'default_corn_inputs',
    'default_rice_inputs',
    )

default_inputs = [    
    Variable('Nfertilizer_source', 'Conventional',
        notes='Can only be "Conventional" (steam methane reforming) or '
        '"Green" (refer to GREET for the default green ammonia pathway).'),
    ]


# %%

default_corn_inputs = [
    *default_inputs,
    # Yield
    Variable('CornYield_TS', 178.4, 'bu/acre'),
    # Energy
    Variable('Diesel_CornFarming_val', 7.2216825542863, 'gal/acre'),
    Variable('Gasoline_CornFarming_val', 1.27596490556539, 'gal/acre'),
    Variable('NG_CornFarming_val', 86.9829190935403, 'ft3/acre'),
    Variable('LPG_CornFarming_val', 2.15424982868667, 'gal/acre'),
    Variable('Electricity_CornFarming_val', 69.3252376020865, 'kWh/acre'),
    # Nitrogen Fertilizer
    Variable('Ammonia_CornFarming_val', 48.9509278781036, 'lbs N/acre'),
    Variable('Urea_CornFarming_val', 36.3184303611737, 'lbs N/acre'),
    Variable('AN_CornFarming_val', 3.15812437923246, 'lbs N/acre'),
    Variable('AS_CornFarming_val', 3.15812437923246, 'lbs N/acre'),
    Variable('UAN_CornFarming_val', 50.5299900677199, 'lbs N/acre'),
    Variable('MAP_CornFarming_asNfert_val', 6.31624875846498, 'lbs N/acre'),
    Variable('DAP_CornFarming_asNfert_val', 9.47437313769748, 'lbs N/acre'),
    # Phosphorus Fertilizer
    Variable('MAP_CornFarming_asPfert_val', 29.6214547451708, 'lbs P2O5/acre'),
    Variable('DAP_CornFarming_asPfert_val', 29.6214547451708, 'lbs P2O5/acre'),
    # Potash Fertilizer
    Variable('K2O_CornFarming_val', 59.9160589286196, 'lbs K2O/acre'),
    # Lime
    Variable('CaCO3_CornFarming_val', 573.031087811272, 'lbs K2O/acre'),
    # Herbicide
    Variable('HerbicideUse_CornFarming_val', 1044.16660544699, 'g/acre'),
    # Insecticide
    Variable('InsecticideUse_CornFarming_val', 2.22773747570338, 'g/acre'),
    # Cover crop
    Variable('CC_Choice', 'No cover crop', notes='Can only be "Cover crop" or "No cover crop".'),
    Variable('Diesel_RyeCCFarming_val', 62060, 'Btu/acre'),
    Variable('HerbicideUse_RyeCCFarming_val', 612.3496995, 'g/acre'),
    Variable('RyeCCfarming_Ninbiomass_residue_val', 1.21405880091459, 'dry ton/acre'),
    # Tillage
    Variable('Tillage_Choice', 'Reduced tillage',
             notes='Can only be one of "Conventional tillage", "Reduced tillage", or "No till".'),
    # Manure
    Variable('Manure_Choice', 'No manure', notes='Can only be "Manure" or "No manure".'),
    Variable('Manure_AppTot', 7.854, 'ton/acre'),
    Variable('Manure_AppRatio_Swine', 0.243, 'fraction'),
    Variable('Manure_AppRatio_Dairy', 0.423, 'fraction'),
    Variable('Manure_AppRatio_Cattle', 0.216, 'fraction'),
    Variable('Manure_AppRatio_Chicken', 0.119, 'fraction'),
    Variable('Diesel_ManureApplication_val', 221365.589648777, 'Btu/acre'),
    Variable('Diesel_ManureTransportation_distance', 0.367, 'mile'),
    Variable('Diesel_ManureTransportation_fuel', 10416.49299, 'Btu/ton/mile'),
    # Related to the regionalized N2O emission factors table
    Variable('Climate_zone', 'No consideration',
             notes='Can only be one of "No consideration", "NA", "Wet or Moist", or "Dry".'),
    # Related to the 4R nitrogen management practice for corn farming
    Variable('N_balance_assumed', 0, 'kg N/ha'),
    Variable('N_management_corn', 'Business as usual',
            notes='Can only be one of "Business as usual", '
            '"4R (Right time, Right place, Right form, and Right rate)", '
            'or "Enhanced Efficiency Fertilizer".'),
    # SOC
    Variable('SOC_emission', 0.476628350205226, 'kg C/ha/yr', # Champaign, IL
        notes='Positive is emission, negative is sequestration.'),
    # Ethanol yield, default from GREET pathway
    Variable('Ethanol_yield', 2.88220583817581, 'gal/bu',
             notes='Dry mill with corn oil extraction, default value from GREET.'),
    ]


# %%

#!!! NOT YET READY
default_rice_inputs = [
    *default_inputs,
    # Related to the regionalized N2O emission factors table
    Variable('Nfertilizer_N2O_factor_US_rice', 0.004+0.00374, notes='direct and indirect'),
    # Related to the N content of above and below ground biomass and N2O Emission 
    Variable('Rice_water_regime_during_cultivation', 'Continuously flooded',
             notes='Can only be one of "Continuously flooded", "Single drainage period", '
            '"Multiple drainage period", "Regular rainfed", "Drought prone", or "Deep water".'),
    Variable('Rice_water_regime_pre_season', 'Non flooded pre-season >365 d',
             notes='Can only be one of "Non flooded pre-season <180 d", "Non flooded pre-season >180 d", '
             '"Flooded pre-season (>30 d)", or "Non-flooded pre-season >365 d".'),
    Variable('Rice_time_for_straw_incorporation',
            'Straw incorporated shortly (<30 days) before cultivation',
            notes='Can only be "Straw incorporated shortly (<30 days) before cultivation" or '
            '"Straw incorporated long (>30 days) before cultivation"'),
    ]
