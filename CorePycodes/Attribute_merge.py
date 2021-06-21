#merge tables closest value
import pandas as pd
import os
import json
import corepytools as corepy


CoreOfStudy = 'CincoSaus'

Root_path = os.path.dirname(os.getcwd())
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  CoreOfStudy + '.json')))

Formation_names = '-'.join(Corebeta["Formation"]+Corebeta["Formation_2"]) # Would like to have Formation_names defined in Corebeta

XRF_data = corepy.OutputXRF(Corebeta['corename'],Formation_names) # This directs to the output file

Attribute_dir = os.path.join(Root_path + '/CoreData/CoreAttributes/' + CoreOfStudy +'/') 

Combined_file=XRF_data
lst=[]
for i in range(len(os.listdir(Attribute_dir))):
    
    File_merge= os.path.join(Attribute_dir + os.listdir(Attribute_dir)[i]) #grabs the files in the Attribute folder _XRD, _TOC...
    File_merge=pd.read_csv(File_merge)
    Q=(list(set(list(File_merge))-set(list(XRF_data)))) # finds the column headings that are different and turns into a list
    File_merge = pd.merge(Combined_file, File_merge, how='left', on=['Core','Box', 'Inch'])
    
    Combined_file=File_merge # allows it to loop through and add to XRF_data dataframe
    
    lst.extend([Q]) # appends the list made of column headings

AttributeHeadings=[]
for i in range(len(lst)):    
    #df=pd.DataFrame(lst)
    AttributeHeadings= AttributeHeadings+lst[i]



Corebeta['AttributeHeadings'] = AttributeHeadings
with open(os.path.join(Root_path + '/CoreData/CoreBeta/'   + Corebeta["corename"]  + '.json'), 'w') as f:    
    json.dump(Corebeta, f)  

dirName=corepy.RootDir(Corebeta["corename"], Formation_names) 

Combined_file=File_merge.loc[:,~Combined_file.columns.str.contains('_y')]

#Combined_file.columns = Combined_file.columns.str.rstrip('_x')  # strip suffix at the right end only.
#Combined_file.columns = Combined_file.columns.str.strip('_x')


Combined_file.to_csv (os.path.join(dirName + '/' +  CoreOfStudy + '_' + Formation_names + '_Attribute.csv'))

    #df[Corebeta['WirelineLogs'][i]] =  new_data[:, [1]]
    