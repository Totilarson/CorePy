import os
import corepytools as corepy
from PIL import Image, ImageDraw, ImageFont
import json
#from PIL import ImageFont

# Two things here that could use improvement: core_depth and the locations for the core box cropping
# look at the four coordinates in the corepy.cropCorebox command


Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
#Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['Lease_Name']  +'.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['Lease_Name']  +'.json')))
Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

#core_depth = Corebeta['TopOfFirstCorebox'] # top depth of starting corebox phot

corepy.ImageDir(Run_settings['Lease_Name']) #sets up folder structure

Root_path = os.path.dirname(os.getcwd())
CoreBoxPhotos= os.path.join(Root_path + '/CoreData/CoreBoxPhotos/' + Run_settings['Lease_Name'])

CoreBoxPhotos_cropped= os.path.join(Root_path + '/CoreData/CoreBoxPhotos/' + '/' + Run_settings['Lease_Name'] + "_cropped")  # new directory that will be made
CoretubeFolder = os.path.join(Root_path + '/CoreData/CoreTubes/' + '/' + Run_settings['Lease_Name'] + "_tubes_" + Corebeta['ImageType']) # new directory that will be made

# Makes folders if they do not exist already. 
if not os.path.exists(CoreBoxPhotos_cropped):
    os.makedirs(CoreBoxPhotos_cropped)
    
if not os.path.exists(CoretubeFolder):
    os.makedirs(CoretubeFolder)


listing = os.listdir(CoreBoxPhotos)
for i in listing:
    
    corepy.cropCorebox((Corebeta['CoreBox_crop_points'][0], Corebeta['CoreBox_crop_points'][1], Corebeta['CoreBox_crop_points'][2], Corebeta['CoreBox_crop_points'][3]), i,CoreBoxPhotos,CoreBoxPhotos_cropped) 
    #(left, top, right,bottom)
    #crop coordinates are done by trial and error
    #change the first four numbers in the list to crop correctly

## SECTION 2: This section takes uniform cropped images and cuts them into individual coretubes


# Crop image in respective tubes
def cropCoretubes(imageFileName):
    imagePath = os.path.join(CoreBoxPhotos_cropped, imageFileName)
    imgOpen = Image.open(imagePath)
    width, height = imgOpen.size
    core_width = width/(Corebeta['noOfCols'])
    

    for i in range (1, Corebeta['noOfCols']+1):
        top_x = 0 + core_width*(i-1)
        top_y = 0
        bottom_x = core_width + core_width*(i-1)
        bottom_y = height
        imgCrop = imgOpen.crop((top_x, top_y, bottom_x, bottom_y))
              
        
        
        top_depth=os.path.splitext(imageFileName)[0].split('_') # grabs the top depth and bottom depth from the file name
        core_depth=float(top_depth[1]) #1
        core_depth = (core_depth + float(Corebeta['coretube_length']) * (i-1)  )
        
        imgDraw = ImageDraw.Draw(imgCrop)
        font = ImageFont.truetype("arial.ttf", 25)
        textWidth, textHeight = imgDraw.textsize(str(core_depth))
        imgDraw.text((((core_width-10) -textWidth)/2, 10), str(core_depth), font = font, fill = 'yellow')

        
        imageName = Corebeta['corenameAbrev'] + '_' + str(core_depth) + '_' + str(core_depth + Corebeta['coretube_length']) + '.png'
        croppedimagePath = os.path.join(CoretubeFolder, imageName)
        imgCrop.save(croppedimagePath)

        imgCrop.close()
        core_depth = core_depth + Corebeta['coretube_length']

    imgOpen.close()


#Iterate over all the images in the respective folder
listing = os.listdir(CoreBoxPhotos_cropped)
for fileName in listing:
    cropCoretubes(fileName)





















