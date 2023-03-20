# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 18:45:18 2023

@author: Empli
"""
import pandas as pd, os
join = os.path.join
from BioSTEAMconnectors import SorghumInputs, FDCIC, inputs_path, outputs_path

gtokg = 1000
kgtoton = 907.185 #US TON 
m2_per_ha = 10000
grain_sorg_bu_per_acre = 81.8 #GREET Default
sweet_sorg_ton_per_acre = 13.785714285714286 #!!! average silage sorghum https://legacy.rma.usda.gov/pubs/2015/biomass_sorghum_data_gathering_report.pdf
sorg_bu_per_ton = 39.368 #https://grains.org/markets-tools-data/tools/converting-grain-units/


def update_results(inputs):
    outputs = pd.DataFrame(inputs.copy())
    outputs['temp_BSC_CO2eq'] = pd.Series(dtype='int')
    outputs['temp_BSC_CO2eq_without_SOC'] = pd.Series(dtype='int')
    outputs['temp_total_CO2eq'] = pd.Series(dtype='int')
    outputs['temp_total_CO2eq_without_SOC'] = pd.Series(dtype='int')
    inputs = inputs.T
    for i in inputs:
        if outputs.loc[i,'Crop'] == 'Sorghum':
            SorghumInputs.Yield_TS = outputs.loc[i,'AbovegroundBiomass_gCm']/0.45 #0.45 Carbon ration in drymatter
            fieldGHG = outputs.loc[i,'net_GHG_gCO2e']/(SorghumInputs.Yield_TS*gtokg*kgtoton) #gCO2eq/tonDW
            fdcic = FDCIC(crop_inputs = SorghumInputs())
            fdcic.SOC_emission = (outputs.loc[i,'Delta_soilC_gCm2'])/gtokg*m2_per_ha
            ser = fdcic.GHG_table
            if outputs.loc[i,'SorgType'] == 'SweetSorghum':
                grain_to_sweet = grain_sorg_bu_per_acre*(1/sweet_sorg_ton_per_acre) #bu grain sorg per ton sweet sorg
                outputs.loc[i,'temp_BSC_CO2eq'] = ser['CI with SOC']*grain_to_sweet
                outputs.loc[i,'temp_BSC_CO2eq_without_SOC'] = ser['CI without SOC']*grain_to_sweet
                outputs.loc[i,'temp_total_CO2eq'] = (ser['CI with SOC']*grain_to_sweet) +fieldGHG
                outputs.loc[i,'temp_total_CO2eq_without_SOC'] = (ser['CI without SOC']*grain_to_sweet)+fieldGHG
            else: 
                outputs.loc[i,'temp_BSC_CO2eq'] = ser['CI with SOC']*sorg_bu_per_ton 
                outputs.loc[i,'temp_BSC_CO2eq_without_SOC'] = ser['CI without SOC']*sorg_bu_per_ton 
                outputs.loc[i,'temp_total_CO2eq'] = (ser['CI with SOC']*sorg_bu_per_ton)+fieldGHG
                outputs.loc[i,'temp_total_CO2eq_without_SOC'] = (ser['CI without SOC']*sorg_bu_per_ton)+fieldGHG 
        #elif outputs.loc[i,'Crop'] == 'Sugarcane':
            #SugarcaneInputs.Yield_TS = outputs.loc[i,'AbovegroundBiomass_gCm']
            #fdcic = FDCIC(crop_inputs = SugarcaneInputs())
            #!!! convert units when we get DayCent outputs and set SOC emissions
            #fdcic.SOC_emission = (outputs.loc[i,'Delta_soilC_gCm2'])/gtokg*m2_per_ha
            #!!! add things for fieldGHG
            #ser = fdcic.GHG_table
            #outputs.loc[i,'temp_BSC_CO2eq'] = ser['CI with SOC'] 
            #outputs.loc[i,'temp_BSC_CO2eq_without_SOC'] = ser['CI without SOC']
        else:
           outputs.loc[i,'temp_BSC_CO2eq'] = 0
           outputs.loc[i,'temp_BSC_CO2eq_without_SOC'] = 0
           outputs.loc[i,'temp_total_CO2eq'] = 0
           outputs.loc[i,'temp_total_CO2eq_without_SOC'] = 0
    outputs = outputs.rename(columns={'temp_BSC_CO2eq': 'BSC g CO2eq/ton', 'temp_BSC_CO2eq_without_SOC': 'BSC gCO2eq/ton without SOC', 'temp_total_CO2eq': 'total g CO2eq/ton', 'temp_total_CO2eq_without_SOC': 'total g CO2eq without SOC'})
    return outputs
        
data_path = join(inputs_path, 'SORG.csv')
#data_wb = pd.ExcelFile(data_path)
#inputs = pd.read_csv(data_wb, sheet_name='FDCIC', header=[0], index_col=0).reset_index(drop=True)
inputs = pd.read_csv(data_path, header=[0], index_col=0).reset_index(drop=True)
outputs = update_results(inputs)
output_path = join(outputs_path, 'Complete_CI.csv')
outputs.to_csv(output_path) 
#data_wb.close()



