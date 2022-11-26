#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

from thermosteam.units_of_measure import AbsoluteUnitsOfMeasure as auom

__all__ = ('Variable', 'Variables',)


class Variable:
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