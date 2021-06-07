import os
import corepytools as corepy
from PIL import Image

## SECTION 1: This section takes core box photos and crops them into uniform cropped images
corename = 'Public' #core name being studied
corenameAbrev='PC' # two letter abbreviation for subsequent core tube names

ImageType='vis' # visible or UV images
suffix = ".jpg"

noOfCols = 5# select number of columns in each corebox photo
coreSize =2 # length of each coretube 
core_depth = 3978 # top depth of starting corebox photo


corepy.ImageDir(corename) #sets up folder structure

CoreBoxPhotos= os.path.join(str('.\CorePy\CoreData\CoreBoxPhotos') + '/' + corename)
CoreBoxPhotos_cropped= os.path.join(str('.\CorePy\CoreData\CoreBoxPhotos') + '/' + corename + "_cropped")  # new directory that will be made
CoretubeFolder = os.path.join(str('.\CorePy\CoreData\CoreTubes') + '/' + corename + "_tubes_" + ImageType) # new directory that will be made


# Makes folders if they do not exist already. 
if not os.path.exists(CoreBoxPhotos_cropped):
    os.makedirs(CoreBoxPhotos_cropped)
    
if not os.path.exists(CoretubeFolder):
    os.makedirs(CoretubeFolder)


listing = os.listdir(CoreBoxPhotos)
for i in listing:
    corepy.cropCorebox((70, 125, 740, 920), i,CoreBoxPhotos,CoreBoxPhotos_cropped) #(left, top, right,bottom)
    # crop coordinates are done by trial and error
    # change the first four numbers in the list to crop correctly

## SECTION 2: This section takes uniform cropped images and cuts them into individual coretubes


# Crop image in respective tubes
def cropCoretubes(imageFileName):
    global core_depth
    imagePath = os.path.join(CoreBoxPhotos_cropped, imageFileName)
    imgOpen = Image.open(imagePath)
    width, height = imgOpen.size
    core_width = width/(noOfCols)

    for i in range (1, noOfCols+1):
        top_x = 0 + core_width*(i-1)
        top_y = 0
        bottom_x = core_width + core_width*(i-1)
        bottom_y = height
        imgCrop = imgOpen.crop((top_x, top_y, bottom_x, bottom_y))
        imageName = corenameAbrev + '_' + str(core_depth) + '_' + str(core_depth + coreSize) + '.png'
        croppedimagePath = os.path.join(CoretubeFolder, imageName)
        imgCrop.save(croppedimagePath)

        imgCrop.close()
        core_depth = core_depth + coreSize

    imgOpen.close()


#Iterate over all the images in the respective folder
listing = os.listdir(CoreBoxPhotos_cropped)
for fileName in listing:
    cropCoretubes(fileName)





















