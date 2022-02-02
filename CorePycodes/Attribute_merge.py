import os
import pandas as pd
import json
import corepytools as corepy


# Attribute_merge.py is run after PCAexample and NN_Model_apply.py
# File dependencies: 1) input file _XRF.csv data file in folder //CorePy/CoreOutput/CoreName/<Formation>
# File dependencies: 2) input attribute files in //CorePy/CoreData/CoreAttributes/<core name>
# Output: adds attribute csv files in //CorePy/CoreOutput/CoreName/<Formation>

# Root_path, Run_settings, and Corebeta and the two .json core settings files with all input parameters
Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names is Run_settings["Formation"]
Formation_names=corepy.Formation_names(Run_settings["Formation"],Run_settings["Formation_2"])
# RootDir(corename, Formation_names) established the output folder structure
dirName=corepy.RootDir(Corebeta["corename"], Formation_names) 

# Searches for all csv files in attribute folder. The attribute data have to be depth references (core, box, inch) to match
Attribute_dir = os.path.join(Root_path + '/CoreData/CoreAttributes/'   +  Run_settings['CoreOfStudy'])
all_files = os.listdir(Attribute_dir)    
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))

# Get the path directory for the XRF file name

XRF = corepy.OutputXRF(Run_settings["CoreOfStudy"],Formation_names)
Merged_file=XRF

# Loop over the attribute files and merge on Core-Box-Inch
for i in range(len(csv_files)):
    
    Att_file = pd.read_csv(os.path.join(Attribute_dir + '/' + csv_files[i]))
    # Merging adds duplicate file names so I use these two lines to remove duplicate names
    Merged_file = pd.merge(Merged_file, Att_file, how='left', on=['Core', 'Box', 'Inch'],suffixes=('', '_drop'))  
    Merged_file.drop([col for col in Merged_file.columns if 'drop' in col], axis=1, inplace=True)


Merged_file.to_csv (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Attribute.csv'))