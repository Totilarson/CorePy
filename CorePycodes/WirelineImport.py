import os
import lasio
import corepytools as corepy
import json
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

#import pickle
#import seaborn as sns

#infile = open('chemocolor','rb')
#chemofacies_color= pickle.load(infile)
#infile.close()  

# WirelineImport.py imports .las files using lasio
# Coredata has to be depth corrected with data in coredata['Wireline_Depth']
# output: writes to corebeta.json files the logs available
# output: writes a .csv file _LAS that is the original data in .las file
# output: writes a .csv file _WirelineLog.csv that includes selected logs recalculated for xrf data point depth
# wireline logs selected for export are identified in corebeta.json['WirelineLogs_NeuralModel']

# Root_path, Run_settings, and Corebeta and the two .json core settings files with all input parameters
Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names is Run_settings["Formation"]
Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

coredata = corepy.OutputXRF(Run_settings['CoreOfStudy'],Formation_names) # This directs to the output file

# RootDir(corename, Formation_names) established the output folder structure
dirName=corepy.RootDir(Run_settings['CoreOfStudy'], Formation_names) 

# Corebeta['API']  has to match .las file name in Coredata/WirelineLogs/
API= Corebeta['API']
file_path=os.path.join(Root_path + '/CoreData/WirelineLogs/' + str(API) + '.las')
las = lasio.read(file_path)

# Lasio is used to import .las files and write a _LAS csv file
wirelinedata=las.df()
wirelinedata=wirelinedata.reset_index() # set up so that the first column is renamed 'DEPT' to keep it simple moving forward
wirelinedata.rename(columns={ wirelinedata.columns[0]: "DEPT" }, inplace= True)
wirelinedata.to_csv (os.path.join(dirName   + '/' +  Run_settings['CoreOfStudy'] +  '_LAS.csv'))


### Append Lasio Keys to Corebeta json dictionary to identify all available wireline logs
Corebeta['WirelineLogs'] = las.keys()
with open(os.path.join(Root_path + '/CoreData/CoreBeta/'   + Run_settings['CoreOfStudy']  + '.json'), 'w') as f:    
    json.dump(Corebeta, f)  


# This section calculates wireline log values at the depth of each XRF analysis point
# 1D interpolation is applied
df=pd.DataFrame(coredata['Wireline_Depth'])

for i in range (0,len(Corebeta['WirelineLogs_NeuralModel'])):
    x=wirelinedata['DEPT']  # original wireline log depth is always called DEPT
    y=wirelinedata[Corebeta['WirelineLogs_NeuralModel'][i]] # wireline log attribute being cycled over

    f = interp1d(x,y, bounds_error=False, fill_value=-10, kind='linear')

    new_data = np.array([coredata['Wireline_Depth'] , f(coredata['Wireline_Depth'] )])
    new_data=np.transpose(new_data)
    
    df[Corebeta['WirelineLogs_NeuralModel'][i]] =  new_data[:, [1]]

CoreWirelinedata = (pd.merge(coredata, df, on='Wireline_Depth')) # merge orriginal coredata XRF file with new wireline log values

CoreWirelinedata.to_csv (os.path.join(dirName + '/' +  Run_settings['CoreOfStudy'] + '_' + Formation_names + '_WirelineLog.csv'))
