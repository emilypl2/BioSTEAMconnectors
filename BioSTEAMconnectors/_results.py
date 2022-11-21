#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

__all__ = ('Results',)


class Results:
    '''
    A general class to calculate the carbon intensity, not intended to be used standalone
    (i.e., only its subclasses should be used).
    
    Parameters
    ----------
    FDCIC : obj
        The `class`:`FDCIC` object (with crop inputs provided) for calculation.
    '''
    
    def __init__(self, FDCIC):
        self.FDCIC = FDCIC

            
    @property
    def crop(self):
         return self.FDCIC.crop

    @property
    def crop_inputs(self):
         return self.FDCIC.crop_inputs
    
    #!!! PAUSED
    @property
    def Diesel_GHG(self):
        '''In g GHG/bu.'''
        FDCIC = self.FDCIC
        return (
            FDCIC.Diesel_Farming + 
            FDCIC.Diesel_RyeCCFarming +
            FDCIC.Diesel_ManureApplication +
            FDCIC.Diesel_ManureTransportation
            ) * FDCIC.CF_Diesel
        
    @property
    def Gasoline_GHG(self):
        '''In g GHG/bu.'''
        FDCIC = self.FDCIC
        return FDCIC.Gasoline_Farming * FDCIC.CF_Gasoline