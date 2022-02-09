# CorePytools package
```
CorePytools (CorePy) applies machine learning cluster algorithms to geological samples of core. 
- The primary focus of CorePy is to classify high resolution X-ray fluoresence data into chemofacies 
- unsupervised and supervised clustering tools are applied
- Folder structures are developed to simplify working on multiple cores and formations
- Visualizations are used to validate clustering results.
```

# Installation
```
pip install corepytools
- corepytools includes commonly applied functions that are called by different Python scripts
- corepytools is a dependency 
```
# Running Corepytools and CorePy 
```
1) fork the CorePy repo to your github account
2) make a local clone:
 - command line: `git clone https://github.com/Totilarson/CorePy.git` 
 - if it is necessary to delete the local clone use: 'rm -rf .git*'
3) Navigate to the local repo //CorePy/ and inspect folders 'CoreData' and 'CorePycodes'
4) In //CorePy/CorePycodes open 'settings.py' and 'PCAexample'
- 'settings.py' contains variables for all the Python scripts
 - "CoreOfStudy", "Depth_model", "Formation", and "RockClassification" should match values in Public_XRF.csv datafile
```

# Data examples
```
- CoreData folder contains an example of a high reoslution XRF dataset and corebox photographs
- Naming patterns for core box sticker location, wireline depths, and elemental concentrations are shown 
```

# Settings.py and PCAexample
```
- Running PCAexample.py will build additional output folders and run PCA-Kmeans.
- Output files are in output folder. CSV file includes additional columns of data
- Settings.py writes a Run_settings.json file that is accessed by other scripts
```

# CoreBeta file
```
- <corename>.json files are stored for each core in //CorePy/CoreData/CoreBeta
- files provide core-specific data that is referenced in each script
- Wireline scripts also write data to the .jsom file
```

# CorePy_plotting.py 
```
1) provides additional elemenal plotting
 - elemental cross plots. Elements are selected from Run_settings['Elements_plotted']
 - elements plotted with respect to depth: Depth model selected by: Run_settings['Depth_model']
 - element box plots. majors and trace
 - pie chart of chemofacies abundance
 - Depth referenced chemostrat column output in a folder //CorePy/CoreOutput/CrossSection/
``` 
 
# NN_Build.py and NN_apply.py
```
- these scripts build and apply results from supervised chemfoacies classifications
- An example training dataset is included in //CorePy/CoreData/CoreNeuralModel
- model parameters are output _XGB and __NN files in //CorePy/CoreData/CoreNeuralModel
- output .csv file has additional classification columns

```

# Coreimage.py
```
- Designed to overlay chemofacies results on corebox photographs
- Requires coreboxphotographs be converted to 'coretubes'
- Coretubes are created from Corebox_Crop.py
- Coretubes are depth registered and in folder //CorePy/CoreData/CoreTubes/

```
## About the authors

CorePy is being developed by Toti Larson at the University of Texas at Austin, Bureau of Economic Geology, Mudrocks Systems Research Laboratory (MSRL) research consortium.

1. **Toti E. Larson, Ph.D.** - Research Associate at the University of Texas at Austin. PI MSRL research consortium

2. **Esben Pedersen, M.S.** - Graduate student (graduated 2020) at the University of Texas at Austin. 

3. **Priyanka Periwal, Ph.D.** - Research Science Associate at the University of Texas at Austin. 

4. **J. Evan Sivil** - Research Science Associate at the University of Texas at Austin. 

5. **Geoforce students** - Ana Letícia Batista (2020) - Jackson State University 

## Package Inventory
 


## Package Dependencies

1) os
2) numpy
3) pandas
4) seaborn
5) pickle
6) glob
7) matplotlib.pyplot
8) seaborn as sns
9) sklearn.preprocessing import StandardScaler
10) sklearn.decomposition import PCA
11) sklearn.cluster import KMeans
12) matplotlib.patheffects
13) json
14) corepytools
15) from sklearn.model_selection import train_test_split
16) from sklearn.preprocessing import StandardScaler
17) from sklearn.neural_network import MLPClassifier
18) from sklearn.metrics import classification_report, confusion_matrix
19) from sklearn import metrics
20) import matplotlib.pyplot as plt
21) matplotlib.patches as patches


# Notes

Install corepytools using **pip install corepytools**
Follow over to the authors Github account to download example Python scripts that use corepytools


# Folder structure
corepytools

    |-LICENSE.txt         **MIT**

    |-README.md           **edited in markdown**

    |-setup.py            **name=corepy-tools, package=src, python module=corepytools**

    |-src

        |-corepytools    **contains functions**
    
        |-__init__.py     ** empty**


