#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

from thermosteam.units_of_measure import AbsoluteUnitsOfMeasure as auom

__all__ = ('Inputs', 'Var', 'default_inputs',)


class Var:
    '''
    A simple class used to represent variable value with unit of measurement.
    
    Parameters
    ----------
    name : str
        Name of this variable.
    default_value : int|float
        Default value of this variable.
    default_unit : str
        Default unit of measurement of this variable.
    notes : str
        Additional notes on this variable.
    enable_unit_conversion : bool
        Whether to enable unit conversion.
        
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
    def __init__(self, name, default_value, default_unit, notes='', enable_unit_conversion=False):
        self.name = name
        self._default_value = default_value
        self._default_unit = default_unit
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
            unit = self.default_unit
            val = self.default_value
        return f'{self.name}: {val} {unit}'
        
    def __call__(self, new_unit=None):
        val = self.default_value
        if not new_unit: return val
        if not self.enable_unit_conversion:
            raise ValueError('Unit conversion is not enabled.')
        unit = new_unit
        return auom(unit).convert(val, new_unit)
    
    @property
    def default_value(self):
        '''Default value of this variable.'''
        return self._default_value
    
    @property
    def default_unit(self):
        '''Default unit of this variable.'''
        return self._default_unit


# %%

class Variables:
    '''
    A general class to store parameter and input values, not intended to be used standalone
    (i.e., only its subclasses should be used).
    '''
    acronyms = {
        'ac': 'acre',
        'AN': 'ammonium nitrate',
        'AS': 'ammonium sulfate',
        'bu': 'bushel',
        'CF': 'characterization factor',
        'bu': 'bushels',
        'cwt': 'hundredweight, or 100 lbs',
        'GB': 'gasoline blendstock',
        'GS': 'grain sorghum',
        'ha': 'hectare',
        'Lime': 'CaCO3',
        'LPG': 'liquid petroleum gas',
        'NA': 'nitric acid',
        'NG': 'natural gas',
        'PA': 'phosphoric acid',
        'RO': 'residual oil',
        'SA': 'sulfuric acid',
        'TD': 'transportation & distribution',
        'UAN': 'urea-ammonium nitrate solution',
        }
    
    def reset_variables(self, variables=[]):
        '''
        Reset variable to their default values.
        '''
        variables = variables or self.variables
        for var in self.variables:
            setattr(self, var.name, var.default_value)


# %%

default_inputs = [    
    Var('Nfertilizer_source', 'Conventional',
        notes='Can only be "Conventional" (steam methane reforming) or '
        '"Green" (refer to GREET for the default green ammonia pathway).'),
    ]


class Inputs(Variables):
    '''A general class to store crop inputs.'''

    def __init__(self, inputs=[]):
        self.inputs = inputs or default_inputs
            
        
    @property
    def parameters(self):
         return {}

    @property
    def variables(self):
         return self.inputs
     

# %%

# =============================================================================
# Probably not needed, saving as a ref for now
# =============================================================================

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