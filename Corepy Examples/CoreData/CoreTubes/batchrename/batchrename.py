import os
import glob

path = 'C:/Users/larsont/Documents/gitrepos/CorePy/Corepy Examples/CoreData/CoreTubes/batchrename/'
renamepath = 'C:/Users/larsont/Documents/gitrepos/CorePy/Corepy Examples/CoreData/CoreTubes/batchrename/rename/'

#Q=os.listdir(path)

#




pngfiles = []
for file in glob.glob("*.png"):
    pngfiles.append(file)
    
    
for i in range(len(pngfiles)): #add the -1 becaue
    os.rename(os.path.join(path + '/' + pngfiles[i]), os.path.join(renamepath + '/' + pngfiles[i][:2] + '_' + pngfiles[i][2:6] + '_' + pngfiles[i][7:11] + '.png' ))