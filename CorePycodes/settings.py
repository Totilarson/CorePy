import os
import json
import seaborn as sns
import pickle

#Run settings creates a dict file that is used in all subsequent python scripts
# For unsupervised classificaiton, Chemofacies_PCA is used.
# For supervised classification, a training dataset is required

Run_settings = {
# CoreOfStudy, Depth_model, Formation, Formation_2 define core name (.csv file), Formation (column in .csv file), and Depth_model for plotting (column in.csv file)    
"Lease_Name" : 'Medina',
"Depth_model" : 'Depth_calculated',        # 'XRF_adjusted_depth', 'Depth_calculated' and 'Wireline_Depth' are options in the data file. 
"Formation" : ['Eagle Ford'], # Filter the Formation column by specific formations 'Austin Chalk', 'Eagle Ford', 'Wolfcamp', Bone Spring'
"Formation_2" : [] , # Leave blank for now.  This function can be used to sample members within a formation.

#"Formation Model": ['Wolfcamp'], # Gives the option to run Formation-specific models and define the formation range from tops


#RockClassification and Electrofacies are used for plotting. These are outputs in csv file from machine learning classifications
# both XGBoost  (Chemofacies_XGB) and Neural Network (Chemofacies_NN) classifications are calculated. 
#User can chose which to apply to figures adn subsequent calculations
"RockClassification" : 'Chemofacies_NN',   # Chemofacies_PCA, Chemofacies_NN, Chemofacies_XGB, and Chemofacies_train are options
"Electrofacies" : 'Electrofacies_NN', # 'Electrofacies_XGB' or 'Electrofacies_NN'

# 'elements and Elements_plotted needs to be reconsidered
# 'elements' lists all the elements used in PCA and machine learning classifications. Can be changed depending on what is available or selected
# 'Elements_plotted' is a plotting variable. These can be changed depending on interest, but the sorting of elements does matter for plots.
'elements' :         ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga','As','Pb','Se','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo'],
'Elements_plotted' :  ['Ca','Al','Si', 'K', 'Sr', 'Mo','V','Ni','Cu','Mg','Mn','Cr','Ti', 'Zr','Fe','Th','Zn','Na'], 


# statistic variables
'outlier_multiplier' : 4,   # outlier_multiplier refers to how many standard deviations away from mean are included as outliers
'clusters' : 5,             # clusters refers to the number of K-means clusters to be calculated
'Principal_components' : 5, # Principal_components refers to the number (n) of principal components applied to K-means clustering algorithm (zero through n)
'PC1' :  0,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'PC2' :  1,       # For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
'moving_avg' : 3,           # used to smooth out attribute data in Core_attribute.py

# Machine learning clustering parameters

## Neural Network Machine Learning Parameters 
'NN_HiddenLayer_size' : (10,10,10), # number of hidden layers and nodes in the hidden layers
'random_state' : 1,
'activation' : 'relu', # activation{‘identity’, ‘logistic’, ‘tanh’, ‘relu’}
'solver' :'sgd',  # solver{‘lbfgs’, ‘sgd’, ‘adam’} 
'max_iter': 2000,
'NN_TrainingData_test_size' : 0.25,
'NN_TrainingData_random_state' : 0,



## XGBoost Machine Learning Parameters 
'max_depth': 10,  # the maximum depth of each tree. too high and will overfit. Noticed with Iris dataset that if the number is less than the number of features it skips a feature
'eta': 0.3,  # the training step for each iteration
'silent': 1,  # logging mode - quiet
'objective': 'multi:softprob',  # error evaluation for multiclass training
'num_class': 9, # the number of classes that exist in this datset
'num_round' : 5,  # the number of training iterations

'XGB_TrainingData_test_size' : 0.25,
'XGB_TrainingData_random_state' :0,

}


# This section creates a colorscheme in the dict file that is formation specific
# Additional formation names can be added as the project requires
if Run_settings['Formation'] == ['Austin Chalk']:
    #Run_settings['ColorScheme'] = [1,     2,      3,    4,     6,      5,      8,     7,     9,   9999] #Austin Chalk
    Run_settings['Elements_Depth'] = ['Ca','Sr','Mn', 'Al', 'Mo', 'Ni'] # Eagle Ford
    Run_settings['elements'] =         ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga','As','Pb','Se','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']
    Run_settings['Model_elements'] =   ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe',       'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga',               'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']




if Run_settings['Formation'] == ['Eagle Ford']:
    #Run_settings['ColorScheme'] =  [5    ,4      ,2    ,1      ,3      ,6     ,10     ,8    ,7    ,9] #Eagle Ford
    Run_settings['Elements_Depth'] = ['Ca','Sr','Mn', 'Al', 'Mo', 'Ni'] # Eagle Ford
    Run_settings['elements'] =         ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga','As','Pb','Se','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']
    Run_settings['Model_elements'] =   ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe',       'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga',               'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']



if Run_settings['Formation'] == ['Wolfcamp']:
    Run_settings['Elements_Depth'] = ['Ca','Sr','Mn', 'Al', 'Mo', 'Ni'] # Wolfcamp
    Run_settings['elements'] =         ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga','As','Pb','Se','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']
    Run_settings['Model_elements'] =   ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe',       'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga',               'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']
   
if Run_settings['Formation'] == ['Bone Spring']:    
    Run_settings['Elements_Depth'] = ['Ca','Sr','Mn', 'Al', 'Mo', 'Ni'] # Bone Spring
    Run_settings['elements'] =         ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga','As','Pb','Se','Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']
    Run_settings['Model_elements'] =   ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe',       'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga',               'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']

Run_settings['Formation_names'] = str(Run_settings['Formation'])

# This section creates a json file for ColorScheme called 'chemocolor' that is applied across all plots
#Chemocolor is stored in the same folder as the CorePy codes (see directory below)
Root_path = os.path.dirname(os.getcwd())
with open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings'  + '.json'), 'w') as f:    
    json.dump(Run_settings, f)


palette = {7: (0.00000000,	0.69019608,	0.31372549),
 1: (0.00000000,	0.98823529,	0.96470588),
 2: (1.00000000,	0.00000000,	1.00000000),
 3: (0.43921569,	0.18823529,	0.62745098),
 4: (0.00000000,	0.46274510,	0.71372549),
 5: (1.00000000,	0.5000000,	0.00000000),
 6: (1.00000000,	1.00000000,	0.00000000),
 14: (0.19215686,	0.11372549,	0.00000000),
 100: (0.00000000,	0.98823529,	0.96470588),
 9: (0.74117647,	0.84313725,	0.93333333),
 10:(0.43921569,	0.18823529,	0.62745098),
 11:(0.84705882,	0.84705882,	0.84705882),
 12:(0.00000000,	0.46274510,	0.71372549),
 13:(0.19215686,    0.11372549,	0.00000000),
 0:(0.34901961,	0.34901961,	0.34901961),
 15:(0.83921569,    0.15294118, 0.15686275)
}

#original line up of colors
# 0 = green; 1 = teal; 2 = pink; 3 = purple; 4 = blue; 5 = orange; 6 = yellow; 7 = brown; 8 = teal; 9 = light blue; 10 - purple; 11 = light grey; 12 = blue; 13 = dark brown; 14 = dark grey; 15=red		
# 7 = green; 1 = teal; 2 = pink; 3 = purple; 4 = blue; 5 = orange; 6 = yellow; 7 = brown; 0 = teal; 9 = light blue; 10 - purple; 11 = light grey; 12 = blue; 13 = dark brown; 0 = dark grey; 15=red


#palette = dict(zip(Run_settings["ColorScheme"], sns.color_palette()))
#palette = dict(zip(Run_settings["ColorScheme"], NewColor))
outfile = open('chemocolor','wb')
pickle.dump(palette,outfile)
outfile.close()

