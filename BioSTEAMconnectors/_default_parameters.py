#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BioSTEAMconnectors
# Copyright (C) 2022-, Yalin Li <mailto.yalin.li@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.

'''Default parameter values in FDCIC'''

from . import Variable

__all__ = ('default_parameters',)

# In sheet "Parameters", values here are pulled from GREET
default_parameters = [
    # Lower Heating Values of fuels/Fuel specification
    Variable('Diesel_LHV', 128450, 'Btu/gal'),
    Variable('Gasoline_LHV', 112194, 'Btu/gal'),
    Variable('Ethanol_LHV', 76330, 'Btu/gal'),
    Variable('NG_LHV', 983, 'Btu/ft3', notes='natural gas'),
    Variable('LPG_LHV', 84950, 'Btu/gal', notes='liquid petroleum gas'),
    Variable('Electricity_LHV', 3412, 'Btu/kWh'),
    # Unit conversion, name has been revised to be more consistent and prevents misuse
    Variable('g_per_lb', 453.592, 'g/lb'),
    Variable('Btu_per_MJ', 947.817, 'Btu/MJ'),
    Variable('tonne_per_lb', 0.000453593, 'tonne/lb'),
    Variable('kg_per_lb', 0.4535925, 'kg/lb'),
    Variable('lb_per_bu_CanCorn', 56, 'lb/bu'),
    Variable('L_per_gal', 3.78541, 'L/gal'),
    Variable('acre_per_hectare', 2.47105, 'ac/ha'),
    Variable('g_per_kg', 1000, 'g/kg'),
    Variable('kJ_per_MJ', 1000, 'kJ/MJ'),
    Variable('kJ_per_kWh', 3600, 'kJ/kWh'),
    Variable('kJ_per_GJ', 1000000, 'kJ/GJ'),
    Variable('g_per_ton', 907184.74, 'g/ton'),
    Variable('NG_density', 22, 'g/ft3'),
    # Emission factor from synthetic nitrogen fertilizer
    Variable('Nfertilizer_N2O_factor_US', 0.01325, ''),
    # N content in Nitrogen fertilizer
    Variable('Ammonia_N', 0.824, 'g N/g mass'), # 14/17
    Variable('Urea_N', 0.467, 'g N/g mass'), # 28/60
    Variable('AN_N', 0.35, 'g N/g mass', notes='ammonium nitrate'), # 28/80
    Variable('AS_N', 0.211999, 'g N/g mass', notes='ammonium sulfate'), # 28/132
    Variable('UAN_N', 1,), # unsure why it's 1, maybe because it's as N
    Variable('MAP_N', 0.11, 'monoammonium phosphate'), #!!! why 0.11? should be 14/115=0.122
    Variable('DAP_N', 0.16, 'diammonium phosphate'), #!!! why 0.11? should be 28/132=0.212
    Variable('MAP_share_as_Nfert', 0.31139559, ''), # 14/(14+31) between N and P
    Variable('DAP_share_as_Nfert', 0.474907149, ''), # 28/(28+31) between N and P
    Variable('N2O_N_to_N2O', 1.571428571, 'g N/g N2O'), # 44/28
    Variable('CO2_C_to_CO2', 3.666666667, 'g C/g CO2'), # 44/12
    Variable('Urea_N_to_CO2', 1.571428571, 'g N/g urea'), # 60/28
    Variable('Urea_N', 0.467, 'g CO2/g N in urea'), # 44/28 (MW of CO2 over MW of N)
    # P2O5 content in Phosphorus fertilizer
    Variable('MAP_P2O5', 0.48),
    Variable('DAP_P2O5', 0.48),
    # Lime acidified
    Variable('CO2_content_in_CaCO3', 0.44, 'g CO2/g CaCO3'), # 44/100
    Variable('Percent_Lime_Acidified', 0.492, 'fraction'),
    # Corn: N content of above and below ground biomass and N2O Emission
    Variable('Cornfarming_Ninbiomass_residue', 141.6, 'g/bu'),
    Variable('Cornfarming_biomass_N2O_factor', 0.01264, 'fraction'),
    # Soybean: N content of above and below ground biomass and N2O Emission
    Variable('Soybeanfarming_Ninbiomass_residue', 557, 'g/bu'),
    Variable('Soybeanfarming_Nfixation_N2O_factor', 7.3, 'fraction'),
    Variable('Soybeanfarming_biomass_N2O_factor', 0.01264, 'fraction'),
    Variable('Nfertilizer_N2O_factor_US_soybean', 0.01374, 'fraction'),
    # GS: N content of above and below ground biomass and N2O Emission
    Variable('GSfarming_Ninbiomass_residue', 149),
    Variable('GSfarming_biomass_N2O_factor', 0.01264, 'fraction'),
    Variable('Nfertilizer_N2O_factor_US_sorghum', 0.01374, 'fraction'),
    # Sugarcane: N content of above and below ground biomass and N2O Emission
    Variable('Sugarcanefarming_Ninbiomass_residue', 445.2, 'g/tonne'),
    Variable('Sugarcane_NinVinasse', 205.2, 'g/tonne'),
    Variable('Sugarcane_NinFilteredcake', 35.8783008036739, 'g/tonne'),
    Variable('Sugarcanefarming_biomass_N2O_factor', 0.01264, 'fraction'),
    Variable('Nfertilizer_N2O_factor_Brazil', 0.0122, 'fraction'),
    # Rice: N content of above and below ground biomass and N2O Emission
    Variable('Ricefarming_Ninbiomass_residue', 535.140584128, 'g/cwt'),
    Variable('Ricefarming_biomass_N2O_factor', 0.01264, 'fraction'),
    Variable('EFc', 0.65, 'kg CH4/ha/day'),
    Variable('Rice_cultivation_period', 139, 'day'),
    Variable('Rice_straw_application_rate', 4, 'Mg/ha'),
    # Rye cover crop: yield, N content in biomass, and N2O Emission
    Variable('RyeCCfarming_biomass_N2O_factor', 0.01264, 'g N2O-N/g-N'),
    Variable('RyeCCfarming_Ncontent', 0.016, 'ton-N/dry ton-cover crop'),
    # Manure N and P2O5 content
    Variable('Swine_manure_N', 1279.1304834, 'g N/ton manure'),
    Variable('Dairy_manure_N', 1950.447191, 'g N/ton manure'),
    Variable('Cattle_manure_N', 1991.2705043, 'g N/ton manure'),
    Variable('Chicken_manure_N', 7302.837157, 'g N/ton manure'),
    Variable('Manure_transportation_energy_ton_mile', 10416.49299, 'Btu/ton manure/mile'),
    Variable('Manure_transportation_distance_mile', 0.367, 'mile'),
    Variable('Manure_N2O_factor', 0.01474, 'g-N2O-N/g-N applied'),
    # Global warming potential
    Variable('CO2_GWP', 1, 'kg CO2e/kg CO2'),
    Variable('CH4_GWP', 29.8, 'kg CO2e/kg CH4'),
    Variable('N2O_GWP', 273, 'kg CO2e/kg N2O'),
    Variable('Biogenic_CH4_GWP', 28, 'kg CO2e/kg CH4'),
    ]

# In sheet "Intermediate", values here are calculated based off GREET values
default_parameters.extend([
    ### Production Usage Amount ###
    # Ammonia
    Variable('Ammonia_Prod_NGIn', 27.9613103359878, 'mmBtu/ton'),
    Variable('Ammonia_Prod_ElecIn', 0.188560619556814, 'mmBtu/ton'),
    Variable('Ammonia_Prod_HydrogenIn', 0, 'ton/ton'),
    Variable('Ammonia_Prod_NitrogenIn', 0, 'ton/ton'),
    Variable('Green_Ammonia_Prod_NGIn', 27.9613103359878, 'mmBtu/ton'),
    Variable('Green_Ammonia_Prod_ElecIn', 1.11135683852937, 'mmBtu/ton'),
    Variable('Green_Ammonia_Prod_HydrogenIn', 0.197284, 'ton/ton'),
    Variable('Green_Ammonia_Prod_NitrogenIn', 0.929778, 'ton/ton'),
    # Urea
    Variable('Urea_Prod_NGIn', 3.98108341487325, 'mmBtu/ton'),
    Variable('Urea_Prod_ElecIn', 0.455717971896938, 'mmBtu/ton'),
    Variable('Urea_Prod_AmmoniaIn', 0.567, 'ton ammonia/ton'),
    # Nitric Acid (for sugarcane)
    Variable('NA_Prod_AmmoniaIn', 0.288, 'ton ammonia/ton'),
    # Ammonium Nitrate
    Variable('AN_Prod_NGIn', 0.636285470195725, 'mmBtu/ton'),
    Variable('AN_Prod_ElecIn', 0.214961307498556, 'mmBtu/ton'),
    Variable('AN_Prod_AmmoniaIn', 0.213, 'ton ammonia/ton'),
    Variable('AN_Prod_NAIn', 0.788, 'ton nitric acid/ton'),
    # Ammonium Sulfate
    Variable('AS_Prod_AmmoniaIn', 0.257765731251332, 'ton ammonia/ton'),
    Variable('AS_Prod_SAIn', 0.742234268748668, 'ton sulfuric acid/ton'),
    # Urea-ammonium nitrate solution
    Variable('UAN_Prod_NGIn', 0.137575236799076, 'mmBtu/ton'),
    Variable('UAN_Prod_ElecIn', 0.481513328796765, 'mmBtu/ton'),
    Variable('UAN_Prod_UreaIn', 1.09, 'ton urea/ton'),
    Variable('UAN_Prod_ANIn', 1.43, 'ton AN/ton'),
    # MAP
    Variable('MAP_Prod_NGIn', 0.283748925898093, 'mmBtu/ton'),
    Variable('MAP_Prod_ElecIn', 0.103181427599307, 'mmBtu/ton'),
    Variable('MAP_Prod_AmmoniaIn', 0.133, 'ton ammonia/ton'),
    Variable('MAP_Prod_PAIn', 0.784346173469388, 'ton phosphoric acid/ton',
             notes='In GREET, H3PO4 is reacted with ammonia; '
             'In this cell, the number is already adjusted to P2O5 value'),
    # DAP
    Variable('DAP_Prod_NGIn', 0.23215821209844, 'mmBtu/ton'),
    Variable('DAP_Prod_ElecIn', 0.103181427599307, 'mmBtu/ton'),
    Variable('DAP_Prod_AmmoniaIn', 0.22, 'ton ammonia/ton'),
    Variable('DAP_Prod_PAIn', 0.719889285714286, 'ton phosphoric acid/ton',
             notes='In GREET, H3PO4 is reacted with ammonia; '
             'In this cell, the number is already adjusted to P2O5 value'),
    # K2O
    Variable('K2O_Prod_NGIn', 1.053, 'mmBtu/ton'),
    Variable('K2O_Prod_ElecIn', 1.638, 'mmBtu/ton'),
    Variable('K2O_Prod_DieselIn', 1.209, 'mmBtu/ton'),
    # Lime
    Variable('Lime_Prod_NGIn', 0.000002, 'mmBtu/ton'),
    Variable('Lime_Prod_ElecIn', 0.000244, 'mmBtu/ton'),
    Variable('Lime_Prod_ROIn', 0.001554, 'mmBtu/ton'),
    Variable('Lime_Prod_DieselIn', 0.012296, 'mmBtu/ton'),
    Variable('Lime_Prod_CoalIn', 0.003474, 'mmBtu/ton'),
    Variable('Lime_Prod_GasolineIn', 0.002428, 'mmBtu/ton', notes='gasoline blendstock'),
    # Brazilian Phosphate (P2O5)
    Variable('PA_Brazilian_Prod_ElecIn', 0.438521067297053, 'mmBtu/ton'),
    Variable('PA_Brazilian_Prod_PhosRockIn', 3.525, 'ton phosphoric rock/ton'),
    Variable('PA_Brazilian_Prod_SAIn', 2.73, 'ton sulfuric acid/ton'),
    # Brazilian Lime
    Variable('Lime_Brazilian_Prod_ElecIn', 0.022, 'mmBtu/ton'),
    Variable('Lime_Brazilian_Prod_DieselIn', 0.08, 'mmBtu/ton',),
    # Nitric acid, the original spreadsheet is "Nitrid", probably a typo
    Variable('NA_ElecIn', 0.0275150473598151, 'mmBtu/ton'),
    Variable('NA_AmmoniaIn', 0.288, 'ton ammonia/ton'),

    ### Upstream Inputs CI ###
    # Natural gas for ammonia
    Variable('NG_upstream_CO2_for_Ammonia', 6336.27495433342, 'g CO2/mmBtu'),
    Variable('NG_upstream_CH4_for_Ammonia', 209.647367838732, 'g CH4/mmBtu'),
    Variable('NG_upstream_N2O_for_Ammonia', 1.20338508869173, 'g N2O/mmBtu'),
    # Electricity
    Variable('Electricity_upstream_CO2', 127800.997787876, 'g CO2/mmBtu'),
    Variable('Electricity_upstream_CH4', 270.971245722998, 'g CH4/mmBtu'),
    Variable('Electricity_upstream_N2O', 2.59722458324966, 'g N2O/mmBtu'),
    # Natural gas as stationary fuels
    Variable('NG_upstream_CO2_for_StationaryFuel', 6612.51577425863, 'g CO2/mmBtu'),
    Variable('NG_upstream_CH4_for_StationaryFuel', 223.188741132914, 'g CH4/mmBtu'),
    Variable('NG_upstream_N2O_for_StationaryFuel', 1.41779149855698, 'g N2O/mmBtu'),
    # Nitric acid for Ammonia Nitrate (US)
    Variable('NA_Upstream_CO2', 75170.857071601, 'g CO2/ton'),
    Variable('NA_Upstream_CH4', 105.688518236322, 'g CH4/ton'),
    Variable('NA_Upstream_N2O', 4314.74953262626, 'g N2O/ton'),
    # Sulfuric acid for AS （ammonium sulfate)
    Variable('SA_Upstream_CO2', 37876.883582726, 'g CO2/ton'),
    Variable('SA_Upstream_CH4', 58.4724216450816, 'g CH4/ton'),
    Variable('SA_Upstream_N2O', 0.917706163476711, 'g N2O/ton'),
    # Phosphic acid (P2O5) for MAP/DAP
    Variable('PA_Upstream_CO2', 1223301.07996423, 'g CO2/ton',
             notes='instead of using the value for P2O5 directly from GREET, '
             'this number is adjusted since P2O5 is used as an intermediate for MAP/DAP production'),
    Variable('PA_Upstream_CH4', 2646.44140088924, 'g CH4/ton',
             notes='instead of using the value for P2O5 directly from GREET, '
             'this number is adjusted since P2O5 is used as an intermediate for MAP/DAP production'),
    Variable('PA_Upstream_N2O', 30.3585578183862, 'g N2O/ton',
             notes='instead of using the value for P2O5 directly from GREET, '
             'this number is adjusted since P2O5 is used as an intermediate for MAP/DAP production'),
    # Diesel as fuel
    Variable('Diesel_upstream_CO2', 13186.722667603, 'g CO2/mmBtu'),
    Variable('Diesel_upstream_CH4', 111.772244649243, 'g CH4/mmBtu'),
    Variable('Diesel_upstream_N2O', 0.244015821801455, 'g N2O/mmBtu'),
    # RO as fuel 
    Variable('RO_upstream_CO2', 10089.1978586435, 'g CO2/mmBtu'),
    Variable('RO_upstream_CH4', 102.151248520798, 'g CH4/mmBtu'),
    Variable('RO_upstream_N2O', 0.17225341835045, 'g N2O/mmBtu'),
    # Coal as fuel
    Variable('Coal_upstream_CO2', 1620.01544142514, 'g CO2/mmBtu'),
    Variable('Coal_upstream_CH4', 147.842989765332, 'g CH4/mmBtu'),
    Variable('Coal_upstream_N2O', 0.0330322808747223, 'g N2O/mmBtu'),
    # Gasoline blendstock as fuel
    Variable('GB_upstream_CO2', 17280.008954548, 'g CO2/mmBtu'),
    Variable('GB_upstream_CH4', 117.618105305705, 'g CH4/mmBtu'),
    Variable('GB_upstream_N2O', 0.303658433025717, 'g N2O/mmBtu'),
    # H2 as ammonia feedstock
    Variable('H2_upstream_CO2', 0, 'g CO2/ton'),
    Variable('H2_upstream_CH4', 0, 'g CH4/ton'),
    Variable('H2_upstream_N2O', 0, 'g N2O/ton'),
    # LPG as fuel
    Variable('LPG_upstream_CO2', 10270.9071851525, 'g CO2/mmBtu'),
    Variable('LPG_upstream_CH4', 143.922251990527, 'g CH4/mmBtu'),
    Variable('LPG_upstream_N2O', 0.190046157546839, 'g N2O/mmBtu'),
    # N2 as ammonia feedstock
    Variable('Cryogenic_Nitrogen_for_Ammonia_CO2', 60102.6359553953, 'g CO2/ton'),
    Variable('Cryogenic_Nitrogen_for_Ammonia_CH4', 127.433168895136, 'g CH4/ton'),
    Variable('Cryogenic_Nitrogen_for_Ammonia_N2O', 127.433168895136, 'g N2O/ton'),
    # Electricity for sorghum farming
    Variable('Electricity_upstream_CO2_GSfarming', 208012.449793143, 'g CO2/mmBtu'),
    Variable('Electricity_upstream_CH4_GSfarming', 399.414592088963, 'g CH4/mmBtu'),
    Variable('Electricity_upstream_N2O_GSfarming', 4.45697257919624, 'g N2O/mmBtu'),
    # Brazilian Electricity mix
    Variable('Electricity_Brazilian_upstream_CO2', 31134.2889933693, 'g CO2/mmBtu'),
    Variable('Electricity_Brazilian_upstream_CH4', 68.1540904421038, 'g CH4/mmBtu'),
    Variable('Electricity_Brazilian_upstream_N2O', 2.60720001275336, 'g N2O/mmBtu'),
    # Nitric acid for Ammonia Nitrate (Brazil)
    Variable('NA_Brazilian_Upstream_CO2', 49535.7667048375, 'g CO2/ton'),
    Variable('NA_Brazilian_Upstream_CH4', 59.9936612743312, 'g CH4/ton'),
    Variable('NA_Brazilian_Upstream_N2O', 4314.24657035987, 'g N2O/ton'),
    # Phosphoric rock (Brazil)
    Variable('PhosRock_Brazilian_Upstream_CO2', 223137.180388021, 'g CO2/ton'),
    Variable('PhosRock_Brazilian_Upstream_CH4', 516.989122373125, 'g CH4/ton'),
    Variable('PhosRock_Brazilian_Upstream_N2O', 6.58762980077705, 'g N2O/ton'),
    # Sulfuric acid for Phosphate (Brazil)
    Variable('SA_Brazilian_Upstream_CO2', 31559.884540055, 'g CO2/ton'),
    Variable('SA_Brazilian_Upstream_CH4', 45.2186780168568, 'g CH4/ton'),
    Variable('SA_Brazilian_Upstream_N2O', 0.91835804021288, 'g N2O/ton'),
    
    ### Product Emissions ###
    # Conventional Ammonia
    Variable('Ammonia_InputsCons_CO2', 418019.378867298, 'g CO2/ton'),
    Variable('Ammonia_InputsCons_GHG', 419299.093955674, 'g CO2/ton'),
    Variable('Ammonia_Process_CO2', 1282572.53476364, 'g CO2/ton'),
    Variable('Ammonia_Process_GHG', 1667878.98548293, 'g CO2/ton'),
    # Green Ammonia
    Variable('Green_Ammonia_InputsCons_CO2', 0, 'g CO2/ton'),
    Variable('Green_Ammonia_InputsCons_GHG', 0, 'g CO2/ton'),
    Variable('Green_Ammonia_Process_CO2', -150152.086092707, 'g CO2/ton'),
    Variable('Green_Ammonia_Process_GHG', -160472.300800874, 'g CO2/ton'),
    # Ammonia T&D
    Variable('Ammonia_TD_CO2_Final', 79892.0911666773, 'g CO2/ton'),
    Variable('Ammonia_TD_GHG_Final', 83116.232535494, 'g CO2/ton'),
    Variable('Ammonia_TD_CO2_Intermediate', 36177.2245218574, 'g CO2/ton'),
    Variable('Ammonia_TD_GHG_Intermediate', 37731.2996020379, 'g CO2/ton'),
    # Urea
    Variable('Urea_InputsCons_CO2', 236336.144795337, 'g CO2/ton'),
    Variable('Urea_InputsCons_GHG', 237059.658932989, 'g CO2/ton'),
    Variable('Urea_Process_CO2', -665268.809333333, 'g CO2/ton'),
    Variable('Urea_Process_GHG', -665268.809333333, 'g CO2/ton'),
    Variable('Urea_TD_CO2_Final', 92393.9719134906, 'g CO2/ton'),
    Variable('Urea_TD_GHG_Final', 96116.6959138755, 'g CO2/ton'),
    # Ammonia Nitrate
    Variable('AN_InputsCons_CO2', 37772.9475482828, 'g CO2/ton'),
    Variable('AN_InputsCons_GHG', 37888.5847970653, 'g CO2/ton'),
    Variable('AN_TD_CO2_Final', 83869.9623133906, 'g CO2/ton'),
    Variable('AN_TD_GHG_Final', 87252.7436104336, 'g CO2/ton'),
    # Ammonia Sulfate
    Variable('AS_TD_CO2_Final', 43714.8666448198, 'g CO2/ton'),
    Variable('AS_TD_GHG_Final', 45384.9329334561, 'g CO2/ton'),
    # Urea-ammonium nitrate solution
    Variable('UAN_InputsCons_CO2', 8167.123794, 'g CO2/ton'),
    Variable('UAN_InputsCons_GHG', 8192.126443, 'g CO2/ton'),
    Variable('UAN_TD_CO2_Final', 279566.541, 'g CO2/ton'),
    Variable('UAN_TD_GHG_Final', 290842.4787, 'g CO2/ton'),
    # MAP
    Variable('MAP_InputsCons_CO2', 16844.6928255856, 'g CO2/ton'),
    Variable('MAP_InputsCons_GHG', 16896.2607878805, 'g CO2/ton'),
    Variable('MAP_TD_CO2_Final', 43714.8666448198, 'g CO2/ton'),
    Variable('MAP_TD_GHG_Final', 45384.9329334561, 'g CO2/ton'),
    # DAP
    Variable('DAP_InputsCons_CO2', 13782.0214027518, 'g CO2/ton'),
    Variable('DAP_InputsCons_GHG', 13824.2133719022, 'g CO2/ton'),
    Variable('DAP_TD_CO2_Final', 43714.8666448198, 'g CO2/ton'),
    Variable('DAP_TD_GHG_Final', 45384.9329334561, 'g CO2/ton'),
    # K2O
    Variable('K2O_InputsCons_CO2', 156856.043783494, 'g CO2/ton'),
    Variable('K2O_InputsCons_GHG', 157379.714438794, 'g CO2/ton'),
    Variable('K2O_TD_CO2_Final', 85006.4969267373, 'g CO2/ton'),
    Variable('K2O_TD_GHG_Final', 88434.6039175592, 'g CO2/ton'),
    # Lime (US)
    Variable('Lime_InputsCons_CO2', 1615.68748023966, 'g CO2/ton'),
    Variable('Lime_InputsCons_GHG', 1625.72043123049, 'g CO2/ton'),
    Variable('Lime_TD_CO2_Final', 6505.50857920391, 'g CO2/ton'),
    Variable('Lime_TD_GHG_Final', 6752.39214215056, 'g CO2/ton'),
    # Diesel (US)
    Variable('CornFarming_DieselCons_CO2', 0.0776795063144252, 'g CO2/Btu'),
    Variable('CornFarming_DieselCons_GHG', 0.0782208477272848, 'g CO2/Btu'),
    # Gasoline (blendstock)
    Variable('CornFarming_GBCons_CO2', 0.0744767583446154, 'g CO2/Btu'),
    Variable('CornFarming_GBCons_GHG', 0.075194823011016, 'g CO2/Btu'),
    # Natural gas
    Variable('CornFarming_NGCons_CO2', 0.0568897869032699, 'g CO2/Btu'),
    Variable('CornFarming_NGCons_GHG', 0.0686122391032699, 'g CO2/Btu'),
    # Liquefied petroleum gas
    Variable('CornFarming_LPGCons_CO2', 0.0680396477962499, 'g CO2/Btu'),
    Variable('CornFarming_LPGCons_GHG', 0.0693835121962499, 'g CO2/Btu'),
    # Herbicide
    Variable('Herbicide_CornFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Variable('Herbicide_CornFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Variable('Herbicide_SoybeanFarming_CO2', 18.4435700710221, 'g CO2/ton'),
    Variable('Herbicide_SoybeanFarming_GHG', 19.5025381699089, 'g CO2/ton'),
    Variable('Insecticide_GSFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Variable('Insecticide_GSFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Variable('Herbicide_SugarcaneFarming_CO2', 14.6740189992022, 'g CO2/ton',
             notes='Assume the same as corn due to lack of data.'),
    Variable('Herbicide_SugarcaneFarming_GHG', 15.5005618973604, 'g CO2/ton',
             notes='Assume the same as corn due to lack of data.'),
    # Insecticide
    Variable('Insecticide_CornFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Variable('Insecticide_CornFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Variable('Insecticide_SoybeanFarming_CO2', 18.4435700710221, 'g CO2/ton'),
    Variable('Insecticide_SoybeanFarming_GHG', 19.5025381699089, 'g CO2/ton'),
    Variable('Insecticide_GSFarming_CO2', 17.8510998760147, 'g CO2/ton'),
    Variable('Insecticide_GSFarming_GHG', 18.875995540809, 'g CO2/ton'),
    Variable('Insecticide_SugarcaneFarming_CO2', 14.6740189992022, 'g CO2/ton',
             notes='Assume the same as corn due to lack of data.'),
    Variable('Insecticide_SugarcaneFarming_GHG', 15.5005618973604, 'g CO2/ton',
             notes='Assume the same as corn due to lack of data.'),
    # Brazilian Phosphate (P2O5)
    # Brazilian P2O5 production does not consume natural gas onsite,
    # and therefore, does not incur onsite GHG emissions
    Variable('PA_InputsCons_CO2', 0, 'g CO2/ton'),
    Variable('PA_InputsCons_GHG', 0, 'g CO2/ton'),
    Variable('PA_TD_CO2_Final', 86711.2988467573, 'g CO2/ton'),
    Variable('PA_TD_GHG_Final', 90207.3943782476, 'g CO2/ton'),
    # Brazilian Lime
    Variable('Brazilian_Lime_InputsCons_CO2', 6239.25302609347, 'g CO2/ton'),
    Variable('Brazilian_Lime_InputsCons_GHG', 6289.06159243846, 'g CO2/ton'),
    # Diesel (Brazilian)
    Variable('SugarcaneFarming_DieselCons_CO2', 0.0777608192847955, 'g CO2/Btu'),
    Variable('SugarcaneFarming_DieselCons_GHG', 0.0783650996008699, 'g CO2/Btu'),
    # Sugarcane soil amendment
    Variable('SugarcaneFarming_SoilAmendment_TD_CO2', 18.680313715969, 'g CO2/ton'),
    Variable('SugarcaneFarming_SoilAmendment_TD_GHG', 530.435404440136, 'g CO2/ton'),
    # Gasoline (Brazilian)
    Variable('SugarcaneFarming_GasolineCons_CO2', 0.0744767583446154, 'g CO2/Btu'),
    Variable('SugarcaneFarming_GasolineCons_GHG', 0.075194823011016, 'g CO2/Btu'),
    # Nitric acid, the original spreadsheet is "Nitrid", probably a typo
    Variable('NA_Process_CO2', 0, 'g CO2/ton'),
    Variable('NA_Process_GHG', 1177449, 'g CO2/ton'),
    Variable('NA_TD_CO2_Final', 48679.1052686707, 'g CO2/ton'),
    Variable('NA_TD_GHG_Final', 50731.7629804194, 'g CO2/ton'),    
    ])