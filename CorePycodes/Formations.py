import os
import pandas as pd
import json

Root_path = os.path.dirname(os.getcwd())
search_dir=os.path.join(Root_path + '/CoreData/CoreXRF/')

Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))


def find_csv_filenames( search_dir, suffix=".csv" ):
    filenames = os.listdir(search_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


Q=(find_csv_filenames(search_dir))


#These two for loops add formations to the .json file based on what it finds in the XRF folder
B=[]
A=[]
for i in range(len(Q)):
    XRF_file=os.path.join(search_dir + Q[i])
    csv_file = pd.read_csv(open(XRF_file, "r"), delimiter=",")
    A.append(os.path.splitext(Q[i])[0])
    B.append(csv_file['Formation'].unique().tolist())

for i in range(len(A)):
    Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  (A[i]).split('_')[0]  +'.json')))
    Corebeta['Formations'] = B[i]
   
    with open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  (A[i]).split('_')[0]  + '.json'), 'w') as f:    json.dump(Corebeta, f)  

