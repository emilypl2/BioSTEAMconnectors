==================
BioSTEAMconnectors
==================

Status
------
.. image:: https://img.shields.io/badge/status-under%20development-orange

This package aims to connect `BioSTEAM <https://biosteam.readthedocs.io>`_ with upstream ecosystem models by accounting for the costs and environmental impacts during cultivation and transportation of biorefinery feedstocks. Current efforts focus on the development of a Python class for carbon intensity calculation as in the Feedstock Carbon Intensity Calculator (`FDCIC <https://greet.es.anl.gov/tool_fd_cic>`_) of `GREET <https://greet.es.anl.gov/>`_.

Work is still in progress and module structure is subject to (potentially significant) change, but you can get some quick results with the following codes:

.. code::

	>>> from BioSTEAMconnectors import CornInputs, FDCIC
	>>> # Provide crop-specific inputs,
	>>> # default values are used if no user-inputs are provided
	>>> inputs = CornInputs()
	>>> fdcic = FDCIC(crop_inputs=inputs)
	>>> ser = fdcic.GHG_table
	>>> print(ser)
	crop                         Corn
	unit                    g CO2e/bu
	Diesel_GHG                    493
	Gasoline_GHG                 77.1
	NG_GHG                       39.4
	LPG_GHG                      86.2
	Electricity_GHG               181
	Ammonia_GHG                   426
	Urea_GHG                      263
	AN_GHG                       56.6
	AS_GHG                       30.2
	UAN_GHG                       692
	MAP_asNfert_GHG              72.3
	DAP_asNfert_GHG               124
	N2O_Fert_and_Res_GHG     3.13e+03
	Urea_CO2_GHG                  248
	MAP_asPfert_GHG               172
	DAP_asPfert_GHG               143
	K2O_GHG                      84.6
	Lime_GHG                       14
	Lime_CO2_GHG                  315
	Herbicide_GHG                 110
	Insecticide_GHG             0.271
	SOC_GHG                      3.96
	CI without SOC           6.76e+03
	CI with SOC              6.77e+03
	dtype: object
	# Default CI does not include soil organic carbon
	>>> print(fdcic.CI)
	6762.4230575623815
	>>> print(fdcic.CI_w_SOC)
	6766.387434292097