# -*- coding: utf-8 -*-
"""
@author: Emily Lin; Yalin Li

TODO/Notes:
    Add in fertilizers
    Crop type and fertilizer
    No need for .c and .f files as long as .exe files are there
    Connect not necessarily needs to be in the same folder as the workspace folder
    Discover the individual sites?
    Let it automatically find schedule and extension files
"""

# %%

# =============================================================================
# Settings that can be updated
# =============================================================================

# Used constants
CFs = {
       'N2O': 265,
       'BioCH4': 28,
       }

EFs = {
       'leached': 0.025,
       'NO': 0.01,
       'vol': 0.01
       }

# Mass conversion
CtoCO2 = 44/12
CtoCH4 = 16/12
NtoN2O = 44/28
m2_per_acre = 4046.86

# Name of the executive files
dc_path = 'DayCent_CABBI.exe' # DayCent
dclist_path = 'list100_DayCent-CABBI.exe' # DayCent list100


# %%

__all__ = ('run_DayCent_connector',)

import os, subprocess, time, shutil, re
import numpy as np, pandas as pd
from . import _connector_path, run_FDCIC

# Functions that used a lot
isfile = os.path.isfile
join = os.path.join
cp = shutil.copy
mv = shutil.move
rm = os.remove


def run_DayCent(sch_file, extension):
    '''
    Runs DayCent with a specific schedule file.

    Parameters
    ----------
    sch_file: str
        Name of schedule file to be used
    extension: str
        whether or not there is an extension file and the extension .bin
    '''
    print(f'\nRunning DayCent for {sch_file}...')
    if extension:
        subprocess.call(f'{dc_path} -s {sch_file} -n {sch_file} -e {extension}', shell=True)
    else:
        subprocess.call(f'{dc_path} -s {sch_file} -n {sch_file}', shell=True)

    time.sleep(10)
    subprocess.call(f'{dclist_path} {sch_file} {sch_file} outvars.txt', shell=True)


def read_lis(lis_path, head_skip, tail_skip):
    '''
    Read space-delimited .lis output files and convert to a dataframe
    (including skipping headers and
    dummy head or tail data rows).

    Parameters
    ----------
    lis_path : str
        Full path and filename of the output .lis file to be read.
    head_skip : int
        Number of rows to skip at beginning of file, incl. headers and dummy data.
    tail_skip : int
        Numbers of rows to skip at end of file, typically dummy data.
    '''
    # read all lines into a 2D list, delete the list initialization and specified head/tail lines
    input_data = open(lis_path, 'r')
    # Skip head lines and get header
    for i in range(head_skip):
        if i== 0:
            header = next(input_data).split()
        else:
            next(input_data)
    data = np.loadtxt(input_data)[:-tail_skip]
    df = pd.DataFrame(data, columns=header)
    return update_col(df)


#!!! This needs redo, get C_frac based on the type of the crop from the user_data spreadsheet
def convert_yield(crmvst, cgrain, C_frac=0.425):
    #determines if crop is a grain or grass
    #what variable has yield of crop
    crmvstsum = 0
    cgrainsum = 0
    for i in range(len(crmvst)):
        crmvstsum += crmvst[i]
    for i in range(len(cgrain)):
        cgrainsum += cgrain[i]
    if cgrainsum > 0:
        cropyield = (cgrain[:] / C_frac)*(1-.07) # 7% storage loss
        cropyield = cropyield*0.429 #gC/m^2 to bu/ac
    else:
        cropyield = crmvst[:]
    return cropyield


def cleanup_files(workspace_path, folders=()):
    '''Remove the copied files generated during run.'''
    # In the top level of workspace
    for file in os.listdir():
        for suffix in ('.100', '.in', '.sch', '.bin', '.lis', '.csv', '.xlsx', 'xlsm',
                       'weather.wth', 'outvars.txt'):
            if file.endswith(suffix):
                rm(file)

    # In individual folders
    for folder in folders:
        folder_path = join(workspace_path, folder)
        for file in os.listdir(folder_path):
            for suffix in ('.bin', '.lis', '.csv'):
                if (file.endswith(suffix)
                    # and file not in ('TEAValues.csv', 'non-soil.csv')
                    ):
                    rm(join(folder_path, file))


def update_col(df):
    '''Update dataframe column names so it's easier to retrieve data.'''
    # Strip spaces and parenthese
    df = df.rename(columns={i: ''.join(re.split('\(|\)| |/', i))
                            for i in df.columns})
    return df

#!!! Use the column name, not numbers
def update_results(inputs, folder):
    '''Read, organize, and save DayCent results.'''
    header = inputs.columns.levels[1]
    outputs = inputs.copy()
    outputs.columns = header

    # Results from DayCent
    harvest = update_col(pd.read_csv('harvest.csv'))
    year_summary = update_col(pd.read_csv('year_summary.csv'))
    lis_results = read_lis(f'{folder}.lis', head_skip=2, tail_skip=1)
    methane = update_col(pd.read_csv('methane.csv'))

    # Find crop yield, harvested grass/grain, g C/m^2 harvest
    cropyield = convert_yield(harvest.crmvst, harvest.cgrain) #bu/ac
    outputs.Yield = cropyield
    multiplier = m2_per_acre / cropyield # from per acre to per bu

    # Soil organic carbon and CO2 from oxidized CH4,
    # gC/m^2 to g CO2e/m^2
    somtc = lis_results.somtc
    SOC = -(somtc[1:].reset_index(drop=True)-somtc[:-1].values)
    outputs.SOC = SOC * 10000/1000 # gC/m2/yr to kgC/ha/yr

    # Direct N2O
    N2Odirect = year_summary.N2Oflux*NtoN2O*CFs['N2O'] # gN/m2/yr -> g CO2eq/m^2 y
    outputs.N2O_FLUX = N2Odirect * multiplier

    # Indirect N2O from leached and volatilized N, g N2O-N/m^2 to g CO2e /m^2 d
    #!!! Go with Jeff's suggestion for now, but need to double-check
    leached = EFs['leached']*(lis_results.strmac2[1:].reset_index(drop=True)-harvest.strmac2) #!!! maybe don't need the harvest part based on the email?
    NO = EFs['NO']*year_summary.NOflux
    vol = EFs['vol']*lis_results.volpac[1:].reset_index(drop=True)
    N2Oindirect = (leached+NO+vol)*NtoN2O*CFs['N2O']
    outputs.N_leaching = N2Oindirect * multiplier

    #!!! Need to add in this part
    Napp = harvest.fertappN #applied N fertilizer, g N/m2
    Papp = harvest.fertappP #applied P fertilizer, g P/m2

    #formatting methane variables
    methane['year'] = np.floor(methane.time)
    # Daily emission to annual emission
    years = methane.year.unique()
    CH4_prodyear = np.array([methane[methane.year==i].CH4_prod.sum() for i in years])
    CH4_oxyear = np.array([methane[methane.year==i].CH4_oxid.sum() for i in years])
    # Get the CO2-eq CH4, note that the oxidized CH4 does not need to multiply by the methane CF
    CH4flux = (CH4_prodyear-CH4_oxyear)*CtoCH4*CFs['BioCH4'] + CH4_oxyear*CtoCO2
    outputs.CH4_FLUX = CH4flux * multiplier

    outputs.columns = inputs.columns
    return outputs


def run_DayCent_connector():
    '''Execute DayCent-related functions. '''
    # Navigate to workspace
    workspace_path = input("Path to workspace: ")
    # Change the directory now so that if there's a problem with the path,
    # the user will receive the error early
    os.chdir(workspace_path)

    #!!! Maybe should consider extension for different folders as well?
    extend = input("Are you extending a file? (y or n) : ")
    if extend == 'y':
        extension = input('Input file running DayCent extension with. '
                          ' Do not include the .bin extension')
    else:
        extension = ''

    CropType = input('What crop? 1: cornstover, 2: sugarcane, 3: sorghum, 4: other: ')
    CropType = int(CropType)

    folders = []
    first = input('Folder name: ')
    folders = [first]
    addfolder = input('Would you like to add another folder? y or n: ')
    while addfolder == 'y':
        new = input('Folder name: ')
        folders.append(new)
        addfolder = input('Would you like to add another folder? y or n: ')

    cleanup_files(workspace_path, folders)

    input_files= [
        'crop.100',
        'cult.100',
        'fert.100',
        'fix.100',
        'harv.100',
        'irri.100',
        'site.100',
        'tree.100',
        'trem.100',
        'outfiles.in',
        'sitepar.in',
        'soils.in',
        'outvars.txt',
        'weather.wth',
        # 'TEAValues.csv',
        # 'non-soil.csv',
        'user_data.xlsx']

    output_files = [
        'co2.csv',
        'harvest.csv',
        'methane.csv',
        'nflux.csv',
        'potcrp.csv',
        'potfor.csv',
        'potgt.csv',
        'resp.csv',
        'summary.csv',
        'year_summary.csv']
    for folder in folders:
        # Copy needed input files
        folder_path = join(workspace_path, folder)
        for file in [*input_files, f'{folder}.sch']:
            cp(join(folder_path, file), workspace_path)

        # Run DayCent and update results
        run_DayCent(sch_file=folder, extension=extension)

        data_path = join(workspace_path, 'user_data.xlsx')
        data_wb = pd.ExcelFile(data_path)
        inputs = pd.read_excel(data_wb, sheet_name='inputs',
                               header=[0,1,2], index_col=0)
        outputs = update_results(inputs, folder)
        data_wb.close()

        # Save results and move back to the respective folder
        data_writer = pd.ExcelWriter(join(folder_path, 'user_data.xlsx'))
        inputs.to_excel(data_writer, sheet_name='inputs')
        outputs.to_excel(data_writer, sheet_name='outputs')
        data_writer.save()

        for file in [*output_files, f'{folder}.lis', f'{folder}.bin']:
            mv(join(workspace_path, file), folder_path)

        # Remove used files
        for file in [*input_files, f'{folder}.sch']:
            rm(join(workspace_path, file))

    print('\nDayCent run finished, calculating feedstock carbon intensity...')

    for folder in folders:
        # Copy the feedstock carbon intensity calculator (FD-CIC) to the folder and rename
        org_fdcic_path = join(_connector_path, 'FD-CIC_2021_dynamic.xlsm')
        new_fdcic_path = join(folder_path, f'{folder}.xlsm')
        cp(org_fdcic_path, new_fdcic_path)

        # Run FD-CIC
        folder_path = join(workspace_path, folder)
        data_path = join(folder, 'user_data.xlsx')
        run_FDCIC(data_path=data_path, fdcic_path=new_fdcic_path)
        print(f'\nFinished calculating carbon intensity for {folder}')

    print('\nAll runs completed!')