import json
#import seaborn as sns
import os
#import corepytools as corepy

Corebeta = {

"corename" : 'PGEBrowne', #core name being studied
"Photo_depth" : 'Depth_calculated' ,
"corenameAbrev" : 'LA', # two letter abbreviation for subsequent core tube names
"County" : "Webb",
"API": 42479407170000, 
"coretube_length" : 2,      # length of each coretube 
'XRF_resolution' : 2/12,    # used to build chemofacies stacking pattern. 2/12 refers to 2" xrf scanning resolution

# For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
 # this is used to make the directory specific to the formations

}


#corepy.RootDir(Corebeta["corename"], Formation_names)

Root_path = os.path.dirname(os.getcwd())

with open(os.path.join(Root_path + '/CoreData/CoreBeta/'   + Corebeta["corename"]  + '.json'), 'w') as f:    
    json.dump(Corebeta, f)    
