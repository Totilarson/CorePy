# CorePytools package

CorePytools (CorePy) is a machine learning python package applied to data collected from geological samples of core. 
- The primary focus of CorePy is to classify high resolution X-ray fluoresence data into chemofacies 
- unsupervised and supervised clustering tools are applied
- CorePy establishes a folder structure for input and output data. Visualizations are used to validate clustering results.

# Installation
pip install corepytools

# Running Corepytools and CorePy 
```
1) fork the CorePy repo to your github account
2) make a local clone:
 - command line: `git clone https://github.com/Totilarson/CorePy.git` 
 - if it is necessary to delete the local clone us: 'rm -rf .git*'
3) Navigate to the local repo //CorePy/ and inspect folders 'CoreData' and 'CorePycodes'
4) In //CorePy/CorePycodes open 'settings.py' and 'PCAexample'
- 'settings.py' contains variables for all the Python scripts
 - "CoreOfStudy", "Depth_model", "Formation", and "RockClassification" should match values in Public_XRF.csv datafile
```
# Settings.py and PCAexample
```
1) Run Settings.py and PCAexample.py 
 - Running PCAexample.py will build additional output folders and run PCA-Kmeans.
 - Output files can be viewed and the results .csv includes additional columns of data
```

#CorePy_plotting.py 
```
1) provides additional elemenal plotting
 - elemental cross plots. Elements are selected from Run_settings['Elements_plotted']
 - elements plotted with respect to depth: Depth model selected by: Run_settings['Depth_model']
 - element box plots. majors and trace
 - pie chart of chemofacies abundance
 - Depth referenced chemostrat column output in a folder //CorePy/CoreOutput/CrossSection/
``` 
 

## About the authors

CorePy is being developed by Toti Larson at the University of Texas at Austin, Bureau of Economic Geology, Mudrocks Systems Research Laboratory (MSRL) research consortium.

1. **Toti E. Larson, Ph.D.** - Research Associate at the University of Texas at Austin. PI MSRL research consortium

2. **Esben Pedersen, M.S.** - Graduate student (graduated 2020) at the University of Texas at Austin. 

3. **Priyanka Periwal, Ph.D.** - Research Science Associate at the University of Texas at Austin. 

4. **J. Evan Sivil** - Research Science Associate at the University of Texas at Austin. 

5. **Geoforce students** - Ana Letícia Batista (2020) - Jackson State University 

## Package Inventory
 
corepytools.py


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


