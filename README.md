# CorePy package

CorePy is designed to perform machine learning on data collected from geological samples of core. 

CorePy bundles a wide range of data analytical tools to interpret multivariate datasets common to geological core characterization

The primary focus of CorePy is to classify high resolution X-ray fluoresence data into chemofacies using unsupervised and supervised clustering tools.

CorePy establishes a folder structure multiple users to work on the same datasets, and also provides visualizations that are useful to validate clustering results.


# Installation
pip install corepytools


# Example
PCAexample.py shows an example that imports corepy package and an example XRF datafile called 'Public_XRF.csv'




## About the authors

CorePy is being developed by Toti Larson at the University of Texas at Austin, Bureau of Economic Geology, Mudrocks Systems Research Laboratory (MSRL) research consortium.

1. **Toti E. Larson, Ph.D.** - Research Associate at the University of Texas at Austin. PI MSRL research consortium

2. **Esben Pedersen, M.S.** - Graduate student (graduated 2020) at the University of Texas at Austin. 

3. **Priyanka Periwal, P.D.** - Research Science Associate at the University of Texas at Austin. 

4. **Ana Letícia Batista** - Undergraduate at Jackson State University (graduated 2020). 2020 Jackson School of Geosciences GeoForce Student

5. **J. Evan Sivil** - Research Science Associate at the University of Texas at Austin. 

## Package Inventory
 
CorePy.py


## Package Dependencies

os
seaborn
pickle
pandas
glob
numpy
natplotlib.pyplot
seaborn as sns
sklearn.preprocessing import StandardScaler
sklearn.decomposition import PCA
sklearn.cluster import KMeans
matplotlib.patheffects

# Notes



# Folder structure
corepy-tools

    |-LICENSE.txt         **MIT**

    |-README.md           **edited in markdown**

    |-setup.py            **name=corepy-tools, package=src, python module=CorePy**

    |-src

        |-CorePy.py    **contains functions**
    
        |-__init__.py     ** empty**


