# CorePy
Python tools designed to integrate and visualize geological core data.
This repository hosts a series of scripts that are used to evaluate 
and cluster geological core-based X-ray fluorescence (XRF) measurements.
These Python tools were developed by Toti Larson and Esben Pederson at the 
University of Texas at Austin (UT Austin) Bureau opf Economic Geology (BEG) 
Mudrock Systems Research laboratory (MSRL).


Scripts
1) settings: this houses the variables used in several scripts and the 
directory structure. 
2) PCAchemofacies: this script a) sets instrument detection limits into the
XRF dataset, b) identifies outliers based on mean + 4 standard deviations, c)
conducts a principal component analysis (PCA), d) runs a k-means cluster analysis on
resutling PCA for unsupervised chamoefacies classification, e) plots PCA and cluster
results on a biplot, and f) outputs a new dataset with cluster identifications on one 
column.


Initial Folder structure:
1) Set up a Folder called "CorePy" and map coredata_dir (settings) to it. 
For example:'C:/Users/' + user + '/Box/CorePy/Coredata/CoreXRF'
2) set up /Coredata/CoreXRF/ and place the file "Core-01" in that directory
