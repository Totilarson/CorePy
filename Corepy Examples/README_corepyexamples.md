## CorePytools package
CorePytools (CorePy) is a machine learning python package applied to data collected from geological samples of core. The primary focus of CorePy is to classify high resolution 
X-ray fluoresence data into chemofacies using unsupervised and supervised clustering tools. CorePy establishes a folder structure for input and output data. Visualizations are used to validate clustering results. There are a lot of dependencies to run corepytools and scripts. See dependencies section.

- **pip install corepytools**

## Corepy Examples
- This folder has several python scripts that are used for various functions.
 - **Corebeta.py** - lists all key parameters and variables used for each core in subsequent python scripts. outputs a .json file used in Corepy  
 - **PCAexample.py** -  Unsupervised clustering. Takes input XRF data and conducts principal component analysis. Outputs a .csv file with PCA-kmeans clusters.
 - **Corebox_crop.py** - Takes corebox images and crops them into depth registered core tubes
 - **Corepy_plotting.py** - Makes cross plots and depth profiles (chemofacies and element concentrations) to evaluate clustering results
 - **Coreimage.py** - overlays chemofacies cluster results on core box images  

## Data Examples
- contains examples of data that are needed to run both PCAexample.py and Corebox_crop.py. Running either of these scripts will establish the folder structure. Then you need to copy-paste the folders 'CoreBoxPhotos' and CoreXRF **from** Data-examples **to** './CorePy/Coredata.
- Cloning the Corepy repo should take care of this.

## PCAexample.py
- The first time through it may throw an error:
 **Error**: [Errno 2] No such file or directory: './CorePy/Coredata/CoreXRF/T5iLOD_XRF.csv'
- The folder structure will be made and the example .csv files (Public_XRF.csv and T5iLOD_XRF.csv) need to be copied to the folder: .\CorePy\CoreData\CoreXRF
- Run PCAexample again and all necessary files should be in place.
- **Core variables** - all variable are stored in **Corebeta.py** Notes are included in Corebeta.py 
- Cloning the Corepy repo should take care of this.

## Corebox_crop.py
- This script crops corebox photographs into coretubes. The first time through it will throw an error:
 - [WinError 3] The system cannot find the path specified: '.\\CorePy\\CoreData\\CoreBoxPhotos/Public'
 
- The folder structure will be made and the example Corebox photos (folder called **Public** in the provided Data-examples folder ) need to be copied in the folder: .\CorePy\CoreData\CoreBoxPhotos

- Run Corebox_crop again and all necessary files should be in place.
- Cloning the Corepy repo should take care of this.

- Now the folder **Public_cropped** should have cropped core box photographs and the **Public_tubes_vis** folder should have coretubes 

- See dependencies section

- The trial and error portion of this script is knowing where to crop each core box photo. the line: corepy.cropCorebox((70, 125, 740, 920),...) gives the coordinates used for this example. These coordinates will have to be adjusted for other photos 

## Corepy_plotting.py
- Once PCAexample.py or the Neural Model scripts (**NN_model_build** and **NN_model_apply.py**) are run there are chemofacies columns in the output spread sheets. In the Corebeta.py script you can select which chemofacies you want plotted (i.e., Chemofacies_PCA, Chemofacies_Train, or Chemofacies_NN)

## NN_model_build.py
- training data sets are built to be Formation-specific and should not be easily overwritten. There is a separate folder **"CoreNeuralModel"** where the Fomration-specific training datasets are stored.
-  Copy a .csv file here and populate the column **"Chemofacies_train"**. These values can be obtained from unsupervised or supervised approaches, but will form the basis of the Neural Model.
-  The training dataset file name should include only the Formation names and '_Trainingdataset.csv' . **For example: Eagle Ford_TrainingDataset.csv**
-  There are several strategies that can be used to edit the training dataset and look at the model results

## NN_model_apply.py
- This executes the Neural Network model that is run off the Formation-specific training dataset (saved in folder **"CoreNeuralModel"**)
- A separate .csv output file is built and it contains several columns including CHemofacies_NN and the probability

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
