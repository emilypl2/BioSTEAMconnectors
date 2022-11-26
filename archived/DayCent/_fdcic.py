# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 09:49:03 2021

@author: Yalin Li
"""

import pandas as pd, xlwings as xw
# from math import floor, ceil
# from matplotlib import pyplot as plt

__all__ = ('run_FDCIC',)


def num_to_col(num):
    '''Convert number to Excel column letters'''
    col = ''
    while num > 0:
        num, r = divmod(num-1, 26)
        col = chr(65+r) + col
    return col


def run_FDCIC(data_path, fdcic_path):
    # Copy data from the processed DayCent outputs to FD-CICd
    data = pd.read_excel(data_path, sheet_name='outputs', index_col=0)
    letter = num_to_col(data.shape[1]+1) # +1 for the index column
    fdcic = xw.Book(fdcic_path)
    inputs = fdcic.sheets['Macro Inputs']
    inputs.clear_contents()
    # inputs.range(f'A:{letter}').value = data.copy()
    inputs.range(f'A:{letter}').value = data

    # Run Macro
    run_macro = fdcic.macro('Run_Macro')
    run_macro()
    fdcic.save()
    fdcic.app.quit() # use `close` won't close the Excel app



# %%

# =============================================================================
# Legacy codes not in use now, may convert to make plots
# =============================================================================

# # Function to make plots
# def make_plots(macro_outputs):
#     # Make a new folder if there isn't one
#     if not os.path.isdir('Plots'):
#         os.mkdir('Plots')

#     # Find a good brackets for y axis
#     GHG_lower = floor((np.array(macro_outputs.GHG_per_bu[2:], 'float')/1000).min())*1000
#     GHG_upper = ceil((np.array(macro_outputs.GHG_per_bu[2:], 'float')/1000).max())*1000

#     for crop in ('corn', 'soybean'):
#         crop_data = macro_outputs[macro_outputs.CROP_type==crop]
#         for expt in crop_data.Experiment.unique():
#             fig, ax = plt.subplots(figsize=(8, 4.5))
#             data = crop_data[crop_data.Experiment==expt]
#             ax.bar(data.Replication, data.GHG_per_bu)
#             xrange = range(data.Replication.min()-1, data.Replication.max()+1)
#             ax.set(xlim=(data.Replication.min()-1, data.Replication.max()+1),
#                    xticks=xrange, xticklabels=['', *data.Replication],
#                    ylim=(GHG_lower, GHG_upper),
#                    xlabel=f'Experiment # {expt}',
#                    ylabel='GHG [gCO2e/bu]')
#             ax.figure.savefig(f'Plots/{crop}_expt_{expt}.png', dpi=100)
#             plt.close(fig)


# make_plots(macro_outputs)