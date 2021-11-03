# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 15:16:48 2021

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
        SOC = np.append(SOC,somtc[count_up] - somtc[count_up+1])
        count_up += 1
    SOC = (SOC/12)*44
    return SOC

def convertCH4(var):
    #converts gC/m^2 to gCH4/m^2 gCO2eq/m^2
    CtoCH4toCO2eq = ((var/12) * (12.011 + 4*(1.008)))*BiogenicCH4CF
    return CtoCH4toCO2eq

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
    else:
        cropyield = crmvst[:]
    return cropyield

def totalCH4(ox, prod):
    #subtracts the produced CH4 by the oxidized CH4 to get net CH4
    CH4new = prod - ox
    return CH4new

def nonsoilcalc(fertapp): 
    '''

    Parameters
    ----------
    fertapp : list
        amount of nitrogen fertilizer applied since previous HARV event

    Returns
    -------
    None.

    '''
    chemop = nonsoil[0] + nonsoil[1]
    emissions = chemop + fertapp*nonsoil[3] + (nonsoil[4]*(nonsoil[5]/10000)*nonsoil[2])
    return emissions

def MESPPrices(var,time, BioPrice = 1.4):
    '''
    converts yield (g corn/m^2 harvest) to prices ($/dryton cornstover)
    then finds the MESP ($/gal)

    Parameters
    ----------
    var : series or list 
        var is the variable containing the yield data (g feedstock/m^2 harvest)
        
    Returns
    -------
    price: list
        list of MESP values per year [$/gal]
    drytonacre: list
        dryton/acre per year
    TotalCost: list
        total cost per year ($/dryton cornstover)

    '''
    outputs = pd.DataFrame()
    outputs['years'] = time
    
    # .5cornstover / corn #(1 ton/ 907185 gram)*(4046.86 m^2 / 1 acre)
    drytonacre = var*.5*(1/907185)*(4046.86/1) # ton cornstover/acre
     # Yalin: I think you should do (i.e., 7% is dry storage loss)
        # temp[index] *= (1-0.15)*(1-0.07)
        #for some reason this ^^ was deleted at some point, do we remember why? 
    replaceharv = (TEAValues[6]/drytonacre) + (TEAValues[17]/drytonacre)
    TotalCost = (TEAValues[6]/drytonacre) + (TEAValues[17]/drytonacre) + TEAValues[19] + TEAValues[21] + TEAValues[23] + TEAValues[8]
    Feedratio = ((TEAValues[6]/drytonacre) + TEAValues[8])/TotalCost 
    Logratio = ((TEAValues[17]/drytonacre) + TEAValues[19] + TEAValues[21] + TEAValues[23])/TotalCost 
    #not currently considering price of lime -> need to 
    price = np.empty((0,0))
    Feed = np.empty((0,0))
    Log = np.empty((0,0))
    Bio = np.empty((0,0))
    for i in range(len(TotalCost)):
        cornstover.price = TotalCost[i] * (1/907.185) # 1 ton is 907.185 kg
        MESP = cornstover_tea.solve_price(ethanol)
        MESP = MESP*cs.ethanol_density_kggal
        price = np.append(price, MESP)
        Feed = np.append(Feed, (MESP - BioPrice)*Feedratio[i])
        Log = np.append(Log, (MESP - BioPrice)*Logratio[i])
        Bio = np.append(Bio, [BioPrice])
    outputs['MESP [$/gal]'] = price
    outputs['Feedstock [$/gal'] = Feed
    outputs['Logistics & Preprocessing [$/gal]'] = Log
    outputs['Biorefinery [$/gal]'] = Bio
    return price, drytonacre, TotalCost, replaceharv, outputs
    
def percornstover(chem_list,cropyield):
    #converts a variable to variable / kg cornstover
    gtokg = chem_list/1000 # g CO2e /m^2 to kg CO2e / m^2
    m2toacre = gtokg * 4046.86 #kg CO2e / m^2 to kg CO2e / acre
    tontokg = cropyield*907.185 #dryton/acre to kg/acre
    perkg= m2toacre /tontokg
    return perkg

def calc_emissions(inputs,time,names):
    #generates emissions (GWP) dataframe
    outputs = pd.DataFrame()
    outputs['years'] = time
    count = 0
    GWP = [1,1,0,0,1,0,0,1,1]
    for i in range(len(inputs)):
        templist = []
        if GWP[i] == 1:
            value = (inputs[i] / ratio)*2.98668849 #convert from per kg ethanol to gal ethanol
            templist = np.append(templist, value)
        else:
              templist = np.append(templist, inputs[i])
        outputs[names[count]] = templist
        count += 1
    return outputs

def add2(source1, source2):
    #adds two lists
    total = source1 + source2
    return total

def valueratio(cropyield, dollarperton, CropPrice = 241.6654953): 
    #cornprice = 241.6654953 #$ per dryton
    cornstovervalue = (cropyield*.5)*dollarperton
    cornvalue = cropyield*CropPrice
    monratio = (cornstovervalue/(cornstovervalue + cornvalue))
    return monratio
    
def calc_emissions_mon(inputs,time,names):
    #generates emissions (GWP) dataframe w monetary ratio
    outputs = pd.DataFrame()
    outputs['years'] = time
    count = 0
    for i in range(len(inputs)):
        templist = np.empty((0,0))
        value = (inputs[i] /ratio)*2.98668849 #convert from per kg ethanol to gal ethanol
        value = value * monetaryratio
        templist = np.append(templist, value)
        outputs[names[count]] = templist
        count += 1
    return outputs

def output():
    df = MESPdf
    df.to_csv(r'%s\MESPdf.csv' % (target_path), index = False, header=True)
    df = emissionsdffeedstock
    df.to_csv(r'%s\FeedstockEmissions.csv' % (target_path), index = False, header=True)
    df = emissionsdfmon
    df.to_csv(r'%s\AllocationEmissions.csv' % (target_path), index = False, header=True)
    df = GWPCornstover
    df.to_csv(r'%s\GWPCornstover.csv' % (target_path), index = False, header=True)

def reset(): 
    for item in folder_list:
        sch_file = item
        totalfiles = ['AllocationEmissions.csv','FeedstockEmissions.csv','MESPdf.csv','GWPCornstover.csv',f'{sch_file}.lis','co2.csv','harvest.csv','methane.csv','nflux.csv',
         'potcrp.csv','potfor.csv','potgt.csv','resp.csv',f'{sch_file}.bin','summary.csv','year_summary.csv','crop.100','cult.100','fert.100','fix.100','harv.100','irri.100',
         'site.100','tree.100','trem.100','outfiles.in','sitepar.in','soils.in','outvars.txt','weather.wth', f'{item}.sch','TEAValues.csv','non-soil.csv']
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
    TEAValues = pd.read_csv('TEAValues.csv')
    nonsoil = pd.read_csv('non-soil.csv')
    
    #from the dataframes, separating important variables
    N2Oflux = np.array(((year_summary.iloc[:,1])/28)*44*N2OCF) #g CO2eq/m^2 y
    NOflux = np.array(year_summary.iloc[:,2]) #g N/m^2 y
    cgrain = np.array(harvest.iloc[:,6])  #g C/m^2 harvest
    crmvst = np.array(harvest.iloc[:,10]) #g C/m^2 harvest
    strmac2harv = np.array(harvest.iloc[:,39]) #g N/m^2 y
    fertapp = np.array(harvest.iloc[:,31])
    CH4_ox = convertCH4(np.array(methane.iloc[:,21])) #g C/m^2 d
    CH4_prod = convertCH4(np.array(methane.iloc[:,18])) #g C/m^2 d
    TEAValues = np.array(TEAValues.iloc[:,CropType]) 
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
    return harvest, year_summary, methane, N2Oflux, NOflux, cgrain, crmvst, strmac2harv, fertapp, lis_results, volpac, strmac2lis, somtc, CH4_ox, CH4_prod, TEAValues, nonsoil
    
def DayCentRun():
    DayCent(dc_path, sch_file, run_id, outvars, dclist_path, extension)
    #runs daycent
    global  harvest, year_summary, methane, N2Oflux, NOflux, cgrain, crmvst, strmac2harv, fertapp, lis_results, volpac, strmac2lis, somtc, CH4_ox, CH4_prod, TEAValues, nonsoil
    harvest, year_summary, methane, N2Oflux, NOflux, cgrain, crmvst, strmac2harv, fertapp, lis_results, volpac, strmac2lis, somtc, CH4_ox, CH4_prod, TEAValues, nonsoil = setupvar() 
    #formatting methane variables
    CH4_oxyear = np.array(daystoyears(CH4_ox)) # g CO2e /m^2 year
    CH4_prodyear = np.array(daystoyears(CH4_prod)) # g CO2e /m^2 year
    CH4 = totalCH4(CH4_oxyear, CH4_prodyear)
    
    #finding N2O from indirect sources and CO2 flux
    N2Oindirect = N2Oindirectcalc() # g N2O-N/m^2 to g CO2e /m^2 d
    SOC = SOCcalc() #gC/m^2 to g CO2e/m^2
    nonsoil = nonsoilcalc(fertapp)
    
    #finding yield variable and converting to price/dryton and dryton/acre
    cyield = cropyield(crmvst,cgrain)
    
    #defining cornstover pieces
    global cornstover, cornstover_tea, ethanol
    cornstover = cs.cornstover
    cornstover_tea = cs.cornstover_tea
    ethanol = cs.ethanol
    
    #generate MESP dataframe
    MESP, dryton_acre, dollarperton, replaceharv, MESPdf = MESPPrices(cyield,np.array(year_summary.iloc[:,0]))
    
    #defining ratio and kg CO2eq / kg cornstover variables for each chemical
    global ratio, monetaryratio
    ratio = ethanol.F_mass / (cornstover.F_mass - cornstover.imass['Water'])
    CO2eq_per_kg_cornstover_from_N2O = percornstover(N2Oflux, dryton_acre)
    CO2eq_per_kg_cornstover_from_N2O_indirect = percornstover(N2Oindirect, dryton_acre)
    CO2eq_per_kg_cornstover_from_N2O_total = add2(CO2eq_per_kg_cornstover_from_N2O, CO2eq_per_kg_cornstover_from_N2O_indirect)
    CO2eq_per_kg_cornstover_from_SOC = percornstover(SOC, dryton_acre)
    CO2eq_per_kg_cornstover_from_CH4_ox = percornstover(CH4_oxyear, dryton_acre)
    CO2eq_per_kg_cornstover_from_SOC_total = add2(CO2eq_per_kg_cornstover_from_SOC,CO2eq_per_kg_cornstover_from_CH4_ox)
    CO2eq_per_kg_cornstover_from_CH4 = percornstover(CH4, dryton_acre)
    CO2eq_per_kg_cornstover_from_nonsoil = percornstover(nonsoil, dryton_acre)
    names1 = ['GWP_Total (kg CO2 eq/gal ethanol)','GWP_N2Ototal (kg CO2 eq/gal ethanol)','N2Oflux (kg CO2 eq/kg feedstock)',
              'N2Oindirect (kg CO2 eq/kg feedstock)', 'GWP_SOCtotal (kg CO2 eq/gal ethanol)', 'SOC (kg CO2 eq/kg feedstock)',
              'CH4_ox (kg CO2 eq/kg feedstock)', 'GWP_CH4 (kg CO2 eq/gal ethanol)', 'GWP_nonsoil (kg CO2 eq/gal ethanol)']
    CO2eq_per_kg_cornstover_total = add2(CO2eq_per_kg_cornstover_from_nonsoil, add2(CO2eq_per_kg_cornstover_from_N2O_total, add2(CO2eq_per_kg_cornstover_from_CH4,CO2eq_per_kg_cornstover_from_SOC_total)))
    inputsfeed = (CO2eq_per_kg_cornstover_total, CO2eq_per_kg_cornstover_from_N2O_total, CO2eq_per_kg_cornstover_from_N2O, CO2eq_per_kg_cornstover_from_N2O_indirect,
                  CO2eq_per_kg_cornstover_from_SOC_total, CO2eq_per_kg_cornstover_from_SOC, CO2eq_per_kg_cornstover_from_CH4_ox, CO2eq_per_kg_cornstover_from_CH4, CO2eq_per_kg_cornstover_from_nonsoil)
    #generate emissions dataframe
    emissionsdffeedstock = calc_emissions(inputsfeed,year_summary.iloc[:,0],names1)
    monetaryratio = valueratio(cyield, dollarperton)
    names2 = ['GWP_Total (kg CO2 eq/gal ethanol)','GWP_N2Ototal (kg CO2 eq/gal ethanol)','GWP_CO2total (kg CO2 eq/gal ethanol)',
              'GWP_CH4 (kg CO2 eq/gal ethanol)', 'GWP_nonsoil (kg CO2 eq/gal ethanol)']
    inputsmon = (CO2eq_per_kg_cornstover_total, CO2eq_per_kg_cornstover_from_N2O_total, CO2eq_per_kg_cornstover_from_SOC_total, CO2eq_per_kg_cornstover_from_CH4, CO2eq_per_kg_cornstover_from_nonsoil)
    emissionsdfmon = calc_emissions_mon(inputsmon,year_summary.iloc[:,0], names2)
    return N2Oindirect, SOC, nonsoil, CH4_oxyear, CH4_prodyear, CH4, cyield, cornstover, cornstover_tea, ethanol, MESP, dryton_acre, dollarperton, replaceharv, MESPdf, ratio, emissionsdffeedstock, monetaryratio, emissionsdfmon
    
def BioSTEAMRun():
    os.chdir(f'{target_path}/BioSTEAMconnectors-main')
    # Additional codes added by Yalin for LCA accounting
    from _lca_cornstover import GWP_CF_stream, GWP_CFs
    
    # All streams that contain LCA-relevant chemicals
    lca_streams = [
        cs.denaturant,
        cs.cellulase,
        cs.sulfuric_acid,
        cs.DAP,
        cs.CSL,
        cs.ammonia,
        cs.FGD_lime,
        cs.caustic,
        cs.emissions,
            ]
    
    # One stream that representing all chemicals
    lca_stream = tmo.Stream('lca_stream')
    lca_stream.mix_from(lca_streams)
    
    # Get the gross results
    def get_GWP():
        cs_processing_GWP = GWP_CFs['Cornstover']/ratio
        material_GWP = (GWP_CF_stream.mass*lca_stream.mass).sum()/ethanol.F_mass
        power_GWP = cs.BT.power_utility.rate*GWP_CFs['Electricity']/ethanol.F_mass
        return cs_processing_GWP, material_GWP, power_GWP
    
    cs_processing_GWP, material_GWP, power_GWP = get_GWP()
    emissions_from_daycent = np.array(emissionsdfmon['GWP_Total (kg CO2 eq/gal ethanol)'])
    # Using a mass allocation factor of 0.5,
    # (based on the assumption that corn:cornstover = 1:1)
    # total_GWP (kg CO2-eq/kg ethanol) can be calculated as:
    #emissions for daycent total GWP
    GWPCornstover = pd.DataFrame()
    GWPCornstover['GWPethanolfromcornstover']= emissions_from_daycent+(2.98668849*(cs_processing_GWP+material_GWP+power_GWP)) #the emissions from daycent was multiplied by .5, why?
    #smaller than 0
    # As a comparison, the cornstover-derived ethanol has a GWP of
    # 0.19 CO2-eq/kg ethanol
    # in GREET 2020
    # GREET (https://greet.es.anl.gov/) is a model developed by ANL (Argonne National Lab)
    # for energy and emission accounting of fuels
    return GWPCornstover
    
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
            f'{item}.sch','TEAValues.csv','non-soil.csv']
    for file in copy:
        shutil.copy(f"{folder_path}/{file}",target_path)
    #start DayCent
    N2Oindirect, SOC, nonsoil, CH4_oxyear, CH4_prodyear, CH4, cyield, cornstover, cornstover_tea, ethanol, MESP, dryton_acre, dollarperton, replaceharv, MESPdf, ratio, emissionsdffeedstock, monetaryratio, emissionsdfmon = DayCentRun()
    #start BioSTEAM
    GWPCornstover = BioSTEAMRun()
    output()
    outputs = ['MESPdf.csv','FeedstockEmissions.csv','AllocationEmissions.csv','GWPCornstover.csv']
    for file in outputs:
        shutil.copy(f"{target_path}/{file}", folder_path)
    totalfiles = ['AllocationEmissions.csv','FeedstockEmissions.csv','MESPdf.csv','GWPCornstover.csv',f'{sch_file}.lis','co2.csv','harvest.csv','methane.csv','nflux.csv',
         'potcrp.csv','potfor.csv','potgt.csv','resp.csv',f'{sch_file}.bin','summary.csv','year_summary.csv']
    for file in totalfiles:
        shutil.copy(f"{target_path}/{file}", folder_path)
        os.remove(f"{target_path}/{file}")
    for file in copy:
        os.remove(f"{target_path}/{file}")