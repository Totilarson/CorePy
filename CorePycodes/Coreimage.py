import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches
import pickle
import math
import corepytools as corepy
import json


# Coreimage.py takes core image files that are depth registered LH_6732_6735.png, for example
# The core abbreviation 'LH'is listed in corebeta .json file "corenameAbrev": LH
# images stored in folder /CoreTubes
# User needs to copy core tube images into /CoreTubes in this naming structure: Corename_vis
# known issue: 'chunk size' (defined below) and noOfColumns (defined in corebeta.json) need to be divisible or won't print
# work around: I add blank core tubes to fill bottom of core photos. Would like to improve this

# 1) Define root path, 2) load Run_settings file for input variables, and 3) 
Root_path = os.path.dirname(os.getcwd())

Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
#loads the Corebeta .json file that provides information specific to each core
#Corebeta are .json files for each core name. MOre information about these .json files in CorePy description
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))
# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names isRun_settings["Formation"]
Formation_names=corepy.Formation_names(Run_settings["Formation"],Run_settings["Formation_2"])

# loads the color palette into a dict called "chemofacies_color
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()
 
# RootDir(corename, Formation_names) established the output folder structure
dirName=corepy.RootDir(Corebeta["corename"], Formation_names) 


# Import datafiles
# Coredata for XRF files and core tube photos. Directories were created by corepytools
coredata = corepy.OutputXRF(Run_settings["CoreOfStudy"],Formation_names)
Tubes_dir = os.path.join(Root_path +   str('/CoreData/CoreTubes') + '/' + Run_settings["CoreOfStudy"] + '_tubes_vis')

#makes a list of the file names and sorts them top to bottom so they are called correctly in the loop
file_names=corepy.natural_sort(os.listdir(Tubes_dir))


# This section determines how many coretubes per row in the output image
rows=math.ceil(len(file_names)/Corebeta['noOfCols'])
chunksize=50 # number of files to be processed. might fail if folder doesnt have 100 files
number_chunks=math.ceil(len(file_names)/chunksize)

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), chunksize):
        # Create an index range for l of n items:
        yield l[i:i+chunksize]

a=list(chunks(file_names, chunksize)) #a list of files in each chunk


for h in range(len(a)):

    file_names=a[h] #manually select which chuck to process
    rows=math.ceil(len(file_names)/Corebeta['noOfCols']) # rows is re-written here to use number of rows in the chunked files
    

    fig, axs = plt.subplots(nrows=rows, ncols=Corebeta['noOfCols'], figsize=(10,10*rows),sharey=True)
    photo_number=0 # starts counting photos at 0 in the file_names folder

    for i in range(rows):
        for j in range(Corebeta['noOfCols']):
            photofile = file_names[photo_number]
        
            image=os.path.join(Tubes_dir,photofile)
            img = Image.open(image)
            axs[i,j].imshow(img)

    
#section adding chemofacies patches
            depths=os.path.splitext(photofile)[0].split('_') # grabs the top depth and bottom depth from the file name
            photo_top=float(depths[1]) #1
            photo_bottom=float(depths[2]) #2

            XX = coredata     [coredata     [Corebeta['Photo_depth']].between(photo_top, (photo_bottom))] # this should be working now
                
        # makes sure the rectangels are the same width
            arr = np.array(img) #converts the img to an array for pixel size information
            pixel_width=np.shape(arr)[1]*0.8
            pixel_height=np.shape(arr)[0]*0.8

            sticker_depth   = XX[Corebeta['Photo_depth']].values #depth of each sticker minus the top box depth
            pixel_depth     =(sticker_depth-photo_top)   / ((photo_top + Corebeta['coretube_length'])-photo_top)*len(arr) # convert sticker depth to pixel depth

            photo_number=photo_number+1 # this loops the images

            for k in range(len(pixel_depth)):

                rect = patches.Rectangle((pixel_width*0.9-50  ,  pixel_depth[k])  ,  pixel_width*0.15  ,  pixel_height*0.02  ,linewidth=1 ,edgecolor='w',facecolor=chemofacies_color[XX[Run_settings['RockClassification']].values[k]])
                axs[i,j].add_patch(rect) # Add the patch to the Axes

    plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names +  '_' + str(photo_top) + '.png'),dpi = 300)
    #plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names +  '_' + str(photo_top) + '.eps'),format='eps',dpi = 600)
    
#plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names +  '_' + str(photo_top) + '.png'),dpi = 300)