## CorePytools package

CorePytools (CorePy) is a machine learning python package applied to data collected from geological samples of core. The primary focus of CorePy is to classify high resolution 
X-ray fluoresence data into chemofacies using unsupervised and supervised clustering tools. CorePy establishes a folder structure for input and output data. Visualizations are used to validate clustering results.

Core  box photographs can be cropped and used to visualized chemofacies results. Wireline log data can be upsampled and data integrated to chemofacies for upscaling  

## Installation
pip install corepytools

The folder 'Data-example' contains examples of data that are needed to run both PCAexample and Corebox_crop. Running either of these scripts will establish the folder structure. Then you need to copy-paste the folders 'CoreBoxPhotos' and CoreXRF **from** Data-examples **to** './CorePy/Coredata

## PCAexample
This script provides an example of unsupervised clustering using principal component analysis and K-means clustering.
 after installing corepytools **pip install corepytools** run PCAexample. The first time through it will throw an error:
 **Error**: [Errno 2] No such file or directory: './CorePy/Coredata/CoreXRF/T5iLOD_XRF.csv'
 
The folder structure will be made and the example .csv files (Public_XRF.csv and T5iLOD_XRF.csv) need to be copied to the folder: .\CorePy\CoreData\CoreXRF

Run PCAexample again and all necessary files should be in place.

There are a lot of dependencies to run corepytools and PCAexample. See dependencies section

## PCAexample variables
I tried to keep this as simple as possible, but there are a lot of variables to consider when using core data. First, understand how the data is stored
in the Public_XRF.csv file. 
** Depth_model** There are different depth models (Depth_calculated, XRF_adjusted_depth, and Wireline_depth) that can be chosen.

**Formation_names** The last two columns in Puclic_XRF.csv have Formation and sub-Formation names. This function is used to isolate data from a specific formation.
An output folder is made for the Formation selected.
**RockClassification** CorePy is a clustering algorithm, and uses multiple types of clustering. This example is unsupervised PCA, so the Chemofacies_PCA is built as a column in the output .csv file.
Different clustering algorithms will be added. Chemofacies_NN for the trained neural network model results.
**elements** XRF generally includes 30 elemental concentrations, but the users can select to remove sepcific elements if interested. Add/remove elements as necessary
**outlier_multiplier** = 4 ## outlier_multiplier refers to how many standard deviations away from mean are included as outliers
**clusters** = 4 ## clusters refers to the number of K-means clusters to be used. Use whatever you would like
**Principal_components** = 4 ## Principal_components refers to the number (n) of principal components applied to K-means clustering algorithm (zero through n). See results of elebow method to decide
**Elements_plotted**=['Ca','Al','Si','K','Mg','Mo','V','Ni']
**moving_avg** used to smooth visualization data. can be any number
**XRF_resolution** The resolution (in inches) that the XRF data was collected. This value affects the chemofacies strat column built in the figure

## Corebox_crop
1) This script crops corebox photographs into coretubes. The first time through it will throw an error:
 - [WinError 3] The system cannot find the path specified: '.\\CorePy\\CoreData\\CoreBoxPhotos/Public'
 
2) The folder structure will be made and the example Corebox photos (folder called **Public** in the provided Data-examples folder ) need to be copied in the folder: .\CorePy\CoreData\CoreBoxPhotos

3) Run Corebox_crop again and all necessary files should be in place.

4) Now the folder **Public_cropped** should have cropped core box photographs and the **Public_tubes_vis** folder should have coretubes 
See dependencies section

5) The trial and error portion of this script is knowing where to crop each core box photo. the line: corepy.cropCorebox((70, 125, 740, 920),...) gives the coordinates used for this example. These coordinates will have to be adjusted for other photos 

## Package Dependencies

1) os
2) numpy
3) pandas
4) seaborn
5) pickle
6) glob
7) matplotlib.pyplot
8) seaborn
9) sklearn.preprocessing import StandardScaler
10) sklearn.decomposition import PCA
11) sklearn.cluster import KMeans
12) matplotlib.patheffects
13) corepytools
14) PIL import Image

## Lets collaborate!!!
We are interested in adding new functionality. Any and all ideas and datasets are welcome! Send me an email!
