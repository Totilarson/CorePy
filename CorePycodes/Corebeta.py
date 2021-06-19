import json
import seaborn as sns
import os
import corepytools as corepy

Corebeta = {

"corename" : 'Public', #core name being studied
"corenameAbrev" : 'PC', # two letter abbreviation for subsequent core tube names
"Depth_model" : 'Depth_calculated' ,        # 'XRF_adjusted_depth' and 'Wireline_Depth' are options in the data file. 

"Formation" : ['Eagle Ford'], # Filter the Formation column by specific formations
"Formation_2" : [] ,        # This function is not built in yet, but can be used to sample members within a formation 

"RockClassification" : 'Chemofacies_PCA',   # A column in the output .csv file will have this title
"Depth_model" : 'Depth_calculated',         #'XRF_adjusted_depth' and 'Wireline_Depth' are options in the data file. 
"coretube_length" : 2,      # length of each coretube 
'noOfCols' :  5,            # select number of columns in each corebox photo

'outlier_multiplier' : 4,   # outlier_multiplier refers to how many standard deviations away from mean are included as outliers
'clusters' : 4,             # clusters refers to the number of K-means clusters to be used
'Principal_components' : 4, # Principal_components refers to the number (n) of principal components applied to K-means clustering algorithm (zero through n)
'XRF_resolution' : 2/12,    # used to build chemofacies stacking pattern. 2/12 refers to 2" xrf scanning resolution
'ImageType' : 'vis',        # visible or UV images
'moving_avg' : 3,           # used to smooth out XRF data
# For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'PC1' :  0,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'PC2' :  1,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
 # this is used to make the directory specific to the formations
'ColorScheme' : [1,     2,      3,    4,    5,      6,     7,     8,   9 ,   10], 
#                blue, orange, green, red, purple, brown, pink, grey, gold, teal

'Elements_plotted' :  ['Ca','Al','Si','K','Mg','Mo','V','Ni'], # plotting variable. These can be changed depending on interest. 

'elements' :   ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'As', 'Pb','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo'],

}

Formation_names=corepy.Formation_names(Corebeta["Formation"],Corebeta["Formation_2"])
corepy.RootDir(Corebeta["corename"], Formation_names)


Root_path = os.path.dirname(os.getcwd())

with open(os.path.join(Root_path + '/CoreData/CoreBeta/'   + Corebeta["corename"] + '.json'), 'w') as f:    
#with open(os.path.join(Corebeta["corename"] + '.json'), 'w') as f:
    json.dump(Corebeta, f)    

    
palette = dict(zip(Corebeta["ColorScheme"], sns.color_palette()))

#with open(os.path.join(Root_path + '/CoreData/CoreBeta/'   + Corebeta["corename"] + '_Colorscheme.json'), 'w') as f:
#with open('ColorScheme.json', 'w') as f:
  #  json.dump(palette, f)
    
    
    
    
#import PCAexample.py

#import Corepy_plotting.py