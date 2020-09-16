#==========================================
# Title:  settings.py
# Author: Toti Larson & Esben Pedersen
# Date:   09/16/2020
# Description:  settings.py is run first and is where variables used in subsequent scripts are defined and listed
# Version: 1.0
#   Changelog:
#==========================================

# Import libraries and dependencies
import os

# Define settings.py variables
user = "larsont"        # Used to identify file structure
corename = 'LazyA'      # Specify the core
coretube_name = 'LA'    # Two letters identifying each coretube image
photo_type = 'Vis'      # VIS or UV are the options
coretube_length = 3     # Length (in feet) of coretube images
noOfcolumns = 5         # Number of columns of core per core box

# Input list of Formations as strings, or simply use ['all'] to include all formations
Formation = ['Eagle Ford'] # Input as a list of strings
Formation_names = '-'.join(Formation) # Join formation names to be used for file naming

elements =  ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'As', 'Pb',
             'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo'] # Elements used in all PCA and neural network models

Ternary_elements=['Si', 'Al', 'Ca'] # Elements plotted in ternary diagram

outlier_multiplier = 4          # Scalar used in the statistics to identify outliers
clusters = 4                    # Number of K-means clusters used to cluster PCA
Neural_model_chemofacies = 6    # Number of chemofacies in Training dataset

# Defines how many Principal components are used to build the chemofacies
Principal_components = 2    # Number of principal components applied to clustering
PCA1 = 0                    # Principal component plotted on x-axis
PCA2 = 1                    # Principal component plotted on y-axis

# Directory and file read/write handling
coredata_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/CoreXRF')
output_dir = os.path.join('C:/Users/' + user +   '/Box/CorePy/Coreoutput' + '/' + user + '/' + corename + ' Output' + '/' + Formation_names)
coretube_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Coretubes')
corephotos_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Corephotos')
coredata_attributes = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Coredata/Coreattributes')
neural_model = os.path.join('C:/Users/' + user + '/Box/CorePy/Coreoutput' + '/' + user + '/' + 'Neuralmodel')
LOD_T5 = os.path.join(coredata_dir,'T5iLOD.csv')


### DO NOT EDIT BELOW THIS LINE  ###

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


suffix =  '.csv'
imagesuffix = '.png'
