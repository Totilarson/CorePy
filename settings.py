#==========================================
# Title:  settings.py
# Author: Toti Larson & Esben Pedersen
# Date:   09/16/2020
# Description:  settings.py is run first and is where variables used in subsequent scripts are defined and listed
# Folder structure (i.e., 'C:/Users/') may need to be changed depending or your system
# Version: 1.0
# Python Version 3.7.6
# Operating system: Windows
#   Changelog:
#==========================================

# Import libraries and dependencies
import os

# Define settings.py variables
user = "larsont"        # Used to identify file structure
corename = 'Core-01'    # Core name (set to use the example dataset provided)
coretube_name = 'C1'    # Two letters identifying each coretube image
photo_type = 'Vis'      # Options are Vis or UV
coretube_length = 2     # Length (in feet) of coretube images for depth referencing
noOfcolumns = 5         # Number of columns within each core box

# Input list of Formations as strings, or simply use ['all'] to include all formations.
Formation = ['Eagle Ford'] # List of strings, for example: ['Pine Island', 'Cow Creek']

Formation_names = '-'.join(Formation) # For output file naming purposes, will join Formations in var Formation

XRF_resolution = 2/12 # Defines vertical resolution of XRF scans (2 inches)

elements =  ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'As', 'Pb',
             'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo'] # Elements used in all PCA and neural network models

#'Depth_calculated' is calculated from core box top depth + sticker number
#XRF_adjusted_depth are adjusted to tie to wire line logs
Depth_model = 'Depth_calculated' # 'Depth_calculated' and 'XRF_adjusted_depth' are options in the data file.



Ternary_elements = ['Si', 'Al', 'Ca'] # elements used to be plotted in ternary diagram

outlier_multiplier = 4          # Scalar chosen as cutoff to define outliers
clusters = 5                    # Number of K-means clusters used to cluster PCA (Adjust to chose number of clusters defined)
Neural_model_chemofacies = 6    # Number of chemofacies in Training dataset (var clusters+1, to account for outlier classification)

# Define how many principal components are used to build the chemofacies.
Principal_components = 2    # Number of principal components applied to clustering
PCA1 = 0  # Principal component plotted on x-axis
PCA2 = 1 # Principal component plotted on y-axis

# Directory and input/output handling. Edit to your localization.
coredata_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/CoreXRF')
output_dir = os.path.join('C:/Users/' + user +   '/Box/CorePy/Coreoutput' + '/' + user + '/' + corename + ' Output' + '/' + Formation_names)
coretube_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coretubes')
corephotos_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Corephotos')
crossection_dir = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Crossection/' + Formation_names)
coredata_attributes = os.path.join('C:/Users/' + user + '/Box/CorePy/Coredata/Coredata/Coreattributes')
neural_model = os.path.join('C:/Users/' + user + '/Box/CorePy/Coreoutput' + '/' + user + '/' + 'Neuralmodel')
LOD_T5 = os.path.join(coredata_dir,'T5iLOD.csv')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(crossection_dir):
    os.makedirs(crossection_dir)

# Defines suffix files for input data and image files
suffix =  '.csv'
imagesuffix = '.png'
