# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 18:45:18 2023

@author: Empli
"""
import pandas as pd, os
join = os.path.join
from BioSTEAMconnectors import SorghumInputs, SugarcaneInputs, FDCIC, inputs_path, outputs_path

gtokg = 1000
m2_per_ha = 10000

def update_results(inputs):
    outputs = pd.DataFrame(inputs.copy())
    outputs['temp_CO2eq'] = pd.Series(dtype='int')
    outputs['temp_CO2eq_without_SOC'] = pd.Series(dtype='int')
    inputs = inputs.T
    for i in inputs:
        if outputs.loc[i,'Crop'] == 'Sorghum':
            fdcic = FDCIC(crop_inputs = SorghumInputs())
            fdcic.SOC_emission = (outputs.loc[i,'Delta_soilC_gCm2'])/gtokg*m2_per_ha
            ser = fdcic.GHG_table
            outputs.loc[i,'temp_CO2eq'] = ser['CI with SOC']
            outputs.loc[i,'temp_CO2eq_without_SOC'] = ser['CI without SOC']
        elif outputs.loc[i,'Crop'] == 'Sugarcane':
            fdcic = FDCIC(crop_inputs = SugarcaneInputs())
            #!!! convert units when we get DayCent outputs and set SOC emissions
            #fdcic.SOC_emission = (outputs.loc[i,'Delta_soilC_gCm2'])/gtokg*m2_per_ha
            ser = fdcic.GHG_table
            outputs.loc[i,'temp_CO2eq'] = ser['CI with SOC'] 
            outputs.loc[i,'temp_CO2eq_without_SOC'] = ser['CI without SOC']
        else:
            outputs.iloc[i, -1] = 0
            outputs.iloc[i, -2] = 0
    outputs = outputs.rename(columns={'temp_CO2eq': f'{ser.unit}', 'temp_CO2eq_without_SOC': f'{ser.unit} without SOC'})
    return outputs
        
data_path = join(inputs_path, 'SORG.csv')
#data_wb = pd.ExcelFile(data_path)
#inputs = pd.read_csv(data_wb, sheet_name='FDCIC', header=[0], index_col=0).reset_index(drop=True)
inputs = pd.read_csv(data_path, header=[0], index_col=0).reset_index(drop=True)
outputs = update_results(inputs)
output_path = join(outputs_path, 'Complete_CI.csv')
outputs.to_csv(output_path) 
#data_wb.close()



