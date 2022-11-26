#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

'''
TODO: could consider using openpyxl to get the cell range values from FDCIC/GREET.
Note that some cells have alternative names in FDCIC

Note: Canadian corn not included at this stage.
'''

import pandas as pd
from math import e
from . import default_parameters, Variable, Variables

__all__ = ('FDCIC', 'Variable', 'Variables')





# %%

class FDCIC(Variables):
    '''
    A general class to calculate feedstock carbon intensity and cost as in
    GREET's feedstock carbon intensitity calculator.
    
    Parameters
    ----------
    crop_inputs : :class:`CropInputs`
        Object containing crop inputs.
    '''
    
    parameters = default_parameters
    
    def __init__(self, crop_inputs):
        self.crop_inputs = crop_inputs
        self.reset_variables()

    @property
    def crop(self):
        '''Name of the crop of interest.'''
        return self.crop_inputs.crop
    
    @property
    def GHG_functional_unit(self):
        '''Functional unit of the GHG results for the crop of interest.'''
        return self.crop_inputs.GHG_functional_unit
    
    @property
    def inputs(self):
        '''Crop-specific inputs.'''
        return self.crop_inputs.inputs

    @property
    def variables(self):
        if hasattr(self, '_variables'):
            dct = self._variables
            dct.empty()
            dct.update(self.parameters)
        else:
            self._variables = dct = self.parameters.copy()
        dct.update(self.crop_inputs.inputs)
        return dct
    
    # Universal Aliases
    @property
    def g_to_lb(self):
        '''Same as `g_per_lb`.'''
        return self.g_per_lb
    
    @property
    def btu_to_MJ(self):
        '''Same as `Btu_per_MJ`.'''
        return self.Btu_per_MJ
    
    @property
    def tonne2lb(self):
        '''Same as `tonne_per_lb`.'''
        return self.tonne_per_lb

    @property
    def kg_to_lb(self):
        '''Same as `kg_per_lb`.'''
        return self.kg_per_lb
    
    @property
    def L_to_gal(self):
        '''Same as `L_per_gal`.'''
        return self.L_per_gal
    
    @property
    def ac_per_ha(self):
        '''Same as `acre_per_hectare`.'''
        return self.acre_per_hectare
    acre2hectare = ac_per_ha

    @property
    def kg2g(self):
        '''Same as `g_per_kg`.'''
        return self.g_per_kg

    @property
    def MJ2kJ(self):
        '''Same as `kJ_per_MJ`.'''
        return self.kJ_per_MJ
    
    @property
    def kWh2kJ(self):
        '''Same as `kJ_per_kWh`.'''
        return self.kJ_per_kWh

    @property
    def GJ2kJ(self):
        '''Same as `kJ_per_GJ`.'''
        return self.kJ_per_GJ
    
    @property
    def ton2g(self):
        '''Same as `g_per_ton`.'''
        return self.g_per_ton

    @property
    def Urea_content_in_UAN(self):
        '''Same as `UAN_Prod_UreaIn`.'''
        return self.UAN_Prod_UreaIn
    
    # Characterization factors
    def _get_NG_Elec_source(self):
        return 'Ammonia', '' if self.crop != 'BrazilianSugarcane' else 'StationaryFuel', 'Brazilian_'
    
    @property
    def _CF_Ammonia_shared(self):
        ammonia_type = self.Nfertilizer_source
        if ammonia_type not in ('Conventional', 'Green'):
            raise ValueError(f'{ammonia_type} is invalid for `Nfertilizer_source`, '
                             'check `crop_inputs.Nfertilizer_source.notes` for valid values.')
        prefix = '' if ammonia_type == 'Conventional' else 'Green_'
        vals = [
            getattr(self, f'{prefix}Ammonia_Prod_NGIn'),
            getattr(self, f'{prefix}Ammonia_Prod_ElecIn'),
            getattr(self, f'{prefix}Ammonia_Prod_HydrogenIn'),
            getattr(self, f'{prefix}Ammonia_Prod_NitrogenIn'),
            getattr(self, f'{prefix}Ammonia_InputsCons_GHG'),
            ]
        NG, Elec = self._get_NG_Elec_source()
        CO2 = (
            vals[0]*getattr(self, f'NG_upstream_CO2_for_{NG}') +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_CO2') +
            vals[2]*self.H2_upstream_CO2 +
            vals[3]*self.Cryogenic_Nitrogen_for_Ammonia_CO2
            )
        CH4 = (
            vals[0]*getattr(self, f'NG_upstream_CH4_for_{NG}') +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_CH4') +
            vals[2]*self.H2_upstream_CH4 +
            vals[3]*self.Cryogenic_Nitrogen_for_Ammonia_CH4
            )
        N2O = (
            vals[0]*getattr(self, f'NG_upstream_N2O_for_{NG}') +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_N2O') +
            vals[2]*self.H2_upstream_N2O +
            vals[3]*self.Cryogenic_Nitrogen_for_Ammonia_N2O
            )
        return CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP
    
    @property
    def CF_Ammonia_Final(self):
        '''In g GHG/ton ammonia.'''
        return self._CF_Ammonia_shared + self.Ammonia_TD_GHG_Final
    
    @property
    def CF_Ammonia_Intermediate(self):
        '''In g GHG/ton ammonia.'''
        return self._CF_Ammonia_shared + self.Ammonia_TD_GHG_Intermediate
    
    @property
    def CF_Urea(self):
        '''In g GHG/ton.'''
        vals = [
            self.Urea_Prod_NGIn,
            self.Urea_Prod_ElecIn,
            self.Urea_Prod_AmmoniaIn,
            ]
        NG, Elec = self._get_NG_Elec_source()
        CO2 = (
            vals[0]*self.NG_upstream_CO2_for_StationaryFuel +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_CO2')
            )
        CH4 = (
            vals[0]*self.NG_upstream_CH4_for_StationaryFuel +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_CH4')
            )
        N2O = (
            vals[0]*self.NG_upstream_N2O_for_StationaryFuel +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_N2O')
            )
        return (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            vals[2]*self.CF_Ammonia_Intermediate +
            self.Urea_InputsCons_GHG + self.Urea_Process_GHG + self.Urea_TD_GHG_Final
            )
    
    @property
    def CF_NA(self):
        '''In g GHG/ton.'''
        vals = [
            self.NA_ElecIn,
            self.NA_AmmoniaIn,
            ]
        CO2 = vals[0]*self.Electricity_upstream_CO2
        CH4 = vals[0]*self.Electricity_upstream_CH4
        N2O = vals[0]*self.Electricity_upstream_N2O
        return (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            vals[1]*self.CF_Ammonia_Intermediate +
            self.NA_Process_GHG + self.NA_TD_GHG_Final
            )
    
    @property
    def CF_AN(self):
        '''In g GHG/ton.'''
        vals = [
            self.AN_Prod_NGIn,
            self.AN_Prod_ElecIn,
            self.AN_Prod_AmmoniaIn,
            self.AN_Prod_NAIn,
            ]
        NG, Elec = self._get_NG_Elec_source()
        CO2 = (
            vals[0]*self.NG_upstream_CO2_for_StationaryFuel +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_CO2')
            )
        CH4 = (
            vals[0]*self.NG_upstream_CH4_for_StationaryFuel +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_CH4')
            )
        N2O = (
            vals[0]*self.NG_upstream_N2O_for_StationaryFuel +
            vals[1]*getattr(self, f'Electricity_{Elec}upstream_N2O')
            )
        GHG = (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            vals[2]*self.CF_Ammonia_Intermediate +
            self.AN_InputsCons_GHG + self.AN_TD_GHG_Final
            )
        if 'Brazilian' not in self.crop: return GHG + vals[3]*self.CF_NA
        return GHG + self.NA_Prod_AmmoniaIn*self.CF_Ammonia_Intermediate
    
    @property
    def CF_AS(self):
        '''In g GHG/ton.'''
        vals = [
            self.AS_Prod_AmmoniaIn,
            self.AS_Prod_SAIn,
            ]
        CO2 = vals[1]*self.SA_Upstream_CO2
        CH4 = vals[1]*self.SA_Upstream_CH4
        N2O = vals[1]*self.SA_Upstream_N2O
        return (
            vals[0]*self.CF_Ammonia_Intermediate +
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            self.AS_TD_GHG_Final
            )
    
    @property
    def CF_UAN(self):
        '''In g GHG/ton.'''
        vals = [
            self.UAN_Prod_NGIn,
            self.UAN_Prod_ElecIn,
            self.UAN_Prod_UreaIn,
            self.UAN_Prod_ANIn,
            ]
        CO2 = (
            vals[0]*self.NG_upstream_CO2_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_CO2
            )
        CH4 = (
            vals[0]*self.NG_upstream_CH4_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_CH4
            )
        N2O = (
            vals[0]*self.NG_upstream_N2O_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_N2O
            )
        return (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            vals[2]*self.CF_Urea + vals[3]*self.CF_AN +
            self.UAN_InputsCons_GHG + self.UAN_TD_GHG_Final
            )
    
    def _get_MAP_DAP_CF(self, prefix='M'):
        vals = [
            getattr(self, f'{prefix}AP_Prod_NGIn'),
            getattr(self, f'{prefix}AP_Prod_ElecIn'),
            getattr(self, f'{prefix}AP_Prod_AmmoniaIn'),
            getattr(self, f'{prefix}AP_Prod_PAIn'), # already adjusted to P2O5
            getattr(self, f'{prefix}AP_InputsCons_GHG'),
            getattr(self, f'{prefix}AP_TD_GHG_Final'),
            ]
        CO2 = (
            vals[0]*self.NG_upstream_CO2_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_CO2 +
            vals[3]*self.PA_Upstream_CO2
            )
        CH4 = (
            vals[0]*self.NG_upstream_CH4_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_CH4 +
            vals[3]*self.PA_Upstream_CH4
            )
        N2O = (
            vals[0]*self.NG_upstream_N2O_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_N2O +
            vals[3]*self.PA_Upstream_N2O
            )
        return (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            vals[2]*self.CF_Ammonia_Intermediate +
            self.MAP_InputsCons_GHG + self.MAP_TD_GHG_Final
            )
    
    @property
    def CF_MAP(self):
        '''In g GHG/ton.'''
        return self._get_MAP_DAP_CF('M')
    
    @property
    def CF_DAP(self):
        '''In g GHG/ton.'''
        return self._get_MAP_DAP_CF('D')
    
    @property
    def CF_P2O5(self):
        '''For Brazilian sugarcane, in g GHG/ton.'''
        vals = [
            self.PA_Brazilian_Prod_ElecIn,
            self.PA_Brazilian_Prod_PhosRockIn,
            self.PA_Brazilian_Prod_SAIn,
            ]
        CO2 = (
            vals[0]*self.Electricity_Brazilian_upstream_CO2 +
            vals[1]*self.PhosRock_Brazilian_Upstream_CO2 +
            vals[2]*self.SA_Brazilian_Upstream_CO2
            )
        CH4 = (
            vals[0]*self.Electricity_Brazilian_upstream_CH4 +
            vals[1]*self.PhosRock_Brazilian_Upstream_CH4 +
            vals[2]*self.SA_Brazilian_Upstream_CH4
            )
        N2O = (
            vals[0]*self.Electricity_Brazilian_upstream_N2O +
            vals[1]*self.PhosRock_Brazilian_Upstream_N2O +
            vals[2]*self.SA_Brazilian_Upstream_N2O
            )
        return (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            self.PA_InputsCons_GHG + self.PA_TD_GHG_Final
            )
    
    @property
    def CF_K2O(self):
        '''In g GHG/ton.'''
        vals = [
            self.K2O_Prod_NGIn,
            self.K2O_Prod_ElecIn,
            self.K2O_Prod_DieselIn,
            ]
        CO2 = (
            vals[0]*self.NG_upstream_CO2_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_CO2 +
            vals[2]*self.Diesel_upstream_CO2
            )
        CH4 = (
            vals[0]*self.NG_upstream_CH4_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_CH4 +
            vals[2]*self.Diesel_upstream_CH4
            )
        N2O = (
            vals[0]*self.NG_upstream_N2O_for_StationaryFuel +
            vals[1]*self.Electricity_upstream_N2O +
            vals[2]*self.Diesel_upstream_N2O
            )
        return (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            self.K2O_InputsCons_GHG + self.K2O_TD_GHG_Final
            )
    
    @property
    def CF_Lime(self):
        '''CaCO3, in g GHG/ton.'''
        if 'Brazilian' not in self.crop:
            vals = [
                self.Lime_Prod_NGIn,
                self.Lime_Prod_ElecIn,
                self.Lime_Prod_ROIn,
                self.Lime_Prod_DieselIn,
                self.Lime_Prod_CoalIn,
                self.Lime_Prod_GasolineIn,
                ]
            CO2 = (
                vals[0]*self.NG_upstream_CO2_for_StationaryFuel +
                vals[1]*self.Electricity_upstream_CO2 +
                vals[2]*self.RO_upstream_CO2 +
                vals[3]*self.Diesel_upstream_CO2+
                vals[4]*self.Coal_upstream_CO2 +
                vals[5]*self.GB_upstream_CO2
                )
            CH4 = (
                vals[0]*self.NG_upstream_CH4_for_StationaryFuel +
                vals[1]*self.Electricity_upstream_CH4 +
                vals[2]*self.RO_upstream_CH4 +
                vals[3]*self.Diesel_upstream_CH4+
                vals[4]*self.Coal_upstream_CH4 +
                vals[5]*self.GB_upstream_CH4
                )
            N2O = (
                vals[0]*self.NG_upstream_N2O_for_StationaryFuel +
                vals[1]*self.Electricity_upstream_N2O +
                vals[2]*self.RO_upstream_N2O +
                vals[3]*self.Diesel_upstream_N2O+
                vals[4]*self.Coal_upstream_N2O +
                vals[5]*self.GB_upstream_N2O
                )
            return (
                CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
                self.Lime_InputsCons_GHG + self.Lime_TD_GHG_Final
                )
        vals = [
            self.Lime_Brazilian_Prod_ElecIn,
            self.Lime_Brazilian_Prod_DieselIn,
            ]
        CO2 = (
            vals[0]*self.Electricity_Brazilian_upstream_CO2 +
            vals[1]*self.Diesel_upstream_CO2
            )
        CH4 = (
            vals[0]*self.Electricity_Brazilian_upstream_CH4 +
            vals[1]*self.Diesel_upstream_CH4
            )
        N2O = (
            vals[0]*self.Electricity_Brazilian_upstream_N2O +
            vals[1]*self.Diesel_upstream_N2O
            )
        return (
            CO2*self.CO2_GWP + CH4*self.CH4_GWP + N2O*self.N2O_GWP +
            self.Brazilian_Lime_InputsCons_GHG + self.Lime_TD_GHG_Final
            )
    
    @property
    def CF_Diesel(self):
        '''In g GHG/Btu.'''
        GHG = (
            self.Diesel_upstream_CO2*self.CO2_GWP +
            self.Diesel_upstream_CH4*self.CH4_GWP +
            self.Diesel_upstream_N2O*self.N2O_GWP
            )
        if not 'Sugarcane' in self.crop: return GHG+self.CornFarming_DieselCons_GHG
        return GHG+self.SugarcaneFarming_DieselCons_GHG
    
    @property
    def CF_GB(self):
        '''In g GHG/Btu.'''
        return (
            self.GB_upstream_CO2*self.CO2_GWP +
            self.GB_upstream_CH4*self.CH4_GWP +
            self.GB_upstream_N2O*self.N2O_GWP +
            self.CornFarming_GBCons_GHG
            )
    
    @property
    def CF_NG(self):
        '''In g GHG/Btu.'''
        return (
            self.NG_upstream_CO2_for_StationaryFuel*self.CO2_GWP +
            self.NG_upstream_CH4_for_StationaryFuel*self.CH4_GWP +
            self.NG_upstream_N2O_for_StationaryFuel*self.N2O_GWP +
            self.CornFarming_NGCons_GHG
            )
    
    @property
    def CF_LPG(self):
        '''In g GHG/Btu.'''
        return (
            self.LPG_upstream_CO2*self.CO2_GWP +
            self.LPG_upstream_CH4*self.CH4_GWP +
            self.LPG_upstream_N2O*self.N2O_GWP +
            self.CornFarming_LPGCons_GHG
            )
    
    @property
    def CF_Electricity(self):
        '''In g GHG/Btu.'''
        crop = self.crop
        if 'Brazilian' not in crop:
            prefix = '_GSfarming' if self.crop == 'Sorghum' else ''
            return (
                getattr(self, f'Electricity_upstream_CO2{prefix}')*self.CO2_GWP +
                getattr(self, f'Electricity_upstream_CH4{prefix}')*self.CH4_GWP +
                getattr(self, f'Electricity_upstream_N2O{prefix}')*self.N2O_GWP
                )
        return (
            self.Electricity_Brazilian_upstream_CO2*self.CO2_GWP +
            self.Electricity_Brazilian_upstream_CH4*self.CH4_GWP +
            self.Electricity_Brazilian_upstream_N2O*self.N2O_GWP
            )
    
    @property
    def CF_Herbicide(self):
        '''In g GHG/g.'''
        crop = self.crop
        crop = 'GS' if crop == 'Sorghum' else crop
        try: return getattr(self, f'Herbicide_{crop}Farming_GHG')
        except AttributeError: return 0
        
    @property
    def CF_Insecticide(self):
        '''In g GHG/g.'''
        crop = self.crop
        crop = 'GS' if crop == 'Sorghum' else crop
        try: return getattr(self, f'Insecticide_{crop}Farming_GHG')
        except AttributeError: return 0
    
    # Energy and chemcial usage
    @property
    def Diesel_Farming(self):
        '''In Btu/bu.'''
        return getattr(self, f'Diesel_{self.crop}Farming_val', 0)*self.Diesel_LHV/self.crop_inputs.Yield_TS
    
    @property
    def Gasoline_Farming(self):
        '''In Btu/bu.'''
        return getattr(self, f'Gasoline_{self.crop}Farming_val', 0)*self.Gasoline_LHV/self.crop_inputs.Yield_TS
    
    @property
    def NG_Farming(self):
        '''In Btu/bu.'''
        return getattr(self, f'NG_{self.crop}Farming_val', 0)*self.NG_LHV/self.crop_inputs.Yield_TS

    @property
    def LPG_Farming(self):
        '''In Btu/bu.'''
        return getattr(self, f'LPG_{self.crop}Farming_val', 0)*self.LPG_LHV/self.crop_inputs.Yield_TS
    
    @property
    def Electricity_Farming(self):
        '''In Btu/bu.'''
        return getattr(self, f'Electricity_{self.crop}Farming_val', 0)*self.Electricity_LHV/self.crop_inputs.Yield_TS
    
    @property
    def Ammonia_Farming(self):
        '''In g N/bu.'''
        return getattr(self, f'Ammonia_{self.crop}Farming_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS
    
    @property
    def Urea_Farming(self):
        '''In g N/bu.'''
        return getattr(self, f'Urea_{self.crop}Farming_val')*self.g_to_lb/self.crop_inputs.Yield_TS
    
    @property
    def AN_Farming(self):
        '''In g N/bu.'''
        return getattr(self, f'AN_{self.crop}Farming_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS

    @property
    def AS_Farming(self):
        '''In g N/bu.'''
        return getattr(self, f'AS_{self.crop}Farming_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS

    @property
    def UAN_Farming(self):
        '''In g N/bu.'''
        return getattr(self, f'UAN_{self.crop}Farming_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS

    @property
    def MAP_Farming_asNfert(self):
        '''In g N/bu.'''
        return getattr(self, f'MAP_{self.crop}Farming_asNfert_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS

    @property
    def DAP_Farming_asNfert(self):
        '''In g N/bu.'''
        return getattr(self, f'DAP_{self.crop}Farming_asNfert_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS

    @property
    def MAP_Farming_asPfert(self):
        '''In g P2O5/bu.'''
        return getattr(self, f'MAP_{self.crop}Farming_asPfert_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS
    
    @property
    def DAP_Farming_asPfert(self):
        '''In g P2O5/bu.'''
        return getattr(self, f'DAP_{self.crop}Farming_asPfert_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS

    @property
    def K2O_Farming(self):
        '''In g K2O/bu.'''
        return getattr(self, f'K2O_{self.crop}Farming_val', 0)*self.g_to_lb/self.crop_inputs.Yield_TS
    
    @property
    def CaCO3_Farming(self):
        '''In g/bu.'''
        try: lime = getattr(self, f'CaCO3_{self.crop}Farming_val')
        except:
            try: lime = getattr(self, f'Lime_{self.crop}Farming_val')
            except: lime = 0
        return lime*self.g_to_lb/self.crop_inputs.Yield_TS
    Lime_Farming = CaCO3_Farming
    
    @property
    def HerbicideUse_Farming(self):
        '''In g/bu.'''
        return getattr(self, f'HerbicideUse_{self.crop}Farming_val', 0)/self.crop_inputs.Yield_TS
    
    @property
    def InsecticideUse_Farming(self):
        '''In g/bu.'''
        return getattr(self, f'InsecticideUse_{self.crop}Farming_val', 0)/self.crop_inputs.Yield_TS

    @property
    def Herbicide_Farming_CO2(self):
        '''In g CO2/ton.'''
        crop = self.crop
        # Rice has the same value as corn
        crop = 'Corn' if crop in ('Corn', 'Rice') else 'GS' if 'Sorghum' in crop else crop
        return getattr(self, f'Herbicide_{self.crop}Farming_CO2', 0)
    
    @property
    def Herbicide_Farming_GHG(self):
        '''In g GHG/ton.'''
        crop = self.crop
        # Rice has the same value as corn
        crop = 'Corn' if crop in ('Corn', 'Rice') else 'GS' if 'Sorghum' in crop else crop
        return getattr(self, f'Herbicide_{self.crop}Farming_GHG', 0)
    
    @property
    def Insecticide_Farming_CO2(self):
        '''In g CO2/ton.'''
        crop = self.crop
        # Rice has the same value as corn
        crop = 'Corn' if crop in ('Corn', 'Rice') else 'GS' if 'Sorghum' in crop else crop
        return getattr(self, f'Insecticide_{self.crop}Farming_CO2', 0)
    
    @property
    def Insecticide_Farming_GHG(self):
        '''In g GHG/ton.'''
        crop = self.crop
        # Rice has the same value as corn
        crop = 'Corn' if crop in ('Corn', 'Rice') else 'GS' if 'Sorghum' in crop else crop
        return getattr(self, f'Insecticide_{self.crop}Farming_GHG', 0)
    
    @property
    def Diesel_RyeCCFarming(self):
        '''In Btu per `FDCIC.GHG_functional_unit`.'''
        CC_Choice = self.CC_Choice
        if CC_Choice == 'No cover crop': return 0
        elif CC_Choice == 'Cover crop': return self.Diesel_RyeCCFarming_val/self.Yield_TS
        raise ValueError(f'{CC_Choice} is invalid for `crop_inputs.CC_Choice`, '
                         'check `crop_inputs.CC_Choice.notes` for valid values.')
    
    @property
    def HerbicideUse_RyeCCFarming(self):
        '''In g per `FDCIC.GHG_functional_unit`.'''
        CC_Choice = self.CC_Choice
        if CC_Choice == 'No cover crop': return 0
        elif CC_Choice == 'Cover crop': return self.HerbicideUse_RyeCCFarming_val/self.Yield_TS

    @property
    def RyeCCfarming_Ninbiomass_residue(self):
        '''In g N/bu.'''
        CC_Choice = self.CC_Choice
        if CC_Choice == 'No cover crop': return 0
        elif CC_Choice == 'Cover crop': return self.RyeCCfarming_Ninbiomass_residue_val/self.Yield_TS
    
    @property
    def Manure_N_inputs_Soil(self):
        '''In g N per `FDCIC.GHG_functional_unit`.'''
        Manure_Choice = self.Manure_Choice
        if Manure_Choice == 'No manure': return 0
        elif Manure_Choice == 'Manure':
            return self.Manure_AppTot * (
                self.Manure_AppRatio_Swine*self.Swine_manure_N +
                self.Manure_AppRatio_Dairy*self.Dairy_manure_N +
                self.Manure_AppRatio_Cattle*self.Cattle_manure_N +
                self.Manure_AppRatio_Chicken*self.Chicken_manure_N
                ) / self.Yield_TS
        raise ValueError(f'{Manure_Choice} is invalid for `crop_inputs.Manure_Choice`, '
                         'check `crop_inputs.Manure_Choice.notes` for valid values.') 
    
    @property
    def Diesel_ManureApplication(self):
        '''In g Btu per `FDCIC.GHG_functional_unit`.'''
        Manure_Choice = self.Manure_Choice
        if Manure_Choice == 'No manure': return 0
        elif Manure_Choice == 'Manure': return self.Diesel_ManureApplication / self.Yield_TS

    @property
    def Diesel_ManureTransportation(self):
        '''In g Btu per `FDCIC.GHG_functional_unit`.'''
        Manure_Choice = self.Manure_Choice
        if Manure_Choice == 'No manure': return 0
        elif Manure_Choice == 'Manure':
            return (
                self.Manure_AppTot * # ton/acre
                self.Diesel_ManureTransportation_distance * # mile
                self.Diesel_ManureTransportation_fuel / # Btu/ton/mile
                self.Yield_TS # bu/acre
                )
    
    # Corn
    @property
    def Nfertilizer_direct_N2O_factor_US_corn(self):
        zone = self.crop_inputs.Climate_zone
        if zone in ('No consideration', 'NA', 'Wet or Moist'): return 0.01
        elif zone == 'Dry': return 0.005
        raise ValueError(f'{zone} is invalid for `crop_inputs.Climate_zone`, '
                         'check `crop_inputs.Climate_zone.notes` for valid values.')
    
    @property
    def Nfertilizer_indirect_N2O_factor_US_corn(self):
        zone = self.crop_inputs.Climate_zone
        if zone in ('No consideration', 'NA'): return 0.00374
        elif zone == 'Wet or Moist': return 0.00418
        elif zone == 'Dry': return 0.00055
    
    @property
    def Nfertilizer_N2O_factor_US_corn(self):
        return self.Nfertilizer_direct_N2O_factor_US_corn+self.Nfertilizer_indirect_N2O_factor_US_corn
    
    @property
    def Nitrogen_balance_assumed(self):
        '''Same as `N_balance_assumed`.'''
        return self.N_balance_assumed
    
    @property
    def Nfertilizer_direct_N2O_4R_US_corn(self):
        '''N2O-N emissions under 4R practice, in g GHG per `FDCIC.GHG_functional_unit`.'''
        return e**(0.339+0.0047*self.N_balance_assumed)
    
    # Canadian Corn, not currently in use
    @property
    def lb2bu_CanCorn(self):
        '''Same as `lb_per_bu_CanCorn`.'''
        return self.lb_per_bu_CanCorn
    
    # Rice
    @property
    def SFw(self):
        '''Scaling factor to account for the differences in water regime during the cultivation period (SFw).'''
        regime = self.Rice_water_regime_during_cultivation
        if regime == 'Continuously flooded': return 1
        elif regime == 'Single drainage period': return 0.71
        elif regime == 'Multiple drainage period': return 0.55
        elif regime == 'Regular rainfed': return 0.54
        elif regime == 'Drought prone': return 0.16
        elif regime == 'Deep water': return 0.06
        raise ValueError(f'{regime} is invalid for `crop_inputs.Rice_water_regime_during_cultivation`, '
                         'check `crop_inputs.Rice_water_regime_during_cultivation.notes` for valid values.')

    @property
    def SFp(self):
        '''Scaling factor to account for the differences in water regime in the pre-season before the cultivation period (SFp).'''
        regime = self.Rice_water_regime_pre_season
        if regime == 'Non flooded pre-season <180 d': return 1
        elif regime == 'Non flooded pre-season >180 d': return 0.89
        elif regime == 'Flooded pre-season (>30 d)': return 2.41
        elif regime == 'Non-flooded pre-season >365 d': return 0.59
        raise ValueError(f'{regime} is invalid for `crop_inputs.Rice_water_regime_pre_season`, '
                         'check `crop_inputs.Rice_water_regime_pre_season.notes` for valid values.')

    @property
    def Rice_ammendment_factor(self):
        '''Conversion factor for organic amendment in terms of its relative effect with respect to straw applied shortly before cultivation.'''
        app_time = self.Rice_time_for_straw_incorporation
        if app_time == 'Straw incorporated shortly (<30 days) before cultivation': return 1 
        elif app_time == 'Straw incorporated long (>30 days) before cultivation': return 0.19
        raise ValueError(f'{app_time} is invalid for `crop_inputs.Rice_time_for_straw_incorporation`, '
                         'check `crop_inputs.Rice_time_for_straw_incorporation.notes` for valid values.')
    
    @property
    def SFo(self):
        '''Scaling factor should vary for both type and amount of organic amendment applied  (SFo).'''
        return (1+self.Rice_straw_application_rate*self.Rice_ammendment_factor)**0.59
    
    @property
    def Annual_CH4_emission_from_rice_field(self):
        '''In kg CH4/ha.'''
        return self.EFc*self.SFw*self.SFp*self.Fo*self.Rice_cultivation_period
    
    # Itemized GHG
    @property
    def Diesel_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return (#!!! Add tillage usage?
            self.Diesel_Farming +
            self.Diesel_RyeCCFarming +
            self.Diesel_ManureApplication +
            self.Diesel_ManureTransportation
            ) * self.CF_Diesel
    
    @property
    def Gasoline_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.Gasoline_Farming*self.CF_GB
    
    @property
    def NG_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.NG_Farming * self.CF_NG
    
    @property
    def LPG_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.LPG_Farming*self.CF_LPG
    
    @property
    def Electricity_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.Electricity_Farming*self.CF_Electricity
    
    @property
    def Ammonia_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.Ammonia_Farming/self.Ammonia_N*self.CF_Ammonia_Final/self.ton2g
    
    @property
    def Urea_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.Urea_Farming/self.Urea_N*self.CF_Urea/self.ton2g
    
    @property
    def AN_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.AN_Farming/self.AN_N*self.CF_AN/self.ton2g
    
    @property
    def AS_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.AS_Farming/self.AS_N*self.CF_AS/self.ton2g
    
    @property
    def UAN_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.UAN_Farming/self.UAN_N*self.CF_UAN/self.ton2g
    
    @property
    def MAP_asNfert_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.MAP_Farming_asNfert/self.MAP_N*self.CF_MAP/self.ton2g*self.MAP_share_as_Nfert
    
    @property
    def DAP_asNfert_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.DAP_Farming_asNfert/self.DAP_N*self.CF_DAP/self.ton2g*self.DAP_share_as_Nfert
    
    @property
    def N2O_Fert_and_Res_GHG(self):
        '''N2O emission due to N fertilizer and biomass residue, in g GHG per `FDCIC.GHG_functional_unit`.'''
        crop = self.crop
        Nfert = (
            self.Ammonia_Farming +
            self.Urea_Farming +
            self.AN_Farming +
            self.AS_Farming +
            self.UAN_Farming
            )

        if crop == 'Corn':
            Nfert += self.MAP_CornFarming_asNfert_val + self.DAP_CornFarming_asNfert_val
            Nfert_N2O_factor = self.Nfertilizer_N2O_factor_corn
            Nres = self.Cornfarming_Ninbiomass_residue * self.Cornfarming_biomass_N2O_factor
        else:
            #!!! TODO
            raise AttributeError(f'N in residual biomass not implemented for crop {crop}.')
            
        # crop = 'US_sorghum' if 'sorghum' in crop else 'Brazil' if 'brazil' in crop else f'US_{crop}'
        # Nfert_N2O_factor = getattr(self, f'Nfertilizer_N2O_factor_{crop}')
        
        return (
            Nfert*Nfert_N2O_factor +
            Nres +
            self.RyeCCfarming_Ninbiomass_residue*self.RyeCCfarming_biomass_N2O_factor +
            self.Manure_N_inputs_Soil*self.Manure_N2O_factor
            ) * self.N2O_GWP * self.N2O_N_to_N2O
    
    @property
    def Urea_CO2_GHG(self):
        '''CO2 emission due to urea use, in g GHG per `FDCIC.GHG_functional_unit`.'''
        return (
            self.Urea_Farming +
            self.UAN_Farming*self.UAN_Prod_UreaIn*self.Urea_N
            ) * self.Urea_N_to_CO2
    
    @property
    def MAP_asPfert_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.MAP_Farming_asPfert/self.MAP_P2O5*self.CF_MAP/self.ton2g*(1-self.MAP_share_as_Nfert)
    
    @property
    def DAP_asPfert_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.DAP_Farming_asPfert/self.DAP_P2O5*self.CF_DAP/self.ton2g*(1-self.DAP_share_as_Nfert)
    
    @property
    def K2O_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.K2O_Farming*self.CF_K2O/self.ton2g
    
    @property
    def Lime_GHG(self):
        '''CaCO3, in g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.Lime_Farming*self.CF_Lime/self.ton2g
    
    @property
    def Lime_CO2_GHG(self):
        '''CO2 emission due to lime (CaCO3) use, in g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.Lime_Farming*self.CO2_content_in_CaCO3*self.Percent_Lime_Acidified
    
    @property
    def Herbicide_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return (self.HerbicideUse_Farming+self.HerbicideUse_RyeCCFarming)*self.Herbicide_Farming_GHG
    
    @property
    def Insecticide_GHG(self):
        '''In g GHG per `FDCIC.GHG_functional_unit`.'''
        return self.InsecticideUse_Farming*self.Insecticide_Farming_GHG
    
    @property
    def SOC_GHG(self):
        '''
        GHG due to soil organic carbon change, in g GHG per `FDCIC.GHG_functional_unit`.
        Note that it is not included in the total carbon intensity (i.e., FDCIC.CI)
        by default.
        '''
        return getattr(self, 'SOC_emission', 0)*self.CO2_C_to_CO2/self.acre2hectare*self.kg2g/self.Yield_TS
    
    _GHG_items = [
        'Diesel_GHG',
        'Gasoline_GHG',
        'NG_GHG',
        'LPG_GHG',
        'Electricity_GHG',
        'Ammonia_GHG',
        'Urea_GHG',
        'AN_GHG',
        'AS_GHG',
        'UAN_GHG',
        'MAP_asNfert_GHG',
        'DAP_asNfert_GHG',
        'N2O_Fert_and_Res_GHG',
        'Urea_CO2_GHG',
        'MAP_asPfert_GHG',
        'DAP_asPfert_GHG',
        'K2O_GHG',
        'Lime_GHG',
        'Lime_CO2_GHG',
        'Herbicide_GHG',
        'Insecticide_GHG',
        'SOC_GHG',
        ]
    @property
    def GHG_items(self):
        '''All items considered in GHG accounting.'''
        return self._GHG_items
    @GHG_items.setter
    def GHG_items(self, i):
        self._GHG_items = i

    @property
    def GHG_table(self):
        '''A table of the GHG breakdown.'''
        dct = dict(crop=self.crop, unit=f'g CO2e/{self.GHG_functional_unit}')
        items = self.GHG_items
        dct.update({item: getattr(self, item) for item in items})
        ser = pd.Series(dct)
        ser['CI without SOC'] = ser[2:-1].sum()
        ser['CI with SOC'] = ser[2:-1].sum()
        return ser

    @property
    def CI(self):
        '''
        Feedstock carbon intensity, does not include soil organic carbon change,
        same as `FDCIC.CI`, in g CO2e/`FDCIC.GHG_functional_unit`.
        '''
        return self.GHG_table.iloc[-2].value
    CI_wo_SOC = CI
    
    @property
    def CI_w_SOC(self):
        '''
        Feedstock carbon intensity with soil organic carbon change,
        in g CO2e/`FDCIC.GHG_functional_unit`.
        '''
        return self.GHG_table.iloc[-2].value