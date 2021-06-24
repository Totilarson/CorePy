import matplotlib.pyplot as plt
import os
import corepytools as corepy
import json
from PIL import Image

Veritical_factor=50 # adjust this value if the widht/height ratios get crazy
Maximum_length=25000

#mylist = os.listdir(settings.crossection_dir)
CoreOfStudy = 'LloydHurt'
Root_path = os.path.dirname(os.getcwd())
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  CoreOfStudy + '.json')))
Formation_names = '-'.join(Corebeta["Formation"]+Corebeta["Formation_2"]) # Would like to have Formation_names defined in Corebeta

crossection_dir = os.path.join(Root_path + '/CoreOutput/CrossSection/' + Formation_names + '/')
mylist = os.listdir(crossection_dir)

fig, axs = plt.subplots(nrows=1, ncols=len(mylist), figsize=(15,15),sharey=True)

for i in range(len(mylist)):
    core_image=os.path.join(crossection_dir, mylist[i])
    img=Image.open(core_image)
    A=float(os.path.splitext(mylist[i])[0].split('_')[2]) #top depth
    B=float(os.path.splitext(mylist[i])[0].split('_')[3]) #bottom depth
    C=float(img.size[1]) # number of pixels in the depth direction
    D=C/(B-A) # scaling to normalize image heights
    img = img.resize((img.size[0],   int(img.size[1]/D*Veritical_factor)   ), Image.ANTIALIAS)
    plt.subplot(1, len(mylist), i+1), plt.imshow(img)
    plt.ylim(img.size[1] ,img.size[1]-Maximum_length) #datum on the bottom of the core
 
    plt.xticks([])
    plt.yticks([])
    plt.title(mylist[i].split('_')[0])


plt.savefig(os.path.join(Root_path + '/CoreOutput/CrossSection/' + Formation_names + '.png'),dpi = 600)

