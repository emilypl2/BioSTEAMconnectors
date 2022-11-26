#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

from . import (
    Variables,
    default_corn_inputs,
    default_rice_inputs,
    )

__all__ = (
    'Inputs',
    'CornInputs',
    'RiceInputs',
    )


# %%

class Inputs(Variables):
    '''A general class to store crop inputs.'''

    def __init__(self, inputs=[]):
        self.inputs = inputs    
        
    @property
    def parameters(self):
         return {}

    @property
    def variables(self):
         return self.inputs


# %%

class CornInputs(Inputs):
    '''User inputs for corn.'''
    
    def __init__(self, inputs=[]):
        self.inputs = inputs or default_corn_inputs
        self.reset_variables()

    @property
    def crop(self):
        return 'Corn'
    
    @property
    def GHG_functional_unit(self):
        return 'bu'

    @property
    def Nfertilizer_source_corn(self):
        '''Same as `Nfertilizer_source`.'''
        return self.Nfertilizer_source
    @Nfertilizer_source_corn.setter
    def Nfertilizer_source_corn(self, i):
        self.Nfertilizer_source = i
        
    @property
    def Yield_TS(self):
        '''Same as `CornYield_TS`, in `CornInputs.GHG_functional_unit`/acre.'''
        return self.CornYield_TS
    @Yield_TS.setter
    def Yield_TS(self, i):
        self.CornYield_TS = i
        

# %%

class RiceInputs(Inputs):
    '''User inputs for corn.'''
    
    def __init__(self, inputs=[]):
        self.inputs = inputs or default_rice_inputs
        self.reset_variables()

    @property
    def crop(self):
        return 'Rice'
    
    @property
    def GHG_functional_unit(self):
        return 'cwt'

    @property
    def Nfertilizer_source_Rice(self):
        '''Same as `Nfertilizer_source`.'''
        return self.Nfertilizer_source
    @Nfertilizer_source_Rice.setter
    def Nfertilizer_source_Rice(self, i):
        self.Nfertilizer_source = i
        
    @property
    def Yield_TS(self):
        '''Same as `RiceYield_TS`, in `RiceInputs.GHG_functional_unit`/acre.'''
        return self.RiceYield_TS
    @Yield_TS.setter
    def Yield_TS(self, i):
        self.RiceYield_TS = i