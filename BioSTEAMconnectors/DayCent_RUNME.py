# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 12:04:14 2021

@author: Yalin Li
"""

import os
path = os.path.dirname(__file__)
os.sys.path.insert(0, path)
from DayCent import run_DayCent_connector
run_DayCent_connector()