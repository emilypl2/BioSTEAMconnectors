#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

'''
TODO: could consider using openpyxl to get the cell range values from FDCIC/GREET
'''

from math import e
from thermosteam.units_of_measure import AbsoluteUnitsOfMeasure as auom

class Var:
    '''
    A simple class used to represent variable value with unit of measurement.
    
    Parameters
    ----------
    name : str
        Name of this variable.
    value : int|float
        Value of this variable.
    unit : str
        Default unit of measurement of this variable.
    enable_unit_conversion : bool
        Whether to enable unit conversion.
    notes : str
        Additional notes on this variable.
        
    Examples
    --------
    >>> Diesel_LHV = Var('Diesel LHV', 128450, 'Btu/gal')
    >>> Diesel_LHV
    Diesel LHV: 128450 Btu/gal
    
    Calling this unit without any input will return the value in
    the default unit of measurement.
    
    >>> Diesel_LHV()
    128450
    >>> When `enable_unit_conversion` is enabled, will attempt to convert the unit.
    >>> Diesel_LHV.enable_unit_conversion = True
    >>> Diesel_LHV('Btu/m3') # doctest +ELLIPSIS
    33932900.1254...
    '''
    def __init__(self, name, value, unit, notes='', enable_unit_conversion=False):
        self.name = name
        self.value = value
        self.unit = unit
        self.notes = notes
        self.enable_unit_conversion = enable_unit_conversion
        
    def __repr__(self, new_unit=None):
        if new_unit:
            if not self.enable_unit_conversion:
                raise ValueError('Unit conversion is not enabled.')
            else:
                unit = new_unit
                val = self(new_unit)
        else:
            unit = self.unit
            val = self.value
        return f'{self.name}: {val} {unit}'
        
    def __call__(self, new_unit=None):
        val = self.value
        if not new_unit: return val
        if not self.enable_unit_conversion:
            raise ValueError('Unit conversion is not enabled.')
        unit = new_unit
        return auom(unit).convert(val, new_unit)    

# class RefVar(Var):
#     '''
#     Non-independent variables whose value is based on a linked variable.
#     Note that this class needs to be attached to the same :class:`FDCIC` object
#     that its reference variable is attached to.
    
#     Values and units of this class cannot be changed
#     (should change the reference object instead),
#     and unit conversion is disabled.
    
#     Parameters
#     ----------
#     name : str
#         Name of the this variable.
#     ref_name : str
#         Name of the reference variable.
#     fdcic : obj
#         The :class:`FDCIC` object that this variable and its reference variable
#         are attached to.
#     factor : int|float
#         A multiplication factor on top of the value of the reference variable.
#     notes : str
#         Additional notes on this variable.
#     '''
#     def __init__(self, name, ref_name, fdcic, factor=1, notes=''):
#         self.name = name
#         self.ref_name = ref_name
#         self.fdcic = fdcic
#         self.factor = factor
#         self.notes = notes

#     @property
#     def enable_unit_conversion(self):
#         return False

#     @property
#     def fdcic(self):
#         fdcic = self._fdcic
#         if not fdcic:
#             raise AttributeError(f'Variable {self.name} has not been assigned a `FDCIC` class.')
#         return fdcic
#     @fdcic.setter
#     def fdcic(self, i):
#         self._fdcic = i
    
#     @property
#     def ref(self):
#         return getattr(self.fdcic, self.ref_name)
    
#     @property
#     def value(self):
#         return self.ref.value

#     @property
#     def unit(self):
#         return self.ref.unit


# %%

# =============================================================================
# Default parameter values in FDCIC
# =============================================================================

# In sheet "Parameters", values here are pulled from GREET
default_parameters = [
    # Lower Heating Values of fuels/Fuel specification
    Var('Diesel_LHV', 128450, 'Btu/gal'),
    Var('Gasoline_LHV', 112194, 'Btu/gal'),
    Var('Ethanol_LHV', 76330, 'Btu/gal'),
    Var('NG_LHV', 983, 'Btu/ft3', notes='natural gas'),
    Var('LPG_LHV', 84950, 'Btu/gal', notes='liquid petroleum gas'),
    Var('Electricity_LHV', 3412, 'Btu/kWh'),
    # Unit conversion, name has been revised to be more consistent and prevents misuse
    Var('g_per_lb', 453.592, 'g/lb'),
    Var('Btu_per_MJ', 947.817, 'Btu/MJ'),
    Var('tonne_per_lb', 0.000453593, 'tonne/lb'),
    Var('kg_per_lb', 0.4535925, 'kg/lb'),
    Var('lb_per_bu_CanCorn', 56, 'lbs/bushel'),
    Var('L_per_gal', 3.78541, 'L/gal'),
    Var('acre_per_hectare', 2.47105, 'acre/hectare'),
    Var('g_per_kg', 1000, 'g/kg'),
    Var('kJ_per_MJ', 1000, 'kJ/MJ'),
    Var('kJ_per_kWh', 3600, 'kJ/kWh'),
    Var('kJ_per_GJ', 1000000, 'kJ/GJ'),
    Var('g_per_ton', 907184.74, 'g/ton'),
    Var('NG_density', 22, 'g/ft3'),
    # Emission factor from synthetic nitrogen fertilizer
    Var('Nfertilizer_N2O_factor_US', 0.01325, ''),
    # Corn: N content of above and below ground biomass and N2O Emission
    Var('Cornfarming_Ninbiomass_residue', 141.6, 'unknown'),
    Var('Cornfarming_biomass_N2O_factor', 0.01264, ''),
    # N content in Nitrogen fertilizer
    Var('Ammonia_N', 0.824, 'g N/g mass'), # 14/17
    Var('Urea_N', 0.467, 'g N/g mass'), # 28/60
    Var('AN_N', 0.35, 'g N/g mass', notes='ammonium nitrate'), # 28/80
    Var('AS_N', 0.211999, 'g N/g mass', notes='ammonium sulfate'), # 28/132
    Var('UAN_N', 1,), # unsure why it's 1, maybe because it's as N
    Var('MAP_N', 0.11, 'monoammonium phosphate'), #!!! why 0.11? should be 14/115=0.122
    Var('DAP_N', 0.16, 'diammonium phosphate'), #!!! why 0.11? should be 28/132=0.212
    Var('MAP_share_as_Nfert', 0.31139559, ''), # 14/(14+31) between N and P
    Var('DAP_share_as_Nfert', 0.474907149, ''), # 28/(28+31) between N and P
    Var('N2O_N_to_N2O', 1.571428571, 'g N/g N2O'), # 44/28
    Var('CO2_C_to_CO2', 3.666666667, 'g C/g CO2'), # 44/12
    Var('Urea_N_to_CO2', 1.571428571, 'g N/g urea'), # 60/28
    Var('Urea_N', 0.467, 'g CO2/g N in urea'), # 44/28 (MW of CO2 over MW of N)
    # P2O5 content in Phosphorus fertilizer
    Var('MAP_P2O5', 0.48),
    Var('DAP_P2O5', 0.48),
    # Lime acidified
    Var('CO2_content_in_CaCO3', 0.44, 'g CO2/g CaCO3'), # 44/100
    Var('Percent_Lime_Acidified', 0.492, 'fraction'),
    # Soybean: N content of above and below ground biomass and N2O Emission
    Var('Soybeanfarming_Ninbiomass_residue', 557, notes='N content of above and below ground biomass: grams'),
    Var('Soybeanfarming_Nfixation_N2O_factor', 7.3, notes='N2O emissions from N fixation: grams N2O'),
    Var('Soybeanfarming_biomass_N2O_factor', 0.01264, notes='N2O emissions: N in N2O as % of N in soybean biomass'),
    Var('Nfertilizer_N2O_factor_US_soybean', 0.01374, notes='N2O Emissions: N fertilizer in soybean field'),
    # GS (grain sorghum): N content of above and below ground biomass and N2O Emission
    Var('GSfarming_Ninbiomass_residue', 149, notes='N content of above and below ground biomass: grams'),
    Var('GSfarming_biomass_N2O_factor', 0.01264, notes='N2O Emissions: N in N2O as % of N in grain sorghum biomass'),
    Var('Nfertilizer_N2O_factor_US_sorghum', 0.01374, notes='N2O Emissions: N fertilizer in grain sorghum field'),
    # Sugarcane: N content of above and below ground biomass and N2O Emission
    Var('Sugarcanefarming_Ninbiomass_residue', 445.2, notes='N content of above and below ground biomass: grams'),
    Var('Sugarcane_NinVinasse', 205.2, notes='N content of above and below ground biomass: grams'),
    Var('Sugarcane_NinFilteredcake', 35.8783008036739, notes='N content of filtered cake as soil amendment'),
    Var('Sugarcanefarming_biomass_N2O_factor', 0.01264, notes='N2O Emissions: N in N2O as % of N in biomass'),
    Var('Nfertilizer_N2O_factor_Brazil', 0.0122, notes='N2O Emissions: N fertilizer in Brazillian sugarcane fields'),
    # Rice: N content of above and below ground biomass and N2O Emission
    Var('Ricefarming_Ninbiomass_residue', 535.140584128, notes='N content of above and below ground biomass: gram N/cwt rice '),
    Var('Ricefarming_biomass_N2O_factor', 0.01264, notes='N2O Emissions: N in N2O as % of N in rice biomass'),
    Var('EFc', 0.65, 'kg CH4/ha/day'),
    Var('Rice_cultivation_period', 139, 'day'),
    Var('Rice_straw_application_rate', 4, 'Mg/ha'),
    # Rye cover crop: yield, N content in biomass, and N2O Emission
    Var('RyeCCfarming_biomass_N2O_factor', 0.01264, 'g N2O-N/g-N'),
    Var('RyeCCfarming_Ncontent', 0.016, 'ton-N/dry ton-cover crop'),
    # Manure N and P2O5 content
    Var('Swine_manure_N', 1279.1304834, 'g N/ton manure'),
    Var('Dairy_manure_N', 1950.447191, 'g N/ton manure'),
    Var('Cattle_manure_N', 1991.2705043, 'g N/ton manure'),
    Var('Chicken_manure_N', 7302.837157, 'g N/ton manure'),
    Var('Manure_transportation_energy_ton_mile', 10416.49299, 'Btu/ton manure/mile'),
    Var('Manure_transportation_distance_mile', 0.367, 'mile'),
    Var('Manure_N2O_factor', 0.01474, 'g-N2O-N/g-N applied'),
    # Global warming potential
    Var('CO2_GWP', 1, 'kg CO2e/kg CO2'),
    Var('CH4_GWP', 29.8, 'kg CO2e/kg CH4'),
    Var('N2O_GWP', 273, 'kg CO2e/kg N2O'),
    Var('Biogenic_CH4_GWP', 28, 'kg CO2e/kg CH4'),
    ]

# In sheet "Intermediate", values here are calculated based off GREET values
default_parameters.extend([
    ### Production Usage Amount
    # Ammonia
    Var('Ammonia_Prod_NGIn', 27.9613103359878, 'mmBtu/ton'),
    Var('Ammonia_Prod_ElecIn', 0.188560619556814, 'mmBtu/ton'),
    Var('Ammonia_Prod_HydrogenIn', 0, 'ton/ton'),
    Var('Ammonia_Prod_NitrogenIn', 0, 'ton/ton'),
    Var('Green_Ammonia_Prod_NGIn', 27.9613103359878, 'mmBtu/ton'),
    Var('Green_Ammonia_Prod_ElecIn', 1.11135683852937, 'mmBtu/ton'),
    Var('Green_Ammonia_Prod_HydrogenIn', 0.197284, 'ton/ton'),
    Var('Green_Ammonia_Prod_NitrogenIn', 0.929778, 'ton/ton'),
    # Urea
    Var('Urea_Prod_NGIn', 3.98108341487325, 'mmBtu/ton'),
    Var('Urea_Prod_ElecIn', 0.455717971896938, 'mmBtu/ton'),
    Var('Urea_Prod_AmmoniaIn', 0.567, 'ton ammonia/ton'),
    # Ammonium Nitrate
    Var('AN_Prod_NGIn', 0.636285470195725, 'mmBtu/ton'),
    Var('AN_Prod_ElecIn', 0.214961307498556, 'mmBtu/ton'),
    Var('AN_Prod_AmmoniaIn', 0.213, 'ton ammonia/ton'),
    Var('AN_Prod_NAIn', 0.788, 'ton nitric acid/ton'),
    # Ammonium Sulfate
    Var('AS_Prod_AmmoniaIn', 0.257765731251332, 'ton ammonia/ton'),
    Var('AS_Prod_SAIn', 0.742234268748668, 'ton sulfuric acid/ton'),
    # Urea-ammonium nitrate solution
    Var('UAN_Prod_NGIn', 0.137575236799076, 'mmBtu/ton'),
    Var('UAN_Prod_ElecIn', 0.481513328796765, 'mmBtu/ton'),
    Var('UAN_Prod_UreaIn', 1.09, 'ton urea/ton'),
    Var('UAN_Prod_ANIn', 1.43, 'ton AN/ton'),
    # MAP
    Var('MAP_Prod_NGIn', 0.283748925898093, 'mmBtu/ton'),
    Var('MAP_Prod_ElecIn', 0.103181427599307, 'mmBtu/ton'),
    Var('MAP_Prod_AmmoniaIn', 0.133, 'ton ammonia/ton'),
    Var('MAP_Prod_PAIn', 0.784346173469388, 'ton phosphoric acid/ton',
        notes='In GREET, H3PO4 is reacted with ammonia; '
        'In this cell, the number is already adjusted to P2O5 value'),
    # DAP
    Var('DAP_Prod_NGIn', 0.23215821209844, 'mmBtu/ton'),
    Var('DAP_Prod_ElecIn', 0.103181427599307, 'mmBtu/ton'),
    Var('DAP_Prod_AmmoniaIn', 0.22, 'ton ammonia/ton'),
    Var('DAP_Prod_PAIn', 0.719889285714286, 'ton phosphoric acid/ton',
        notes='In GREET, H3PO4 is reacted with ammonia; '
        'In this cell, the number is already adjusted to P2O5 value'),
    # K2O
    Var('K2O_Prod_NGIn', 1.053, 'mmBtu/ton'),
    Var('K2O_Prod_ElecIn', 1.638, 'mmBtu/ton'),
    Var('K2O_Prod_DieselIn', 1.209, 'mmBtu/ton'),
    # Lime
    Var('Lime_Prod_NGIn', 0.000002, 'mmBtu/ton'),
    Var('Lime_Prod_ElecIn', 0.000244, 'mmBtu/ton'),
    Var('Lime_Prod_ROIn', 0.001554, 'mmBtu/ton'),
    Var('Lime_Prod_DieselIn', 0.012296, 'mmBtu/ton'),
    Var('Lime_Prod_CoalIn', 0.003474, 'mmBtu/ton'),
    Var('Lime_Prod_GasolineIn', 0.002428, 'mmBtu/ton', notes='gasoline blendstock'),
    # Brazilian Phosphate (P2O5)
    Var('PA_Brazilian_Prod_ElecIn', 0.438521067297053, 'mmBtu/ton'),
    Var('PA_Brazilian_Prod_PhosRockIn', 3.525, 'ton phosphoric rock/ton'),
    Var('PA_Brazilian_Prod_SAIn', 2.73, 'ton sulfuric acid/ton'),
    # Brazilian Lime
    Var('Lime_Brazilian_Prod_ElecIn', 0.022, 'mmBtu/ton'),
    Var('Lime_Brazilian_Prod_DieselIn', 0.08, 'mmBtu/ton',),
    # Nitric acid, the original spreadsheet is "Nitrid", probably a typo
    Var('NA_ElecIn', 0.0275150473598151, 'mmBtu/ton'),
    Var('NA_AmmoniaIn', 0.288, 'ton ammonia/ton'),

    ### Upstream Inputs CI ###
    # Natural gas for ammonia
    Var('NG_upstream_CO2_for_Ammonia', 6336.27495433342, 'g CO2/mmBtu'),
    Var('NG_upstream_CH4_for_Ammonia', 209.647367838732, 'g CH4/mmBtu'),
    Var('NG_upstream_N2O_for_Ammonia', 1.20338508869173, 'g N2O/mmBtu'),
    # Electricity
    Var('Electricity_upstream_CO2', 127800.997787876, 'g CO2/mmBtu'),
    Var('Electricity_upstream_CH4', 270.971245722998, 'g CH4/mmBtu'),
    Var('Electricity_upstream_N2O', 2.59722458324966, 'g N2O/mmBtu'),
    # Natural gas as stationary fuels
    Var('NG_upstream_CO2_for_StationaryFuel', 6612.51577425863, 'g CO2/mmBtu'),
    Var('NG_upstream_CH4_for_StationaryFuel', 223.188741132914, 'g CH4/mmBtu'),
    Var('NG_upstream_N2O_for_StationaryFuel', 1.41779149855698, 'g N2O/mmBtu'),
    # Nitric acid for Ammonia Nitrate (US)
    Var('NA_Upstream_CO2', 75170.857071601, 'g CO2/ton'),
    Var('NA_Upstream_CH4', 105.688518236322, 'g CH4/ton'),
    Var('NA_Upstream_N2O', 4314.74953262626, 'g N2O/ton'),
    # Sulfuric acid for AS （ammonium sulfate)
    Var('SA_Upstream_CO2', 37876.883582726, 'g CO2/ton'),
    Var('SA_Upstream_CH4', 58.4724216450816, 'g CH4/ton'),
    Var('SA_Upstream_N3O', 0.917706163476711, 'g N2O/ton'),
    # Phosphic acid (P2O5) for MAP/DAP
    Var('PA_Upstream_CO2', 1223301.07996423, 'g CO2/ton',
        notes='instead of using the value for P2O5 directly from GREET, '
        'this number is adjusted since P2O5 is used as an intermediate for MAP/DAP production'),
    Var('PA_Upstream_CH4', 2646.44140088924, 'g CH4/ton',
        notes='instead of using the value for P2O5 directly from GREET, '
        'this number is adjusted since P2O5 is used as an intermediate for MAP/DAP production'),
    Var('PA_Upstream_N2O', 30.3585578183862, 'g N2O/ton',
        notes='instead of using the value for P2O5 directly from GREET, '
        'this number is adjusted since P2O5 is used as an intermediate for MAP/DAP production'),
    # Diesel as fuel
    Var('Diesel_upstream_CO2', 13186.722667603, 'g CO2/mmBtu'),
    Var('Diesel_upstream_CH4', 111.772244649243, 'g CH4/mmBtu'),
    Var('Diesel_upstream_N2O', 0.244015821801455, 'g N2O/mmBtu'),
    # RO as fuel 
    Var('RO_upstream_CO2', 10089.1978586435, 'g CO2/mmBtu'),
    Var('RO_upstream_CH4', 102.151248520798, 'g CH4/mmBtu'),
    Var('RO_upstream_N2O', 0.17225341835045, 'g N2O/mmBtu'),
    # Coal as fuel
    Var('NG_upstream_CO2_for_Ammonia', 1620.01544142514, 'g CO2/mmBtu'),
    Var('NG_upstream_CH4_for_Ammonia', 147.842989765332, 'g CH4/mmBtu'),
    Var('NG_upstream_N2O_for_Ammonia', 0.0330322808747223, 'g N2O/mmBtu'),
    # Gasoline blendstock as fuel
    Var('GB_upstream_CO2', 17280.008954548, 'g CO2/mmBtu'),
    Var('GB_upstream_CH4', 117.618105305705, 'g CH4/mmBtu'),
    Var('GB_upstream_CO2', 0.303658433025717, 'g N2O/mmBtu'),
    # H2 as ammonia feedstock
    Var('H2_upstream_CO2', 0, 'g CO2/ton'),
    Var('H2_upstream_CH4', 0, 'g CH4/ton'),
    Var('H2_upstream_N2O', 0, 'g N2O/ton'),
    # LPG as fuel
    Var('LPG_upstream_CO2', 10270.9071851525, 'g CO2/mmBtu'),
    Var('LPG_upstream_CH4', 143.922251990527, 'g CH4/mmBtu'),
    Var('LPG_upstream_N2O', 0.190046157546839, 'g N2O/mmBtu'),
    # N2 as ammonia feedstock
    Var('Cryogenic_Nitrogen_for_Ammonia_CO2', 60102.6359553953, 'g CO2/ton'),
    Var('Cryogenic_Nitrogen_for_Ammonia_CH4', 127.433168895136, 'g CH4/ton'),
    Var('Cryogenic_Nitrogen_for_Ammonia_N2O', 127.433168895136, 'g N2O/ton'),
    # Electricity for sorghum farming
    Var('Electricity_upstream_CO2_GSfarming', 208012.449793143, 'g CO2/mmBtu'),
    Var('Electricity_upstream_CH4_GSfarming', 399.414592088963, 'g CH4/mmBtu'),
    Var('Electricity_upstream_N2O_GSfarming', 4.45697257919624, 'g N2O/mmBtu'),
    # Brazilian Electricity mix
    Var('Electricity_Brazilian_upstream_CO2', 31134.2889933693, 'g CO2/mmBtu'),
    Var('Electricity_Brazilian_upstream_CH4', 68.1540904421038, 'g CH4/mmBtu'),
    Var('Electricity_Brazilian_upstream_N2O', 2.60720001275336, 'g N2O/mmBtu'),
    # Nitric acid for Ammonia Nitrate (Brazil)
    Var('NA_Brazilian_Upstream_CO2', 49535.7667048375, 'g CO2/ton'),
    Var('NA_Brazilian_Upstream_CH4', 59.9936612743312, 'g CH4/ton'),
    Var('NA_Brazilian_Upstream_N2O', 4314.24657035987, 'g N2O/ton'),
    # Phosphoric rock (Brazil)
    Var('PhosRock_Brazilian_Upstream_CO2', 223137.180388021, 'g CO2/ton'),
    Var('PhosRock_Brazilian_Upstream_CH4', 516.989122373125, 'g CH4/ton'),
    Var('PhosRock_Brazilian_Upstream_N2O', 6.58762980077705, 'g N2O/ton'),
    # Sulfuric acid for Phosphate (Brazil)
    Var('SA_Brazilian_Upstream_CO2', 31559.884540055, 'g CO2/ton'),
    Var('SA_Brazilian_Upstream_CH4', 45.2186780168568, 'g CH4/ton'),
    Var('SA_Brazilian_Upstream_N2O', 0.91835804021288, 'g N2O/ton'),
    
    ### Product Emissions ###
    #!!! units uncertain, double-check
    # Conventional Ammonia
    Var('Ammonia_InputsCons_CO2', 418019.378867298, 'g CO2/ton'),
    Var('Ammonia_InputsCons_GHG', 419299.093955674, 'g CO2/ton'),
    Var('Ammonia_Process_CO2', 1282572.53476364, 'g CO2/ton'),
    Var('Ammonia_Process_GHG', 1667878.98548293, 'g CO2/ton'),
    # Green Ammonia
    Var('Green_Ammonia_InputsCons_CO2', 0, 'g CO2/ton'),
    Var('Green_Ammonia_InputsCons_GHG', 0, 'g CO2/ton'),
    Var('Green_Ammonia_Process_CO2', -150152.086092707, 'g CO2/ton'),
    Var('Green_Ammonia_Process_GHG', -160472.300800874, 'g CO2/ton'),
    # Ammonia T&D
    Var('Ammonia_TD_CO2_Final', 79892.0911666773, 'g CO2/ton'),
    Var('Ammonia_TD_GHG_Final', 83116.232535494, 'g CO2/ton'),
    Var('Ammonia_TD_CO2_Intermediate', 36177.2245218574, 'g CO2/ton'),
    Var('Ammonia_TD_GHG_Intermediate', 37731.2996020379, 'g CO2/ton'),
    # Urea
    Var('Urea_InputsCons_CO2', 236336.144795337, 'g CO2/ton'),
    Var('Urea_InputsCons_GHG', 237059.658932989, 'g CO2/ton'),
    Var('Urea_Process_CO2', -665268.809333333, 'g CO2/ton'),
    Var('Urea_Process_GHG', -665268.809333333, 'g CO2/ton'),
    Var('Urea_TD_CO2_Final', 92393.9719134906, 'g CO2/ton'),
    Var('Urea_TD_GHG_Final', 96116.6959138755, 'g CO2/ton'),
    # Ammonia Nitrate
    Var('AN_InputsCons_CO2', 37772.9475482828, 'g CO2/ton'),
    Var('AN_InputsCons_GHG', 37888.5847970653, 'g CO2/ton'),
    Var('AN_TD_CO2_Final', 83869.9623133906, 'g CO2/ton'),
    Var('AN_TD_GHG_Final', 87252.7436104336, 'g CO2/ton'),
    # Ammonia Sulfate
    Var('AS_TD_CO2_Final', 43714.8666448198, 'g CO2/ton'),
    Var('AS_TD_GHG_Final', 45384.9329334561, 'g CO2/ton'),
    # Urea-ammonium nitrate solution
    Var('UAN_InputsCons_CO2', 16844.6928255856, 'g CO2/ton'),
    Var('UAN_InputsCons_GHG', 16896.2607878805, 'g CO2/ton'),
    Var('UAN_TD_CO2_Final', 43714.8666448198, 'g CO2/ton'),
    Var('UAN_TD_GHG_Final', 45384.9329334561, 'g CO2/ton'),
    # DAP
    Var('DAP_InputsCons_CO2', 13782.0214027518, 'g CO2/ton'),
    Var('DAP_InputsCons_GHG', 13824.2133719022, 'g CO2/ton'),
    Var('DAP_TD_CO2_Final', 43714.8666448198, 'g CO2/ton'),
    Var('DAP_TD_GHG_Final', 45384.9329334561, 'g CO2/ton'),
    # K2O
    Var('K2O_InputsCons_CO2', 156856.043783494, 'g CO2/ton'),
    Var('K2O_InputsCons_GHG', 157379.714438794, 'g CO2/ton'),
    Var('K2O_TD_CO2_Final', 85006.4969267373, 'g CO2/ton'),
    Var('K2O_TD_GHG_Final', 88434.6039175592, 'g CO2/ton'),
    # Lime (US)
    Var('Lime_InputsCons_CO2', 1615.68748023966, 'g CO2/ton'),
    Var('Lime_InputsCons_GHG', 1625.72043123049, 'g CO2/ton'),
    Var('Lime_TD_CO2_Final', 6505.50857920391, 'g CO2/ton'),
    Var('Lime_TD_GHG_Final', 6752.39214215056, 'g CO2/ton'),
    # Diesel (US)
    Var('CornFarming_DieselCons_CO2', 0.0776795063144252, 'g CO2/mmBtu'),
    Var('CornFarming_DieselCons_GHG', 0.0782208477272848, 'g CO2/mmBtu'),
    # Gasoline (blendstock)
    Var('CornFarming_GBCons_CO2', 0.0744767583446154, 'g CO2/mmBtu'),
    Var('CornFarming_GBCons_GHG', 0.075194823011016, 'g CO2/mmBtu'),
    # Natural gas
    Var('CornFarming_NGCons_CO2', 0.0568897869032699, 'g CO2/mmBtu'),
    Var('CornFarming_NGCons_GHG', 0.0686122391032699, 'g CO2/mmBtu'),
    # Liquefied petroleum gas
    Var('CornFarming_LPGCons_CO2', 0.0680396477962499, 'g CO2/mmBtu'),
    Var('CornFarming_LPGCons_GHG', 0.0693835121962499, 'g CO2/mmBtu'),
    # Herbicide
    Var('Herbicide_CornFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Var('Herbicide_CornFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Var('Herbicide_SoybeanFarming_CO2', 18.4435700710221, 'g CO2/ton'),
    Var('Herbicide_SoybeanFarming_GHG', 19.5025381699089, 'g CO2/ton'),
    Var('Insecticide_GSFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Var('Insecticide_GSFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Var('Herbicide_SugarcaneFarming_CO2', 14.6740189992022, 'g CO2/ton',
        notes='We do not have data regarding rice-specific pesticide CI, therefore, '
        'we assume it is the same with corn'),
    Var('Herbicide_SugarcaneFarming_GHG', 15.5005618973604, 'g CO2/ton',
        notes='We do not have data regarding rice-specific pesticide CI, therefore, '
        'we assume it is the same with corn'),
    # Insecticide
    Var('Insecticide_CornFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Var('Insecticide_CornFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Var('Insecticide_SoybeanFarming_CO2', 18.4435700710221, 'g CO2/ton'),
    Var('Insecticide_SoybeanFarming_GHG', 19.5025381699089, 'g CO2/ton'),
    Var('Insecticide_GSFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Var('Insecticide_GSFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Var('Insecticide_SugarcaneFarming_CO2', 14.6740189992022, 'g CO2/ton',
        notes='We do not have data regarding rice-specific pesticide CI, therefore, '
        'we assume it is the same with corn'),
    Var('Insecticide_SugarcaneFarming_GHG', 15.5005618973604, 'g CO2/ton',
        notes='We do not have data regarding rice-specific pesticide CI, therefore, '
        'we assume it is the same with corn'),
    # Brazilian Phosphate (P2O5)
    # Brazilian P2O5 production does not consume natural gas onsite,
    # and therefore, does not incur onsite GHG emissions
    Var('PA_TD_CO2_Final', 86711.2988467573, 'g CO2/ton'),
    Var('PA_TD_GHG_Final', 90207.3943782476, 'g CO2/ton'),
    # Brazilian Lime
    Var('Brazilian_Lime_InputsCons_CO2', 6239.25302609347, 'g CO2/ton'),
    Var('Brazilian_Lime_InputsCons_GHG', 6289.06159243846, 'g CO2/ton'),
    # Diesel (Brazilian)
    Var('SugarcaneFarming_DieselCons_CO2', 0.0777608192847955, 'g CO2/mmBtu'),
    Var('SugarcaneFarming_DieselCons_GHG', 0.0783650996008699, 'g CO2/mmBtu'),
    # Sugarcane soil amendment
    Var('SugarcaneFarming_SoilAmendment_TD_CO2', 18.680313715969, 'g CO2/ton'),
    Var('SugarcaneFarming_SoilAmendment_TD_GHG', 530.435404440136, 'g CO2/ton'),
    # Gasoline (Brazilian)
    Var('SugarcaneFarming_GasolineCons_CO2', 0.0744767583446154, 'g CO2/mmBtu'),
    Var('SugarcaneFarming_GasolineCons_GHG', 0.075194823011016, 'g CO2/mmBtu'),
    # Nitric acid, the original spreadsheet is "Nitrid", probably a typo
    Var('NA_Process_CO2', 0, 'g CO2/ton'),
    Var('NA_Process_GHG', 1177449, 'g CO2/ton'),
    Var('NA_TD_CO2_Final', 48679.1052686707, 'g CO2/ton'),
    Var('NA_TD_GHG_Final', 50731.7629804194, 'g CO2/ton'),    
    ])

# %%

# =============================================================================
# Default user inputs in FDCIC
# =============================================================================


default_inputs = [
    ### Rice: N content of above and below ground biomass and N2O Emission ###
    Var('Rice_water_regime_during_cultivation', 'Continuously flooded'),
    Var('Rice_water_regime_pre_season', 'Non flooded pre-season >365 d'),
    Var('Rice_time_for_straw_incorporation', 'Straw incorporated shortly (<30 days) before cultivation'),
    ### Regionalized N2O emission factors table ###
    Var('Climate_zone', 'No consideration'),
    Var('Nfertilizer_N2O_factor_US_rice', 0.004+0.00374, notes='direct and indirect'),
    ### 4R nitrogen management practice for corn farming,  ###
    Var('N_balance_assumed', 0, 'kg N/ha'),
    ]

# %%

class FDCIC:
    '''
    A general class to calculate feedstock carbon intensity and cost as in
    GREET's feedstock carbon intensitity calculator.
    
    Parameters
    ----------
    parameters : iterable(obj)
        A sequence of :class:`Var` objects that contain contants.
    user_inputs : iterable(obj)
        A sequence of :class:`Var` objects that contain user inputs.
    '''
    acronyms = {
        'AN': 'ammonium nitrate',
        'AS': 'ammonium sulfate',
        'GB': 'gasoline blendstock',
        'GS': 'grain sorghum',
        'LPG': 'liquid petroleum gas',
        'NA': 'nitric acid',
        'NG': 'natural gas',
        'PA': 'phosphoric acid',
        'RO': 'residual oil',
        'SA': 'sulfuric acid',
        'TD': 'transportation & distribution',
        'UAN': 'urea-ammonium nitrate solution',
        }
    
    def __init__(self, parameters=[], user_inputs=[]):
        params = parameters or default_parameters
        self.parameters = {p.name: p for p in params}
        inputs = user_inputs or default_inputs
        self.user_inputs = {i.name: i for i in inputs}
        self.reset_variables()

    def reset_variables(self, variables=[]):
        '''
        Reset variable values based on the provided or saved list of parameters/inputs.
        '''
        variables = variables or self.variables
        for var in self.variables:
            setattr(self, var.name, var.value)
            
    @property
    def variables(self):
        dct = self.parameters
        dct.update(self.inputs)
        return dct
        
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
    def lb2bu_CanCorn(self):
        '''Same as `lb_per_bu_CanCorn`.'''
        return self.lb_per_bu_CanCorn
    
    @property
    def L_to_gal(self):
        '''Same as `L_per_gal`.'''
        return self.L_per_gal
    
    @property
    def ac_per_ha(self):
        '''Same as `acre_per_hectare`.'''
        return self.acre_per_hectare

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
        raise ValueError(
            'Invalid input for `Rice_water_regime_during_cultivation`, '
            'can only be one of "Continuously flooded", "Single drainage period", '
            '"Multiple drainage period", "Regular rainfed", "Drought prone", or "Deep water", '
            f'not {regime}.')

    @property
    def SFp(self):
        '''Scaling factor to account for the differences in water regime in the pre-season before the cultivation period (SFp).'''
        regime = self.Rice_water_regime_pre_season
        if regime == 'Non flooded pre-season <180 d': return 1
        elif regime == 'Non flooded pre-season >180 d': return 0.89
        elif regime == 'Flooded pre-season (>30 d)': return 2.41
        elif regime == 'Non-flooded pre-season >365 d': return 0.59
        raise ValueError(
            'Invalid input for `Rice_time_for_straw_incorporation`, '
            'can only be one of "Non flooded pre-season <180 d", "Non flooded pre-season >180 d", '
            '"Flooded pre-season (>30 d)", or "Non-flooded pre-season >365 d", '
            f'not {regime}.')

    @property
    def Rice_ammendment_factor(self):
        '''Conversion factor for organic amendment in terms of its relative effect with respect to straw applied shortly before cultivation.'''
        app_time = self.Rice_time_for_straw_incorporation
        if app_time == 'Straw incorporated shortly (<30 days) before cultivation': return 1 
        elif app_time == 'Straw incorporated long (>30 days) before cultivation': return 0.19
        raise ValueError(
            'Invalid input for `Rice_time_for_straw_incorporation`, '
            'can only be "Straw incorporated shortly (<30 days) before cultivation", or '
            '"Straw incorporated long (>30 days) before cultivation", '
            f'not {app_time}.')
    
    @property
    def SFo(self):
        '''Scaling factor should vary for both type and amount of organic amendment applied  (SFo).'''
        return (1+self.Rice_straw_application_rate*self.Rice_ammendment_factor)**0.59
    
    @property
    def Annual_CH4_emission_from_rice_field(self):
        '''In kg CH4/ha.'''
        return self.EFc*self.SFw*self.SFp*self.Fo*self.Rice_cultivation_period
    
    @property
    def Nfertilizer_direct_N2O_factor_US_corn(self):
        zone = self.Climate_zone
        if zone in ('No consideration', 'NA', 'Wet or Moist'): return 0.01
        elif zone == 'Dry': return 0.005
        raise ValueError(
            'Invalid input for `Climate_zone`, can only be one of "No consideration", '
            f'"NA", "Wet or Moist", or "Dry", not {zone}.')
    
    @property
    def Nfertilizer_indirect_N2O_factor_US_corn(self):
        zone = self.Climate_zone
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
        '''N2O-N emissions per bushel of corn under 4R practice, [g GHG/bu].'''
        return e**(0.339+0.0047*self.N_balance_assumed)

    @property
    def Herbicide_RiceFarming_CO2(self):
        '''Same as `Herbicide_CornFarming_CO2`.'''
        return self.Herbicide_CornFarming_CO2
    
    @property
    def Herbicide_RiceFarming_GHG(self):
        '''Same as `Herbicide_CornFarming_GHG`.'''
        return self.Herbicide_CornFarming_GHG
    
    @property
    def Insecticide_RiceFarming_CO2(self):
        '''Same as `Insecticide_CornFarming_CO2`.'''
        return self.Insecticide_CornFarming_CO2
    
    @property
    def Insecticide_RiceFarming_GHG(self):
        '''Same as `Insecticide_RiceFarming_GHG`.'''
        return self.Insecticide_CornFarming_GHG

        
    
# %%