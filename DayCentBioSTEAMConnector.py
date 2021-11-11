# -*- coding: utf-8 -*-
"""
@author: Emily Lin; Yalin Li

TODO/Notes:
    Add in fertilizers - done
    Crop type and fertilizer - done
    No need for .c and .f files as long as .exe files are there - done
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
PtoP2O5 = 141.948/30.974
m2_per_acre = 4046.86
gtolb = 1/454

# Name of the executive files
dc_path = 'DayCent_CABBI.exe' # DayCent
dclist_path = 'list100_DayCent-CABBI.exe' # DayCent list100


# %%

import os, subprocess, time, shutil, re
import numpy as np, pandas as pd

# Functions that used a lot
isfile = os.path.isfile
join = os.path.join
cp = shutil.copy
mv = shutil.move
rm = os.remove


def RunDayCent(sch_file, extension):
    '''
    Runs DayCent with a specific schedule file.

    Parameters
    ----------
    sch_file: str
        Name of schedule file to be used
    extension: str
        whether or not there is an extension file and the extension .bin
    '''
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

def crop_type():
    #!!! I don't know why this is indexing as the 0 and not the 1 column
    #Yield indexes as 4 so then CROP_type should index as 1
    C_frac = np.empty((0,0))
    for i in range(len(user_data.iloc[:,0])):
        crop = user_data.iloc[i,0]
        if crop == 'corn':
            C_frac = np.append(C_frac, 0.429)
        elif crop == 'soybean':
            C_frac = np.append(C_frac, 0.3169)
        else:
            print('crop type not supported')
            C_frac = np.append(C_frac, 0.429)
    return C_frac
    
#!!! This needs redo, get C_frac based on the type of the crop from the processed_data spreadsheet
#default value of 0.429 is for corn
def convert_yield(crmvst, cgrain):
    #determines if crop is a grain or grass
    #what variable has yield of crop
    crmvstsum = 0
    cgrainsum = 0
    for i in range(len(crmvst)):
        crmvstsum += crmvst[i]
    for i in range(len(cgrain)):
        cgrainsum += cgrain[i]
    if cgrainsum > 0:
        C_frac = crop_type()
        cropyield = (cgrain[:])*(1-.07) # 7% storage loss
        cropyield = cropyield*C_frac #gC/m^2 to bu/ac
    else:
        cropyield = crmvst[:]
    return cropyield

def cleanup_files(target_path, folders=()):
    '''Remove the copied files generated during run.'''
    # In the top level of workspace
    for file in os.listdir():
        for suffix in ('.100', '.in', '.sch', '.bin', '.lis', '.csv', '.xlsx',
                       'weather.wth', 'outvars.txt'):
            if file.endswith(suffix):
                rm(file)

    # In individual folders
    for folder in folders:
        folder_path = join(target_path, folder)
        for file in os.listdir(folder_path):
            for suffix in ('.bin', '.lis', '.csv'): #!!! xlsx?
                if (file.endswith(suffix)
                    # and file not in ('TEAValues.csv', 'non-soil.csv')
                    ):
                    rm(join(folder_path, file))


def update_col(df):
    '''Update dataframe column names so it's easier to retrieve data.'''
    # Strip spaces and parenthese
    df = df.rename(columns={i: ''.join(re.split('\(|\)| ', i))
                            for i in df.columns})
    return df

#!!! Use the column name, not numbers
def update_results(user_data, folder):
    '''Read, organize, and save DayCent results.'''
    results = user_data.copy()

    # Results from DayCent
    harvest = update_col(pd.read_csv('harvest.csv'))
    year_summary = update_col(pd.read_csv('year_summary.csv'))
    lis_results = read_lis(f'{folder}.lis', head_skip=2, tail_skip=1)
    methane = update_col(pd.read_csv('methane.csv'))

    # Find crop yield, harvested grass/grain, g C/m^2 harvest
    cropyield = convert_yield(harvest.crmvst, harvest.cgrain) #bu/ac
    results.loc[:,4] = cropyield
    multiplier = m2_per_acre / cropyield # from per acre to per bu

    # Soil organic carbon and CO2 from oxidized CH4,
    # gC/m^2 to g CO2e/m^2
    somtc = lis_results.somtc
    SOC = -(somtc[1:].reset_index(drop=True)-somtc[:-1].values)*CtoCO2
    results.loc[:,16] = SOC * 10000/1000 # gCO2/m2/yr to kgCO2/ha/yr

    # Direct N2O
    N2Odirect = year_summary.N2Oflux*NtoN2O*CFs['N2O'] # gN/m2/yr -> g CO2eq/m^2 y
    results.loc[:,17] = N2Odirect * multiplier

    # Indirect N2O from leached and volatilized N, g N2O-N/m^2 to g CO2e /m^2 d
    #!!! Go with Jeff's suggestion for now, but need to double-check
    leached = EFs['leached']*(lis_results.strmac2[1:].reset_index(drop=True)-harvest.strmac2) #!!! maybe don't need the harvest part based on the email?
    NO = EFs['NO']*year_summary.NOflux
    vol = EFs['vol']*lis_results.volpac[1:].reset_index(drop=True)
    N2Oindirect = (leached+NO+vol)*NtoN2O*CFs['N2O']
    results.loc[:,18] = N2Oindirect * multiplier

    #!!! Need to add in this part
    Napp = harvest.fertappN #applied N fertilizer, g N/m2
    results.loc[:,7] = Napp * m2_per_acre * gtolb
    Papp = harvest.fertappP #applied P fertilizer, g P/m2
    results.loc[:,10] = Papp * PtoP2O5 * m2_per_acre * gtolb

    #formatting methane variables
    methane['year'] = np.floor(methane.time)
    # Daily emission to annual emission
    years = methane.year.unique()
    CH4_prodyear = np.array([methane[methane.year==i].CH4_prod.sum() for i in years])
    CH4_oxyear = np.array([methane[methane.year==i].CH4_oxid.sum() for i in years])
    # Get the CO2-eq CH4, note that the oxidized CH4 does not need to multiply by the methane CF
    CH4flux = (CH4_prodyear-CH4_oxyear)*CtoCH4*CFs['BioCH4'] + CH4_oxyear*CtoCO2
    results.loc[:,19] = CH4flux * multiplier
    return results


# Navigate to workspace
target_path = input("Path to workspace: ")
# Change the directory now so that if there's a problem with the path,
# the user will receive the error early
os.chdir(target_path)


#!!! Maybe should consider extension for different folders as well?
extend = input("Are you extending a file? (y or n) : ")
if extend == 'y':
    extension = input('Input file running DayCent extension with. Do not include .bin')
else:
    extension = ''

folders = []
first = input('Folder name: ')
folders = [first]
addfolder = input('Would you like to add another folder? y or n: ')
while addfolder == 'y':
    new = input('Folder name: ')
    folders.append(new)
    addfolder = input('Would you like to add another folder? y or n: ')

cleanup_files(target_path, folders)

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
    'processed_data.xlsx']

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
    folder_path = join(target_path, folder)
    for file in [*input_files, f'{folder}.sch']:
        cp(join(folder_path, file), target_path)

    # Run DayCent and update results
    RunDayCent(sch_file=folder, extension=extension)

    user_data = pd.read_excel(join(target_path, 'processed_data.xlsx'),
                              header=[0,1,2], index_col=0)
    updated_data = update_results(user_data, folder)

    # Save results and move back to the respective folder
    processed_path = join(target_path, 'processed_data.xlsx')
    updated_data.to_excel(processed_path)
    cp(processed_path, folder_path)

    for file in [*output_files, f'{folder}.lis', f'{folder}.bin']:
        mv(join(target_path, file), folder_path)

    # Remove used files
    for file in [*input_files, f'{folder}.sch']:
        rm(join(target_path, file))

print('\nRun finished.')