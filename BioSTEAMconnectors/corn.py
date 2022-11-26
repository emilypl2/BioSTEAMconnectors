#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

from BioSTEAMconnectors import CornInputs, FDCIC

inputs = CornInputs()
fdcic = self = FDCIC(crop_inputs=inputs)
ser = fdcic.GHG_table
print(ser)
print(fdcic.CI)
print(fdcic.CI_w_SOC)
