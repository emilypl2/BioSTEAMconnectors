#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

from . import Var

__all__ = ('default_rice_inputs',)

default_rice_inputs = [
    # Related to N content of above and below ground biomass and N2O Emission 
    Var('Rice_water_regime_during_cultivation', 'Continuously flooded',
        notes='Can only be one of "Continuously flooded", "Single drainage period", '
        '"Multiple drainage period", "Regular rainfed", "Drought prone", or "Deep water".'),
    Var('Rice_water_regime_pre_season', 'Non flooded pre-season >365 d',
        notes='Can only be one of "Non flooded pre-season <180 d", "Non flooded pre-season >180 d", '
        '"Flooded pre-season (>30 d)", or "Non-flooded pre-season >365 d".'),
    Var('Rice_time_for_straw_incorporation',
        'Straw incorporated shortly (<30 days) before cultivation',
        notes='Can only be "Straw incorporated shortly (<30 days) before cultivation" or '
        '"Straw incorporated long (>30 days) before cultivation"'),
    ]
