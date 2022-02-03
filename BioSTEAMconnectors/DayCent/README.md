# BioSTEAMConnectors Manual

## Introduction to the Module

BioSTEAMconnectors (available at GitHub) is written in Python 3.7 and automates the execution of DayCent and the extraction of the applicable parameters. DayCent can be used to evaluate how factors including soil properties (e.g., pH), weather (e.g., precipitation), crop management practices (e.g., irrigation, fertilization), and dynamic soil biogeochemistry (e.g., mineral nitrogen availability) impact emission of certain chemicals and crop yield. The simulated parameters from the DayCent run are then put into a feedstock calculator from CBI which finds the associated emissions. 

There are four main files used to run BioSTEAMconnectors. *`DaycentRUNME.py`* imports run_DayCentConnector from the *`DayCent.py`* file and runs the module. *``__init__.py``* imports `._fdcic` and `._daycent` to initiate the files. *`._daycent.py`* automates the execution of DayCent and exports the results into an excel sheet which will then run the feedstock calculator. At the beginning of the code, there are settings that can be updated to represent the needs of the user. `Clean_files` removes *`.csv`*, *`.bin`*, and *`.lis`* files from previous runs so that a new occurrence can run smoothly. Once cleaned, the run_DayCent function executes DayCent and list100 for the specific schedule file, input files, and an optional extension file provided by the users. Executing `DayCent` will output the desired *`.csv`* files and the *`.lis`* files. The *`.lis`* files can then be used in `read_full_out` to extract the data from the DayCent output files and create a data frame. `Update_col` takes the data from the DayCent run and transforms the variables into data usable for the feedstock calculator. This data includes the yield, SOC, N2Oflux, N2O direct, N leaching, CH4 flux, and N and P fertilizers. These variables are then used to update the excel spreadsheet. *`._fdcic.py`* is then run to transfer DayCent results from *`user_data.xlsx`* and into *`FD-CIC_2021_dynamic.xlsm`* which will execute the macro and calculate the associated emissions. The results will aggregate in the *`<site name>.xlsm`* file.

**![](https://lh4.googleusercontent.com/ChSsCIpPgkJb72tequl8rRpFmoV2LzV9QKIIP1xn0yiCikmYaw8S8WYfhq634cy-UndAx6G_efCislhwFs90VSesPv0xcdybMaIEPS3oHm-CCf0AKf9fUwFODFlvhVMcUyPd4K94)**

**

Figure 1. DayCent configuration

**



## Supported Versions and Devices

DayCent can only be run by Windows devices, causing DayCent and this module to be inaccessible to Apple computers. This module will not produce outputs if run on Apple devices.



## Configuration of Workspace

The module workspace must be configured in order to run properly.

**![](https://lh3.googleusercontent.com/OgO2m97_P1BozN6PwXUBEKtEghxQZsW2rTNDpYho3RFNRVGDDXBaOzK46RA_LM0buK814TxdFqRL0mhfAeRXJl1XjC76p0JUI1i6TBsrjZg9oOkpjeiYUoeBa-c7xNpIL7inTzEJ)**

**

Figure 2. Organization of workspace

**

The CABBI version of DayCent can be downloaded from Github at https://github.com/cabbi-bio/DayCent-CABBI by clicking the `code` button and downloading the *`.ZIP`* file. Once the GitHub file is downloaded, create a workspace folder. For this example, the workspace folder will be called `FakeCities` and will be located in my downloads folder. 

Locate the CABBI DayCent code, the name of the *`.ZIP`* file downloaded is `DayCent-CABBI-master`, and copy over *`DayCent_CABBI.exe`* and *`List100_DayCent-CABBI.exe`* to the workspace folder. The rest of the `DayCent-CABBI-master` folder is not needed.

The python module must then be downloaded. Go to [GitHub - emilypl2/BioSTEAMconnectors: DayCent BioSTEAM connector](https://github.com/emilypl2/BioSTEAMconnectors) and download the code by going to the `code`  button and downloading the *`.ZIP`* file similar to what was done for the CABBI DayCent. Once the file is downloaded, unzip the folder. Remove the *`user_data.xlsx`* from the folder and place a copy in each of the site folders. The results are dependent on each site and therefore must have different *`user_data.xlsx`* sheets. 

Configure your site data into the DayCent acceptable input. Ensure to check the outvars.txt and outfiles.in include all of the files you would like Daycent to generate. While BioSTEAMConnectors supports all of DayCent’s outputs, specific files do need to be turned on to provide the necessary variables to the feedstock calculator. *`harvest.csv`*, and *`methane.csv`* must be set to `1`. In *`outvars.txt`*, `somtc`, `strmac(2)`, and `volpac` must be listed as outputs. List or set these outputs to `1` so that the analysis can run. 

Create a folder for each site. The names of the example sites on the diagram are `site1`, `site2`, through `siteN`. In each of these site folders, put in the relevant *`.100`*, *`.in`*, *`.txt`*, *`.sch`*, and *`.wth`*  (Figure 2). Some of the *`.100`* files are not necessary, so you do not have to have the same *`.100`* files shown (Figure 2) or as previous runs. Change the name of the site file so that it matches the folder name. For instance, if the folder name was `Hogwarts` the schedule name would be *`Hogwarts.sch`*. 

Check that you have all of the files necessary in your site folders and that DayCent and list100 are visible in your workspace.



## Formatting User_data.xlsx

There are three columns that must be updated in the *`user_data.xlsx`* file. First, the `CROP_type` column (E) should represent the type of crop that is going to be modeled. The example uses a yearly rotation of corn and soybean so the *`user_data.xlsx`* shows this. The `tillage_intensity` (F) can then be set. The options are `CT` for conventional tillage, `NT` for no-tillage, and `RT` for reduced tillage. The final column to be updated is `cover_crop` (G) where the options are `R` for ryegrass, `H` for hairy vetch, `RH` for both ryegrass and hairy vetch. Complete the inputs for the three columns equal to the number of years to be modeled. If there are 21 years of data, the *`user_data.xlsx`* columns for `CROP_type`, `tillage_intensity`, and `cover_crop` should be filled through year 21.

**![](https://lh5.googleusercontent.com/dTa1-j1SdXgkSp_LShBhxmyGcodkTdQvndDBXA5g5B1CekuMPAtyT-1ij-nyexW_D4_ezTos_ydfXrS-ANNRcRLgRS-CIXqQIUIsENhjbJVSIPF1QTNM2OsJpnK7Cv8tHFIqyQ6Z)**

**

Figure 3. Example *`user_data.xlsx`* input

**



## Running BioSTEAMConnectors

Enter the *`DayCent_RUNME.py`* file and press run. The model will ask for the path to your workspace first. For the example, the path is `Downloads\FakeCities`. This path can be found in your computer’s folder system. 

It will then ask if you are extending a file, DayCent is able to save the state of a model in a binary file which can later be used to initialize subsequent DayCent runs, allowing DayCent to be run in stages; this is called “extending” from the existing binary file. The two options for this model are `y` if you would like to extend a file or `n`. For the example, no we do not want to run an extension so the answer is `n`. 

BioSTEAMConnectors will then ask for your first site folder name. This is `Hogwarts` for the working example. It will then ask if you would like to add another site. You may be running any number of sites and may continue adding folders until all the sites have been added. Type `y` if you have another site folder that has not been added yet or `n` if they have all been added. For the example, we would write, `Hogwarts`, `y`, `Metropolis`, `y`, `GothamCity`, `n` to add all three folders. 

BioSTEAMConnectors will then run DayCent and complete the analysis. The analysis is finished when the system prints `All runs completed!`. 

An example of the console:

```
Path to workspace: Downloads\FakeCities

Are you extending a file? (y or n) : n

Folder name: Hogwarts

Would you like to add another folder? y or n: n

Running DayCent for Hogwarts...

DayCent run finished, calculating feedstock carbon intensity...

Finished calculating carbon intensity for Hogwarts

All runs completed!
```



## BioSTEAMConnectors Outputs

The results of the module can be found in the file *`<site name>.xlsm`*. The results from DayCent can be found on the left side of the divider in columns H through U. The macro then calculates the emissions in columns W through AE. These emissions are in GHG per bu and GHG per MJ, then broken down into emissions due to energy, nitrogen fertilizer, N2O, CO2 and CH4, SOC, and other chemicals.




