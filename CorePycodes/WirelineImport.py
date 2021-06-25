import os
import lasio
import corepytools as corepy
import json
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd



Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

coredata = corepy.OutputXRF(Run_settings['CoreOfStudy'],Formation_names) # This directs to the output file
dirName=corepy.RootDir(Run_settings['CoreOfStudy'], Formation_names) 

API= Corebeta['API'] # might be an issue with API not being in quotes as it would be if written  API='42303347740000'
file_path=os.path.join(Root_path + '/CoreData/WirelineLogs/' + str(API) + '.las')
las = lasio.read(file_path)

wirelinedata=las.df()
wirelinedata=wirelinedata.reset_index() # set up so that the first column is renamed 'DEPT' to keep it simple moving forward
wirelinedata.rename(columns={ wirelinedata.columns[0]: "DEPT" }, inplace= True)
wirelinedata.to_csv (os.path.join(dirName   + '/' +  Run_settings['CoreOfStudy'] +  '_LAS.csv'))


### Append Lasio Keys to Corebeta json dictionary

Corebeta['WirelineLogs'] = las.keys()

with open(os.path.join(Root_path + '/CoreData/CoreBeta/'   + Run_settings['CoreOfStudy']  + '.json'), 'w') as f:    
    json.dump(Corebeta, f)  

df=pd.DataFrame(coredata['Wireline_Depth'])

for i in range (1,len(Corebeta['WirelineLogs'])):
    x=wirelinedata['DEPT']  # original wireline log depth is always called DEPT
    y=wirelinedata[Corebeta['WirelineLogs'][i]] # wireline log attribute being cycled over

    f = interp1d(x,y, bounds_error=False, fill_value=-10, kind='linear')

    new_data = np.array([coredata['Wireline_Depth'] , f(coredata['Wireline_Depth'] )])
    new_data=np.transpose(new_data)
    
    df[Corebeta['WirelineLogs'][i]] =  new_data[:, [1]]

Final = (pd.merge(coredata, df, on='Wireline_Depth')) # merge orriginal coredata XRF file with new wireline log values

Final.to_csv (os.path.join(dirName + '/' +  Run_settings['CoreOfStudy'] + '_' + Formation_names + '_WirelineLog.csv'))