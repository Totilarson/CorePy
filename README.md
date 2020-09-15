# CorePy
Python tools designed to integrate and visualize geological core data.
This repository hosts a series of scripts that are used to evaluate 
and cluster geological core-based X-ray fluorescence (XRF) measurements.

Scripts
1) settings: this houses the variables used in several scripts and the 
directory structure
2) PCAchemofacies: this script a) sets instrument detection limits into the
XRF dataset, b) identifies outliers based on mean + 4 standard deviations, c)
conducts a principal component analysis (PCA), d) runs a k-means cluster analysis on
resutling PCA for unsupervised chamoefacies classification, e) plots PCA and cluster
results on a biplot, and f) outputs a new dataset with cluster identifications on one 
column,
