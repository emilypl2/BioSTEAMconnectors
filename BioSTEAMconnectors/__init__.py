#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

import os
from warnings import warn
path = os.path.dirname(__file__)
inputs_path = os.path.join(path, 'inputs')
if not os.path.isdir(inputs_path):
    warn(f'No input files available at {inputs_path}.')
outputs_path = os.path.join(path, 'outputs')
if not os.path.isdir(outputs_path): os.mkdir(outputs_path)

from . import _variables
from ._variables import *
from . import _default_parameters
from ._default_parameters import *
from . import _default_inputs
from ._default_inputs import *

from . import _inputs
from . import _fdcic

from ._inputs import *
from ._fdcic import *

__all__ = (
    'path',
    'inputs_path',
    'outputs_path',
    *_variables.__all__,
    *_default_parameters.__all__,
    *_default_inputs.__all__,
    *_inputs.__all__,
    *_fdcic.__all__,
    )