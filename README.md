# CorePy
CorePy is a series of tools written in Python (Version 3.7.6) designed to integrate and visualize geological core data.
This public repository hosts a series of scripts that are used to evaluate
and cluster geological core-based X-ray fluorescence (XRF) measurements.
These Python tools were developed by Toti Larson and Esben Pedersen at the
University of Texas at Austin (UT Austin) Bureau of Economic Geology (BEG)
Mudrock Systems Research laboratory (MSRL).


Scripts included in this public release of CorePy:
1) settings.py: this script houses the variables used in several scripts and defines the
directory structure and input/output file handling for usage in subsequent scripts.
2) PCAchemofacies.py: this script a) sets instrument detection limits into the
XRF dataset, b) identifies outliers based on mean + 4 standard deviations, c)
conducts a principal component analysis (PCA), d) runs a k-means cluster analysis on resulting PCA for unsupervised chemofacies classification, e) plots PCA and cluster results on a biplot, and f) outputs a new dataset with cluster identifications in an appended column.


Initial setup instructions & directory handling:
1) Create a local folder called "CorePy" and map coredata_dir (edit the respective line(s) in settings.py) to it.
For example:'C:/Users/' + user + '/Box/CorePy/Coredata/CoreXRF'
2) Set up /Coredata/CoreXRF/ and place the file "Core-01" in that directory (Example dataset to test PCAchemofacies.py)
3) Run Settings.py
4) Run PCAchemofacies.py

NOTE That it may be necessary to install python packages in addition to those provided by your default python distribution in order for this version of CorePy to run and operate as intended.
