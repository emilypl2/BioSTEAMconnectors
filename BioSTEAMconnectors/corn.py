#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

from . import Var

__all__ = ('default_corn_inputs',)

default_corn_inputs = [
    # Yield
    Var('CornYield_TS', 178.4, 'bu/acre'),
    # Energy
    Var('Diesel_CornFarming_usage', 7.2216825542863, 'gal/acre'),
    Var('Gasoline_CornFarming_usage', 1.27596490556539, 'gal/acre'),
    Var('NG_CornFarming_usage', 86.9829190935403, 'ft3/acre'),
    Var('LPG_CornFarming_usage', 2.15424982868667, 'gal/acre'),
    Var('Electricity_CornFarming_usage', 69.3252376020865, 'kWh/acre'),

    #!!!PAUSED HERE AT ADDING THE ONES FOR THE N FERTILIZERS
    
    
    # Related to regionalized N2O emission factors table
    Var('Climate_zone', 'No consideration',
        notes='Can only be one of "No consideration", "NA", "Wet or Moist", or "Dry".'),
    Var('Nfertilizer_N2O_factor_US_rice', 0.004+0.00374, notes='direct and indirect'),
    # Related to 4R nitrogen management practice for corn farming
    Var('N_balance_assumed', 0, 'kg N/ha'),
    ]
