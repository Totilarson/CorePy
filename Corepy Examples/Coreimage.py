import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches
import pickle
import math
import corepytools as corepy

corename = 'Public' #core name being studied

Formation = ['Eagle Ford'] # Filter the Formation column by specific formations
Formation_2=[] # This function is not built in yet, but can be used to sample members within a formation 
Formation_names = '-'.join(Formation+Formation_2) # this is used to make the directory specific to the formations
RockClassification = 'Chemofacies_PCA' # A column in the output .csv file will have this title
Depth_model='Depth_calculated'# 'XRF_adjusted_depth' and 'Wireline_Depth' are options in the data file. 
coretube_length=2
imagesuffix = 'png' #this is built for png files

#pipes the color dict file for consistent chemofacies coloring
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()

## Import datafiles
coredata = corepy.OutputXRF(corename,Formation_names)
Tubes_dir = os.path.join(str('./CorePy/CoreData/CoreTubes') + '/' + corename + '_tubes_vis')
dirName=corepy.RootDir(corename, Formation_names) 


#makes a list of the file names and sorts them top to bottom so they are called correctly in the loop
#file_names=os.listdir(Tubes_dir)
file_names=corepy.natural_sort(os.listdir(Tubes_dir))

columns = int(5)
rows=math.ceil(len(file_names)/columns)
chunksize=100 # number of files to be processed. might fail if folder doesnt have 100 files
number_chunks=math.ceil(len(file_names)/chunksize)

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), chunksize):
        # Create an index range for l of n items:
        yield l[i:i+chunksize]

a=list(chunks(file_names, chunksize)) #a list of files in each chunk
file_names=a[0] #manually select which chuck to process
rows=math.ceil(len(file_names)/columns) # rows is re-written here to use number of rows in the chunked files

fig, axs = plt.subplots(nrows=rows, ncols=columns, figsize=(10,10*rows),sharey=True)
photo_number=0 # starts counting photos at 0 in the file_names folder

for i in range(rows):
    for j in range(columns):
        photofile = file_names[photo_number]
        
        image=os.path.join(Tubes_dir,photofile)
        img = Image.open(image)
        axs[i,j].imshow(img)

    
#section adding chemofacies patches
        depths=os.path.splitext(photofile)[0].split('_') # grabs the top depth and bottom depth from the file name
        photo_top=float(depths[1]) #1
        photo_bottom=float(depths[2]) #2

        XX = coredata     [coredata     [Depth_model].between(photo_top, (photo_bottom))] # this should be working now
                
        # makes sure the rectangels are the same width
        arr = np.array(img) #converts the img to an array for pixel size information
        pixel_width=np.shape(arr)[1]*0.8
        pixel_height=np.shape(arr)[0]*0.8

        sticker_depth   = XX[Depth_model].values #depth of each sticker minus the top box depth
        pixel_depth     =(sticker_depth-photo_top)   / ((photo_top + coretube_length)-photo_top)*len(arr) # convert sticker depth to pixel depth

        photo_number=photo_number+1 # this loops the images

        for k in range(len(pixel_depth)):

            rect = patches.Rectangle((pixel_width*0.9-50  ,  pixel_depth[k])  ,  pixel_width*0.15  ,  pixel_height*0.02  ,linewidth=1 ,edgecolor='w',facecolor=chemofacies_color[XX[RockClassification].values[k]])
            axs[i,j].add_patch(rect) # Add the patch to the Axes

plt.savefig(os.path.join(dirName + '/' + corename + '_' + Formation_names +  '_' + str(photo_top) + '.png'),dpi = 300)