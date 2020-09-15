#setting is run first and is where the variables are listed

import os
user = "larsont"        # used to identify file structure
corename = 'LazyA'      #specify the core
coretube_name = 'LA'    #two letters identifying each coretube image
photo_type = 'Vis'      # VIS or UV are the options
coretube_length = 3     #length in feet of coretube images
noOfcolumns = 5

# Input list of Formations as strings, or simply use ['all'] to include all formations
Formation = ['Eagle Ford'] # List of strings

Formation_names = '-'.join(Formation) # For output name purposes

elements =  ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'As', 'Pb', 
             'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo'] #elements used in all PCA and neural network models

Ternary_elements=['Si', 'Al', 'Ca'] # elements plotted in ternary diagram

outlier_multiplier = 4      # used in the statistics to identify outliers
clusters = 4                # number of K-means clusters used to cluster PCA
Neural_model_chemofacies=6  # Number of chemofacies in Training dataset

#how many Principal components are used to build the chemofacies.
Principal_components = 2    # number of principal components applied to clustering
PCA1=0  # principal component plotted on x-axis
PCA2=1 # principal component plotted on y-axis

coredata_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/CoreXRF')
output_dir = os.path.join('C:/Users/' + user +   '/Box/CorePy/Coreoutput' + '/' + user + '/' + corename + ' Output' + '/' + Formation_names)
coretube_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Coretubes') 
corephotos_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Corephotos') 
coredata_attributes = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Coredata/Coreattributes') 
neural_model = os.path.join('C:/Users/' + user + '/Box/CorePy/Coreoutput' + '/' + user + '/' + 'Neuralmodel')
LOD_T5 = os.path.join(coredata_dir,'T5iLOD.csv')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


suffix =  '.csv'
imagesuffix = '.png'
