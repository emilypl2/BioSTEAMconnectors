#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.


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
    def __init__(self, name, value, unit, enable_unit_conversion=False, notes=''):
        self.name = name
        self.value = value
        self.unit = unit
        self.enable_unit_conversion = enable_unit_conversion
        self.notes = notes
        
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

default_parameters = [
    # =========================================================================
    # Sheet "Parameters"
    # =========================================================================
    ### Lower Heating Values of fuels/Fuel specification ###
    Var('Diesel_LHV', 128450, 'Btu/gal'),
    Var('Gasoline_LHV', 112194, 'Btu/gal'),
    Var('Ethanol_LHV', 76330, 'Btu/gal'),
    Var('NG_LHV', 983, 'Btu/ft3', notes='natural gas'),
    Var('LPG_LHV', 84950, 'Btu/gal', notes='liquid petroleum gas'),
    Var('Electricity_LHV', 3412, 'Btu/kWh'),
    ### Unit conversion, name has been revised to be more consistent and prevents misuse ###
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
    ### Emission factor from synthetic nitrogen fertilizer ###
    Var('Nfertilizer_N2O_factor_US', 0.01325, ''),
    ### Corn: N content of above and below ground biomass and N2O Emission ###
    Var('Cornfarming_Ninbiomass_residue', 141.6, 'unknown'),
    Var('Cornfarming_biomass_N2O_factor', 0.01264, ''),
    ### N content in Nitrogen fertilizer ###
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
    ### P2O5 content in Phosphorus fertilizer ###
    Var('MAP_P2O5', 0.48),
    Var('DAP_P2O5', 0.48),
    ### Urea content in UAN, linked to `UAN_Prod_UreaIn` ###
    ### Lime acidified ###
    Var('CO2_content_in_CaCO3', 0.44, 'g CO2/g CaCO3'), # 44/100
    Var('Percent_Lime_Acidified', 0.492, 'fraction'),
    ### Soybean: N content of above and below ground biomass and N2O Emission ###
    Var('Soybeanfarming_Ninbiomass_residue', 557, notes='N content of above and below ground biomass: grams'),
    Var('Soybeanfarming_Nfixation_N2O_factor', 7.3, notes='N2O emissions from N fixation: grams N2O'),
    Var('Soybeanfarming_biomass_N2O_factor', 0.01264, notes='N2O emissions: N in N2O as % of N in soybean biomass'),
    Var('Nfertilizer_N2O_factor_US_soybean', 0.01374, notes='N2O Emissions: N fertilizer in soybean field'),
    ### GS (grain sorghum): N content of above and below ground biomass and N2O Emission ###
    Var('GSfarming_Ninbiomass_residue', 149, notes='N content of above and below ground biomass: grams'),
    Var('GSfarming_biomass_N2O_factor', 0.01264, notes='N2O Emissions: N in N2O as % of N in grain sorghum biomass'),
    Var('Nfertilizer_N2O_factor_US_sorghum', 0.01374, notes='N2O Emissions: N fertilizer in grain sorghum field'),
    ### Sugarcane: N content of above and below ground biomass and N2O Emission ###
    Var('Sugarcanefarming_Ninbiomass_residue', 445.2, notes='N content of above and below ground biomass: grams'),
    Var('Sugarcane_NinVinasse', 205.2, notes='N content of above and below ground biomass: grams'),
    Var('Sugarcane_NinFilteredcake', 35.8783008036739, notes='N content of filtered cake as soil amendment'),
    Var('Sugarcanefarming_biomass_N2O_factor', 0.01264, notes='N2O Emissions: N in N2O as % of N in biomass'),
    Var('Nfertilizer_N2O_factor_Brazil', 0.0122, notes='N2O Emissions: N fertilizer in Brazillian sugarcane fields'),
    ### Rice: N content of above and below ground biomass and N2O Emission ###
    Var('Ricefarming_Ninbiomass_residue', 535.140584128, notes='N content of above and below ground biomass: gram N/cwt rice '),
    Var('Ricefarming_biomass_N2O_factor', 0.01264, notes='N2O Emissions: N in N2O as % of N in rice biomass'),
    Var('EFc', 0.65, 'kg CH4/ha/day'),
    Var('Rice_cultivation_period', 139, 'day'),
    Var('Rice_straw_application_rate', 4, 'Mg/ha'),
    ### Rye cover crop: yield, N content in biomass, and N2O Emission ###
    Var('RyeCCfarming_biomass_N2O_factor', 0.01264, 'g N2O-N/g-N'),
    Var('RyeCCfarming_Ncontent', 0.016, 'ton-N/dry ton-cover crop'),
    ### Manure N and P2O5 content ###
    Var('Swine_manure_N', 1279.1304834, 'g N/ton manure'),
    Var('Dairy_manure_N', 1950.447191, 'g N/ton manure'),
    Var('Cattle_manure_N', 1991.2705043, 'g N/ton manure'),
    Var('Chicken_manure_N', 7302.837157, 'g N/ton manure'),
    Var('Manure_transportation_energy_ton_mile', 10416.49299, 'Btu/ton manure/mile'),
    Var('Manure_transportation_distance_mile', 0.367, 'mile'),
    Var('Manure_N2O_factor', 0.01474, 'g-N2O-N/g-N applied'),
    ### Global warming potential ###
    Var('CO2_GWP', 1, 'kg CO2e/kg CO2'),
    Var('CH4_GWP', 29.8, 'kg CO2e/kg CH4'),
    Var('N2O_GWP', 273, 'kg CO2e/kg N2O'),
    Var('Biogenic_CH4_GWP', 28, 'kg CO2e/kg CH4'),
    
    # =========================================================================
    # Sheet "Intermediate"
    # =========================================================================
    ]

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


        
    
# %%