# CorePy package
```
CorePy is a data analytics tool designed to integrate core-based geological data for machine learning characterization 
- The primary focus of CorePy is to classify high resolution X-ray fluoresence data into chemofacies 
- unsupervised and supervised clustering tools are applied
- Folder structures are developed to simplify working on multiple cores and formations
- Visualizations are used to validate clustering results
- CorePy consists of individual scripts and Pip install python package called corepytools
```

# Helpful notes
```
1) Additional notes and tips about GitHub and steps I use are here: https://github.com/Totilarson/MyCheatSheet 
```

# Installation
```
1) fork the CorePy repo to your github account
2) command line: navigate to the folder you want to install CorePy
3) make a local clone:
 - command line: `git clone https://github.com/Totilarson/CorePy.git` 
 - if it is necessary to delete the local clone use: 'rm -rf .git*'
```

# Package Dependencies
```
pip install -r requirements.txt

```

# Getting familiar with CorePy data structures
```
1) Inspect //CorePy/Data
- CoreData folder contains folders to store XRF, attribute, and beta data specific to each core.
- Open the Public_XRF file and undertand that each XRF data point is depth referenced using Core-Box-inch sticker references
- Open CoreAttributes folder. The folder 'Public' is the core name and in that folder are _TOC, _UCS, and _XRD attribute files
- All attribute files are linked with the XRF file using core-box-inch referencing
- Naming patterns for core box sticker location, wireline depths, and elemental concentrations are shown 
2) Inpect /Coredata/Corebeta folder
- Public.json contains core-specific data that is accessed by CorePy scripts. Wireline logs are also written to this files
- several settings have been shifted to the Public.json file, and this will become the repository for formation tops

```
# Getting familiar with CorePycodes
```
1) There are a series of codes in Corepy codes that have specific functions. The general path is to select the core in settings.py, then run Attribute_merge.py to build integrated datasets
2) Settings.py
- 'settings.py' contains variables for all the Python scripts
- "Lease_Name" , "Depth_model", "Formation", and "RockClassification" are the primary values that are changed by the user
- machine learning parameters are stored in settings.py
- 'chemocolor' is generated here. It makes formation-specific color schemes. If you add a new formation you have to add its colorscheme here
- Run_settings.json file is created when settings.py is executed. variables are stored here
- Elements: the complete list of elements analyzed by XRF. Elements_plotted: a specific order of elements for plotting. Model_elements: elements included in machine learning classification
- Run_settings['Elements_Depth'] was added and is formation-specific. Through time, there are key elements for each formation and I wanted an easy place to store them
```
# CoreBeta file
```
- <corename>.json files are stored for each core in //CorePy/CoreData/CoreBeta
- files provide core-specific data that is referenced in each script
- Wireline scripts also write data to the .jsom file
- The .json files can be editted with core specific data.
```
# Open and run Attribute_merge.py
```
- Merges attribute data from //CorePy/CoreData/CoreAttributes/<core name> with XRF input file
- Merges wireline data from //CorePy/CoreData/WirelineLogs/<core name> with XRF input file
- The files are merged based on Core-box-inch input from the XRF and attribute files
- Wireline log data is resampled based on core XRF data spacing
- output is a .csv file that merges XRF and attribute data
- if no attribute data is in folder it will skip over it
- Running Attribute_merge.py will build additional output folders
```
# PCAexample
```
- Running PCAexample.py will run PCA-Kmeans.
- Output files are in output folder. CSV file includes additional columns of data with colun titles Chemofacies_PCA
- the number of K-means clusters is selected in the settings.py file
- Machine learning parameters for Neural model and XGBoost clustering have been added to settings
```

# NN_Build.py and NN_apply.py
```
- these scripts build and apply results from supervised chemfoacies classifications
- An example training dataset is included in //CorePy/CoreData/CoreNeuralModel
- model parameters are output _XGB and __NN files in //CorePy/CoreData/CoreNeuralModel
- output .csv file has additional classification columns
- machine learning parameters are stored in settings.py

```
# CorePy_plotting.py 
```
1) Elemental plots and depth chemostratigraphy plots
 - elemental cross plots. Elements are selected from Run_settings['Elements_plotted']
 - elements plotted with respect to depth: Depth model selected by: Run_settings['Depth_model']
 - element box plots. majors and trace
 - pie chart of chemofacies abundance
 - Depth referenced chemostrat column output in a folder //CorePy/CoreOutput/CrossSection/
```

# Corebox_Crop.py
```
- This code does take trial and error to get the bounding parameters correct
- line 37 Corebeta['CoreBox_crop_points'] are stored for each core in the Corebeta .json file. They need to be adjusted depending on the core box photos
- Core depths are collected from the file name. The file name structure is: PublicCore_3978.jpg where 3978 refers to the top depth of the box.
- top and bottom depths for each core tube are calculated based on the box top depth, core tube length, and number of tubes in a box. This data is stored in the corebeta .json file
- Corebox photos are unique and it takes time to get this part correct
- the output are coretubes that are depth referenced
```
# Coreimage.py
```
- Designed to overlay chemofacies results on corebox photographs
- Requires coreboxphotographs be converted to 'coretubes'
- Coretubes are created from Corebox_Crop.py
- Coretubes are depth registered and in folder //CorePy/CoreData/CoreTubes/
- 'Every core is unique'....typically Depth_calculated is used to identify the position of the XRF sticker, but there are issues specific to each core
- the primary problem is when a core box overlaps another corebox 

```

# Core_attribute.py
```
- This is a plotting function and develops descriptive stats for each chemofacies based on attributes
- Core_attribute.py is run after Attribubte_merge.py
- output is a .csv file with descriptive statistics
- Box plots and depth plots show attribute results with respect to chemofacies
- It is necessasry to add "Attribute_plotted" to the core .json file
```

# Using IrfanView to crop, resize, and batch rename files
```
- download IrfanView https://www.irfanview.com/
- rotate images: Image -> Custom/Fine rotation. Adjust angle until left side of box is vertical. 
  'OK'. File -> Save (Original Folder) -> 'Save'
- cropping photos: Edit -> Create custom crop selection -> "Save and draw on image"...move box 
  crop to desired cropping. Edit -> Crop Selection (cut out) -> Save Original Folder
- cropping photos (2) -> manually click on each photo to crop. Faster this way and you can visualize
  if teh core photo needs to be rotated.
- Crop photo notes -> the goal is to be consistent. Having some of teh cardboard box around the photo
  is OK    
  Batch Rename: File -> Batch conversion/rename -> batch rename -> Batch rename settings (options) -> 
  Name pattern: R1_#####_#####, starting counter: 10500. increment: 12, where 12 is the length of the core box.
  Add all files -> Sort files: "by name, ascending natural"
  Start batch : I put them in a separate file so nothing gets deleted
```


## About the authors

CorePy is being developed by Toti Larson at the University of Texas at Austin, Bureau of Economic Geology, Mudrocks Systems Research Laboratory (MSRL) research consortium.

1. **Toti E. Larson, Ph.D.** - Research Associate at the University of Texas at Austin. PI MSRL research consortium

2. **Esben Pedersen, M.S.** - Graduate student (graduated 2020) at the University of Texas at Austin. 

3. **Priyanka Periwal, Ph.D.** - Research Science Associate at the University of Texas at Austin. 

4. **J. Evan Sivil** - Research Science Associate at the University of Texas at Austin. 

5. **Geoforce students** - Ana Letícia Batista (2020) - Jackson State University 

## Package Inventory
 


# Notes

Install corepytools using **pip install corepytools**
Follow over to the authors Github account to download example Python scripts that use corepytools


# Folder structure
CorePy

    |-LICENSE.txt         **MIT**

    |-README.md           **edited in markdown**

    |-gitignore          

    |CoreData

        |CoreAttributes
        |CoreBeta
        |CoreBoxPhotos
        |CoreNeuralModel
        |CoreXRF
    
    |CoreOutput
    
    |CorePycodes
