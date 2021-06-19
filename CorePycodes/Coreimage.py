import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches
import pickle
import math
import corepytools as corepy
import json
import pandas as pd

CoreOfStudy = 'Public'

Root_path = os.path.dirname(os.getcwd())
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  CoreOfStudy + '.json')))

Root_path = os.path.dirname(os.getcwd())

Formation_names = '-'.join(Corebeta["Formation"]+Corebeta["Formation_2"]) # this is used to make the directory specific to the formations


#pipes the color dict file for consistent chemofacies coloring
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()

## Import datafiles
coredata = corepy.OutputXRF(Corebeta['corename'],Formation_names)

Tubes_dir = os.path.join(Root_path +   str('/CoreData/CoreTubes') + '/' + Corebeta['corename'] + '_tubes_vis')


dirName=corepy.RootDir(Corebeta['corename'], Formation_names) 


#makes a list of the file names and sorts them top to bottom so they are called correctly in the loop
#file_names=os.listdir(Tubes_dir)
file_names=corepy.natural_sort(os.listdir(Tubes_dir))

rows=math.ceil(len(file_names)/Corebeta['noOfCols'])
chunksize=100 # number of files to be processed. might fail if folder doesnt have 100 files
number_chunks=math.ceil(len(file_names)/chunksize)

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), chunksize):
        # Create an index range for l of n items:
        yield l[i:i+chunksize]

a=list(chunks(file_names, chunksize)) #a list of files in each chunk
file_names=a[0] #manually select which chuck to process
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

        XX = coredata     [coredata     [Corebeta['Depth_model']].between(photo_top, (photo_bottom))] # this should be working now
                
        # makes sure the rectangels are the same width
        arr = np.array(img) #converts the img to an array for pixel size information
        pixel_width=np.shape(arr)[1]*0.8
        pixel_height=np.shape(arr)[0]*0.8

        sticker_depth   = XX[Corebeta['Depth_model']].values #depth of each sticker minus the top box depth
        pixel_depth     =(sticker_depth-photo_top)   / ((photo_top + Corebeta['coretube_length'])-photo_top)*len(arr) # convert sticker depth to pixel depth

        photo_number=photo_number+1 # this loops the images

        for k in range(len(pixel_depth)):

            rect = patches.Rectangle((pixel_width*0.9-50  ,  pixel_depth[k])  ,  pixel_width*0.15  ,  pixel_height*0.02  ,linewidth=1 ,edgecolor='w',facecolor=chemofacies_color[XX[Corebeta['RockClassification']].values[k]])
            axs[i,j].add_patch(rect) # Add the patch to the Axes

plt.savefig(os.path.join(dirName + '/' + Corebeta['corename'] + '_' + Formation_names +  '_' + str(photo_top) + '.png'),dpi = 300)