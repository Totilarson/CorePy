import os
import json
import seaborn as sns
import pickle

Run_settings = {
"CoreOfStudy" : 'LazyA',
"Depth_model" : 'Depth_calculated' ,        # 'XRF_adjusted_depth' and 'Wireline_Depth' are options in the data file. 
"Formation" : ['Eagle Ford'], # Filter the Formation column by specific formations
"Formation_2" : [] ,        # This function is not built in yet, but can be used to sample members within a formation 
"RockClassification" : 'Chemofacies_NN',   # A column in the output .csv file will have this title

'outlier_multiplier' : 4,   # outlier_multiplier refers to how many standard deviations away from mean are included as outliers
'clusters' : 4,             # clusters refers to the number of K-means clusters to be used
'Principal_components' : 4, # Principal_components refers to the number (n) of principal components applied to K-means clustering algorithm (zero through n)


'noOfCols' :  5,            # select number of columns in each corebox photo
'ImageType' : 'vis',        # visible or UV images
'moving_avg' : 3,           # used to smooth out XRF data
# For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'PC1' :  0,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'PC2' :  1,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
 # this is used to make the directory specific to the formations
#'ColorScheme' :  [1,     2,      3,    4,     7,      5,      6,     8,     999,   9999], #Austin Chalk
#'ColorScheme' :  [7   ,2      ,1    ,10      ,4      ,8      ,3    ,6       ,9     ,5 ],  #Bone Spring
'ColorScheme' :  [10    ,4      ,2    ,1      ,3      ,20     ,5     ,999    ,999    ,999], #Eagle Ford
#                blue, orange, green, red,   purple, brown,  pink,  grey,    gold,   teal
'Elements_plotted' :  ['Ca','Al','Si','K','Mg','Mo','V','Ni'], # plotting variable. These can be changed depending on interest. 
'elements' :   ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'As', 'Pb','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo'],
}

Run_settings['Formation_names'] = str(Run_settings['Formation'])

Root_path = os.path.dirname(os.getcwd())

with open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings'  + '.json'), 'w') as f:    
    json.dump(Run_settings, f)
    
palette = dict(zip(Run_settings["ColorScheme"], sns.color_palette()))

outfile = open('chemocolor','wb')
pickle.dump(palette,outfile)
outfile.close()





# First step is to run Corebeta.py to make a json file for the core of interest

# Decide which model you want. General path is:
    # 1) run PCAexample to set up folder structure and run outlier tests
    # 2) run Corepy_plotting

#import PCAexample
#import NN_model_build
#import NN_model_apply
#import Corepy_plotting

