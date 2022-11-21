#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

'''
TODO: consider adding the SOC lookup table and choose the N2O emission factor
depending on the region of interest.

PAUSED AT ADDING RESULTS FOR CORN
'''

from . import default_inputs, Inputs, Results, Var

__all__ = ('CornInputs', 'CornResults', 'default_corn_inputs',)

default_corn_inputs = [
    *default_inputs,
    # Yield
    Var('CornYield_TS', 178.4, 'bu/acre'),
    # Energy
    Var('Diesel_CornFarming_val', 7.2216825542863, 'gal/acre'),
    Var('Gasoline_CornFarming_val', 1.27596490556539, 'gal/acre'),
    Var('NG_CornFarming_val', 86.9829190935403, 'ft3/acre'),
    Var('LPG_CornFarming_val', 2.15424982868667, 'gal/acre'),
    Var('Electricity_CornFarming_val', 69.3252376020865, 'kWh/acre'),
    # Nitrogen Fertilizer
    Var('Ammonia_CornFarming_val', 48.9509278781036, 'lbs N/acre'),
    Var('Urea_CornFarming_val', 36.3184303611737, 'lbs N/acre'),
    Var('AN_CornFarming_val', 3.15812437923246, 'lbs N/acre'),
    Var('AS_CornFarming_val', 3.15812437923246, 'lbs N/acre'),
    Var('UAN_CornFarming_val', 50.5299900677199, 'lbs N/acre'),
    Var('MAP_CornFarming_asNfert_val', 6.31624875846498, 'lbs N/acre'),
    Var('DAP_CornFarming_asNfert_val', 9.47437313769748, 'lbs N/acre'),
    # Phosphorus Fertilizer
    Var('MAP_CornFarming_asPfert_val', 29.6214547451708, 'lbs P2O5/acre'),
    Var('DAP_CornFarming_asPfert_val', 29.6214547451708, 'lbs P2O5/acre'),
    # Potash Fertilizer
    Var('K2O_CornFarming_val', 59.9160589286196, 'lbs K2O/acre'),
    # Lime
    Var('CaCO3_CornFarming_val', 573.031087811272, 'lbs K2O/acre'),
    # Herbicide
    Var('HerbicideUse_CornFarming_val', 1044.16660544699, 'g/acre'),
    # Insecticide
    Var('InsecticideUse_CornFarming_val', 2.22773747570338, 'g/acre'),
    # Cover crop
    Var('CC_Choice', 'No cover crop', notes='Can only be "Cover crop" or "No cover crop".'),
    Var('Diesel_RyeCCFarming_val', 62060, 'Btu/acre'),
    Var('HerbicideUse_RyeCCFarming_val', 612.3496995, 'g/acre'),
    Var('RyeCCfarming_Ninbiomass_residue_val', 1.21405880091459, 'dry ton/acre'),
    # Tillage
    Var('Tillage_Choice', 'Reduced tillage',
        notes='Can only be one of "Conventional tillage", "Reduced tillage", or "No till".'),
    # Manure
    Var('Manure_Choice', 'No manure', notes='Can only be "Manure" or "No manure".'),
    Var('Manure_AppTot', 7.854, 'ton/acre'),
    Var('Manure_AppRatio_Swine', 0.243, 'fraction'),
    Var('Manure_AppRatio_Dairy', 0.423, 'fraction'),
    Var('Manure_AppRatio_Cattle', 0.216, 'fraction'),
    Var('Manure_AppRatio_Chicken', 0.119, 'fraction'),
    Var('Diesel_ManureApplication_val', 221365.589648777, 'Btu/acre'),
    Var('Diesel_ManureTransportation_distance', 0.367, 'mile'),
    Var('Diesel_ManureTransportation_fuel', 10416.49299, 'Btu/ton/mile'),
    # Related to the regionalized N2O emission factors table
    Var('Climate_zone', 'No consideration',
        notes='Can only be one of "No consideration", "NA", "Wet or Moist", or "Dry".'),
    # Related to the 4R nitrogen management practice for corn farming
    Var('N_balance_assumed', 0, 'kg N/ha'),
    Var('N_management_corn', 'Business as usual',
        notes='Can only be one of "Business as usual", '
        '"4R (Right time, Right place, Right form, and Right rate)", '
        'or "Enhanced Efficiency Fertilizer".'),
    Var('Nfertilizer_source_corn', 'Conventional',
        notes='Can only be "Conventional" (steam methane reforming) or '
        '"Green" (refer to GREET for the default green ammonia pathway).'),
    # SOC
    Var('SOC_emission', 0.5, 'kg C/ha/yr',
        notes='Positive is emission, negative is sequestration.'),
    # Ethanol yield, default from GREET pathway
    Var('Ethanol_yield', 2.88220583817581, 'gal/bu',
        notes='Dry mill with corn oil extraction, default value from GREET.'),
    ]


class CornInputs(Inputs):
    '''User inputs for corn.'''
    
    def __init__(self, inputs=[]):
        self.inputs = inputs or default_corn_inputs
        self.reset_variables()

    
    @property
    def crop(self):
        return 'Corn'

    @property
    def Nfertilizer_source_corn(self):
        '''Same as `Nfertilizer_source`.'''
        return self.Nfertilizer_source
    @Nfertilizer_source_corn.setter
    def Nfertilizer_source_corn(self, i):
        self.Nfertilizer_source = i
        
    @property
    def Yield_TS(self):
        '''Same as `CornYield_TS`.'''
        return self.CornYield_TS
    @Yield_TS.setter
    def Yield_TS(self, i):
        self.CornYield_TS = i

#!!! PAUSED HERE, NEED TO DROP THE CROP TYPE WHEN ADDING FORMULA
class CornResults(Results):
    '''Result calculation for corn.'''
    