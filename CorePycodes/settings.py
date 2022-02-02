import os
import json
import seaborn as sns
import pickle

#Run settings creates a dict file that is used in all subsequent python scripts
# For unsupervised classificaiton, Chemofacies_PCA is used.
# For supervised classification, a training dataset is required

Run_settings = {
# CoreOfStudy, Depth_model, Formation, Formation_2 define core name (.csv file), Formation (column in .csv file), and Depth_model for plotting (column in.csv file)    
"CoreOfStudy" : 'Public',
"Depth_model" : 'Depth_calculated',        # 'XRF_adjusted_depth', 'Depth_calculated' and 'Wireline_Depth' are options in the data file. 
"Formation" : ['Public Formation'], # Filter the Formation column by specific formations 'Austin Chalk', 'Eagle Ford', 'Wolfcamp', Bone Spring'
"Formation_2" : [] , # Leave blank for now.  This function can be used to sample members within a formation.

#RockClassification and Electrofacies are used for plotting. These are outputs in csv file from machine learning classifications
# both XGBoost  (Chemofacies_XGB) and Neural Network (Chemofacies_NN) classifications are calculated. 
#User can chose which to apply to figures adn subsequent calculations
"RockClassification" : 'Chemofacies_PCA',   # Chemofacies_PCA, Chemofacies_NN, Chemofacies_XGB, and Chemofacies_train are options
"Electrofacies" : 'Electrofacies_NN', # 'Electrofacies_XGB' or 'Electrofacies_NN'

# 'elements and Elements_plotted needs to be reconsidered
# 'elements' lists all the elements used in PCA and machine learning classifications. Can be changed depending on what is available or selected
# 'Elements_plotted' is a plotting variable. These can be changed depending on interest, but the sorting of elements does matter for plots.
'elements' :   ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo'],
'Elements_plotted' :  ['Ca','Al','Si', 'K', 'Mg', 'Mo','V','Ni','Cu','Sr','Mn','Cr','Ti', 'Zr'], 


# statistic variables
'outlier_multiplier' : 4,   # outlier_multiplier refers to how many standard deviations away from mean are included as outliers
'clusters' : 4,             # clusters refers to the number of K-means clusters to be calculated
'Principal_components' : 4, # Principal_components refers to the number (n) of principal components applied to K-means clustering algorithm (zero through n)
'PC1' :  0,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'PC2' :  1,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'moving_avg' : 3,           # used to smooth out attribute data in Core_attribute.py


# noOfCols and ImageType are for original core photographs
#'noOfCols' :  7,            # select number of columns in each corebox photo
#'ImageType' : 'vis',        # visible or UV images
}


# This section creates a colorscheme in the dict file that is formation specific
# Additional formation names can be added as the project requires
if Run_settings['Formation'] == ['Austin Chalk']:
    Run_settings['ColorScheme'] = [1,     2,      3,    4,     7,      5,      6,     8,     999,   9999] #Austin Chalk
if Run_settings['Formation'] == ['Eagle Ford']:
    Run_settings['ColorScheme'] =  [5    ,4      ,2    ,1      ,3      ,6     ,999     ,999    ,999    ,999] #Eagle Ford
if Run_settings['Formation'] == ['Wolfcamp']:
    Run_settings['ColorScheme'] =  [1,     0,      2,    5,    6,    8,      4,     3,     9     ,7]  #Wolfcamp
if Run_settings['Formation'] == ['Bone Spring']:    
    Run_settings['ColorScheme'] =  [0   ,1      ,4    ,3      ,2      ,8      ,7    ,5       ,6     ,9 ]  #Bone Spring
if Run_settings['Formation'] == ['Bone Spring_Lime']:
    Run_settings['ColorScheme'] = [0   ,1      ,4    ,3      ,2      ,7      ,6    ,999       ,5     ,8 ]  #Bone Spring_Lime
if Run_settings['Formation'] == ['Bone Spring_Lime']:
    Run_settings['ColorScheme'] = [0   ,1      ,4    ,3      ,2      ,7      ,6    ,999       ,5     ,8 ]  #Bone Spring_Lime
if Run_settings['Formation'] == ['Public Formation']:
    Run_settings['ColorScheme'] = [0   ,1      ,4    ,3      ,2      ,7      ,6    ,999       ,5     ,8 ]  #Public Formation

# This is an additional function that is not applied yet. Can be expanded to included FOrmation_2, but not used yet
# 
Run_settings['Formation_names'] = str(Run_settings['Formation'])


# This section creates a json file for ColorScheme called 'chemocolor' that is applied across all plots
#Chemocolor is stored in the same folder as the CorePy codes (see directory below)
Root_path = os.path.dirname(os.getcwd())
with open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings'  + '.json'), 'w') as f:    
    json.dump(Run_settings, f)
palette = dict(zip(Run_settings["ColorScheme"], sns.color_palette()))
outfile = open('chemocolor','wb')
pickle.dump(palette,outfile)
outfile.close()
