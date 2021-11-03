# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 20:58:35 2021

@author: Empli
"""
#import necessary packages
import os
import subprocess
import time
import pandas as pd
import matplotlib
import math
import shutil
import numpy as np
matplotlib.use('Agg')
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.style
matplotlib.style.use('classic')
import thermosteam as tmo
from biorefineries import cornstover as cs

N2OCF = 265
BiogenicCH4CF = 28

def DayCent (dc_path, sch_file, run_id, outvars, dclist_path="", extension =""):
    '''
    Runs DayCent for a specific schedule file
    Parameters
    ----------
    dc_path: str
        Name of DayCent version
    sch_file: str
        Name of schedule file to be used
    run_id: str
        What you want the .bin or .lis file to be called
    outvars: str
        Name of file with outputs
    dclist_path: str
        Name of DayCent list100 file
    extension: str
        whether or not this is an extension file and the extension .bin
    '''
    os.chdir(target_path)
    if extension:
        # Yalin: with Python 3, you can use the f-string to improve the readability
        # subprocess.call(f'{dc_path} -s {sch_file} -n {run_id} -e {extension}', shell=True)
        subprocess.call(f'{dc_path} -s {sch_file} -n {run_id} -e {extension}', shell = True)
    else:
        subprocess.call(f'{dc_path} -s {sch_file} -n {run_id}', shell = True)
        time.sleep(10)
    if dclist_path:
       subprocess.call(f'{dclist_path} {run_id} {run_id} {outvars}', shell = True)

def auto_type(datum): # Yalin: I'm amazed to see the singular form of data
    #Convert data types to integer or float if possible
    try:
        return int(datum)
    except:
        try:
            return float(datum)
        except:
            return str(datum)

def read_full_out(out_fpath, head_skip, tail_skip):
    '''
    Yalin: always great to have documentation for modules!
    They should be placed rightly after the `def` line.

    I tried for format your notes into the numpydoc style
    (there are several widely used ones, BioSTEAM uses numpydoc),
    check here [1]_ for more guidance.

    Reads space-delimited .lis output files (including skipping headers and
    dummy head or tail data rows), and returns averages of entire columns or averages of
    annual differences within a column.

    Parameters
    ----------
    out_fpath : str
        Full path and filename of output file to be analyzed.
    head_skip : int
        Number of rows to skip at beginning of file, incl. headers and dummy data.
    tail_skip : int
        Numbers of rows to skip at end of file, typically dummy data.

    .. note:
        You obviously don't need my comment and the numpy docstring in the
        documentation here, I was just trying to give you an example of hyperlink
        (and note).

    Note
    ----
    Another way to add note (can be rendered by both IDE and Sphinx).

    See Also
    --------
    .. [1] `numpydoc style <https://numpydoc.readthedocs.io/en/latest/format.html>`_
    '''

    #Reads space-delimited .lis output files (including skipping headers and
    # dummy head or tail data rows), and returns averages of entire columns or averages of
    #  annual differences within a column.
    # Arguements:
        #out_fpath- full path and filename of output file to be analyzed (str)
        #head_skip- number of rows to skip at beginning of file, incl. headers and dummy data (int)
        # tail_skip- numbers of rows to skip at end of file, typically dummy data (int)
    # read all lines into a 2D list, delete the list initialization and specified head/tail lines
    input_data = open(out_fpath, 'rU')
    mylist = [[]]
    for i in range(head_skip):
        next(input_data)
    # Yalin: Are you trying to split each line in `input_data` into a list?
    # would `input_data.splitlines()` do it?
    for line in input_data:
        mylist.append(line.split())
    del mylist[0]
    # Yalin: what about `del mylist[-j:]`?
    for j in range(tail_skip):
        del mylist[-1]

    # convert each list entry float format if possible, or zero in case of small numbers in scientific notation
    # What str would be in the input?
    # numpy can automatically convert scientific expressions to float
    # import numpy as np
    # mylist_ar = np.array(mylist, dtype=float)
    for k in range(len(mylist)):
        for l in range(len(mylist[k])):
            mylist[k][l] = auto_type(mylist[k][l])
    return mylist

def pull_variable(index, results):
    #seperates the desired vairables from the results
    #index is the the index of the variable you are trying to pull
    #place the volpac strmax(2) and somtc in order at the end of your outfiles
    #otherwise manually set the index numbers at volpac_index, strmac2_index, and somtc_index
    #results is your results list, most likely lis_results
    count_down = len(results)-1
    count_up = 0
    variable = np.empty((0,0))
    while count_down >= 0:
        variable = np.append(variable, results[count_up][index])
        count_up = count_up + 1
        count_down = count_down - 1
    return variable

def N2Oindirectcalc():
    # g N2O-N/m^2 converted to N2O then CO2e
    #finds indirect N2O emissions
    N2Oindirect = (((0.025*(strmac2lis - strmac2harv) + (0.01*(NOflux + volpac)))/28)*44)*N2OCF #CO2/m^2
    return N2Oindirect


def SOCcalc():
    #finds each CO2flux per year and adds them for a total CO2 flux
    #gC/m^2 converted to gCO2/m^2
    count_up = 0
    SOC = np.empty((0,0))
    for index in range(len(somtc)-1):
        SOC = np.append(SOC,somtc[count_up] - somtc[count_up+1]) + (CH4_oxyear[count_up]/12*44)
        count_up += 1
    SOC = (SOC/12)*44
    return SOC

# Yalin: I didn't understand the function, what is 2000 doing?
# I found that you could use `calender` (built-in module) to check leap year
# import calendar
# calendar.isleap(1900)
def daystoyears(var):
    #converts daily methane values to yearly methane values
    count_up = 0
    days = methane.iloc[:,0]
    years = list()
    for i in range(0, (math.ceil(days[len(days)-1]-2000)-(math.floor(days[0]) - 2000))):
        years.append(0)
    for index in range(len(var)):
         start = math.floor(days[0]) - 2000
         count_down_years = (math.ceil(days[len(days)-1]-2000)) + start
         count_up_years = start
         while count_down_years >= 0:
             if (count_up_years + 2000) <= days[count_up] < (count_up_years + 2001):
                 years[(count_up_years - start)] = years[(count_up_years - start)] + var[count_up]
             count_down_years -= 1
             count_up_years += 1
         count_up += 1
    return years

def cropyield(crmvst,cgrain, C_frac = 0.425):
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

def totalCH4(ox, prod):
    #subtracts the produced CH4 by the oxidized CH4 to get net CH4
    CH4new = (prod - ox)/12*16*BiogenicCH4CF
    return CH4new
    
def convert(item):
    #converts a variable to variable / kg cornstover
    #need to convert from gCO2/m^2 to gCO2e/bu
    m2toacre = item*4047 #gCO2eq/acre 4047 m^2=1 acre
    acre = m2toacre/cyield #gCO2/ac
    return acre

def add2(source1, source2):
    #adds two lists
    total = source1 + source2
    return total

def output(file):
    df= file
    df.loc[:,4] = cyield
    df.loc[:,16] = SOC
    df.loc[:,17] = N2Oflux
    df.loc[:,18] = N2Oindirect
    df.loc[:,19] = CH4
    return df
    
    df = Transformed
    df.to_csv(r'%s\TransformedVariables.csv' % (target_path), index = False, header=True)

def reset(): 
    for item in folder_list:
        sch_file = item
        totalfiles = ['AllocationEmissions.csv','FeedstockEmissions.csv','MESPdf.csv','GWPCornstover.csv',f'{sch_file}.lis','co2.csv','harvest.csv','methane.csv','nflux.csv',
         'potcrp.csv','potfor.csv','potgt.csv','resp.csv',f'{sch_file}.bin','summary.csv','year_summary.csv','crop.100','cult.100','fert.100','fix.100','harv.100','irri.100',
         'site.100','tree.100','trem.100','outfiles.in','sitepar.in','soils.in','outvars.txt','weather.wth', f'{item}.sch','TEAValues.csv','non-soil.csv','processed_data.xlsx']
        for file in totalfiles:
            indicate = os.path.isfile(f'{target_path}/{file}')  
            if indicate == True:
                os.remove(f'{target_path}/{file}')
        FileList = ['AllocationEmissions.csv','FeedstockEmissions.csv','MESPdf.csv','GWPCornstover.csv', f'{sch_file}.lis','co2.csv','harvest.csv','methane.csv','nflux.csv','potcrp.csv','potfor.csv','potgt.csv',
                'resp.csv',f'{sch_file}.bin','summary.csv','year_summary.csv','bio.csv','soiln.csv','soiltavg.csv','soiltmax.csv','soiltmin.csv','stemp_dx.csv','vswc.csv','watrbal.csv','wfps.csv','wflux.csv',
                'livec.csv','deadc.csv','soilc.csv','sycs.csv','tgmonth.csv','dN2lyr.csv','dN2Olyr.csv','dels.csv','dc_sip.csv','harvestgt.csv','cflows.csv','year_cflows.csv','daily.csv','psyn.csv']
        for i in FileList:
            indicate = os.path.isfile(f'{target_path}/{item}/{i}')  
            if indicate == True:
                os.remove(f'{target_path}/{item}/{i}')
                
def setupvar():
    #from target path, takes methane.csv, year_summary.csv, and harvest.csv
    #to be used in the module
    os.chdir(target_path)
    harvest = pd.read_csv('harvest.csv')
    year_summary = pd.read_csv('year_summary.csv')
    methane = pd.read_csv('methane.csv')
    nonsoil = pd.read_csv('non-soil.csv')
    filein = pd.read_excel(f'{target_path}/processed_data.xlsx',header=[0,1,2], index_col=0)
    
    #from the dataframes, separating important variables
    N2Oflux = np.array(((year_summary.iloc[:,1])/28)*44*N2OCF) #g CO2eq/m^2 y
    NOflux = np.array(year_summary.iloc[:,2]) #g N/m^2 y
    cgrain = np.array(harvest.iloc[:,6])  #g C/m^2 harvest
    crmvst = np.array(harvest.iloc[:,10]) #g C/m^2 harvest
    strmac2harv = np.array(harvest.iloc[:,39]) #g N/m^2 y
    fertapp = np.array(harvest.iloc[:,31])
    CH4_ox = np.array(methane.iloc[:,21])#g C/m^2 d
    CH4_prod = np.array(methane.iloc[:,18]) #g C/m^2 d
    nonsoil = np.array(nonsoil.iloc[:,CropType]) 
    lis_fpath = f"{item}.lis"
    
    #reading .lis file, reading the data, separating and formatting variables
    lis_results = read_full_out(lis_fpath, 2, 1)
    shape = len(lis_results[0])
    volpac_index = shape - 3 #g N/m^2 y
    strmac2lis_index = shape - 2 #g N/m^2 y
    somtc_index = shape - 1 #g N/m^2 y
    volpac = pull_variable(volpac_index, lis_results)
    volpac = np.delete(volpac,0)
    strmac2lis = pull_variable(strmac2lis_index, lis_results)
    strmac2lis = np.delete(strmac2lis,0)
    somtc = pull_variable(somtc_index, lis_results)
    return harvest, year_summary, methane, N2Oflux, NOflux, cgrain, crmvst, strmac2harv, fertapp, lis_results, volpac, strmac2lis, somtc, CH4_ox, CH4_prod, nonsoil, filein
    
def DayCentRun():
    DayCent(dc_path, sch_file, run_id, outvars, dclist_path, extension)
    #runs daycent
    global  harvest, year_summary, methane, N2Oflux, NOflux, cgrain, crmvst, strmac2harv, fertapp, lis_results, volpac, strmac2lis, somtc, CH4_ox, CH4_prod, nonsoil, filein, CH4_oxyear
    harvest, year_summary, methane, N2Oflux, NOflux, cgrain, crmvst, strmac2harv, fertapp, lis_results, volpac, strmac2lis, somtc, CH4_ox, CH4_prod, nonsoil, filein = setupvar() 
    #formatting methane variables
    CH4_oxyear = np.array(daystoyears(CH4_ox)) # g C /m^2 year
    CH4_prodyear = (np.array(daystoyears(CH4_prod))) # g C /m^2 year
    CH4 = totalCH4(CH4_oxyear, CH4_prodyear)
    
    #finding N2O from indirect sources and CO2 flux
    N2Oindirect = N2Oindirectcalc() # g N2O-N/m^2 to g CO2e /m^2 d
    SOC = SOCcalc() #gC/m^2 to g CO2e/m^2
    
    #finding yield variable 
    cyield = cropyield(crmvst,cgrain) #bu/ac

   
    return N2Oindirect, SOC, CH4_oxyear, CH4_prodyear, CH4, cyield, filein
    
#defines paths to workspace
target_path = input("Path to workspace:") # Yalin: Maybe add ": " at the end (i.e., "Path to workspace: ")
dc_path = "DayCent_CABBI.exe"
#sch_file = input("Input schedule file name (w/o .sch):")
dclist_path = "list100_DayCent-CABBI.exe"
extend = input("Are you extending a file? y or n:")
if extend == 'y':
    extension = input('File running DayCent extension with. Do not include .bin')
else:
    extension = ""

CropType = input('What crop? 1: cornstover, 2: sugarcane, 3: sorghum, 4: other:')
CropType = int(CropType)
folder_list = []
first = input('First folder name:')
folder_list.append(first)
addfolder = input('Would you like to add another folder? y or n:')
while addfolder == 'y':
    new = input('New folder name:')
    folder_list.append(new)
    addfolder = input('Would you like to add another folder? y or n:')

reset()

for item in folder_list:
    folder_path = f'{target_path}/{item}'
    sch_file = item
    run_id = sch_file[:]
    outvars = "outvars.txt"
    copy = ['crop.100','cult.100','fert.100','fix.100','harv.100','irri.100','site.100','tree.100','trem.100','outfiles.in','sitepar.in','soils.in','outvars.txt','weather.wth',
            f'{item}.sch','processed_data.xlsx','TEAValues.csv','non-soil.csv','processed_data.xlsx']
    for file in copy:
        shutil.copy(f"{folder_path}/{file}",target_path)
    #start DayCent
    N2Oindirect, SOC, CH4_oxyear, CH4_prodyear, CH4, cyield, filein = DayCentRun()
    
    chem_list = [N2Oflux, N2Oindirect, CH4]
    for item in chem_list:
        item = convert(item)
        
    df = output(filein)
    
    df.to_excel(f'{target_path}/processed_data.xlsx')
    
   
    outputs = ['processed_data.xlsx']
    for file in outputs:
        shutil.copy(f"{target_path}/{file}", folder_path)
    files = [f'{sch_file}.lis','co2.csv','harvest.csv','methane.csv','nflux.csv',
         'potcrp.csv','potfor.csv','potgt.csv','resp.csv',f'{sch_file}.bin','summary.csv','year_summary.csv']
    for file in files:
        shutil.copy(f"{target_path}/{file}", folder_path)
        os.remove(f"{target_path}/{file}")
    for file in copy:
        indicate = os.path.isfile(f'{target_path}/{file}')  
        if indicate == True:
            os.remove(f'{target_path}/{file}')