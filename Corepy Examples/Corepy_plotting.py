import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
import matplotlib.patheffects as PathEffects
import json
import pandas as pd


CoreOfStudy = 'Public'


Corebeta=json.load(open(os.path.join(CoreOfStudy + '.json')))


## I need to fix this color selection part
corepy.ColorPalette(Corebeta['ColorScheme']) # I want to change color to json using chemofacies_color=json.load(open('ColorScheme.json'))
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

#chemofacies_color2=json.load(open('ColorScheme.json'))

Formation_names = '-'.join(Corebeta["Formation"]+Corebeta["Formation_2"]) # Would like to have Formation_names defined in Corebeta

#coredata = corepy.OutputXRF(Corebeta['corename'],Formation_names) # This directs to the output file

NeuralModel_TrainingDataSet = os.path.join(str('./CoreNeuralModel') + '/' + Formation_names  + '_TrainingDataset.csv')
coredata = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Corebeta["Depth_model"]], ascending=False) # this links to the training dataset
 # This directs to the training dataset
coredata=coredata.sort_values(by=[Corebeta['Depth_model']])


dirName=corepy.RootDir(Corebeta['corename'], Formation_names) 

## Plots made to evaluate chemofacies results 
fig, ((ax1, ax2,), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False, figsize=(10,10))

sns.scatterplot(x=Corebeta["Elements_plotted"][1], y=Corebeta["Elements_plotted"][2], hue=Corebeta["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax1, edgecolor='black')
ax1.legend([])

sns.scatterplot(x=Corebeta["Elements_plotted"][1], y=Corebeta["Elements_plotted"][3], hue=Corebeta["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax2, edgecolor='black')
ax2.legend([])

sns.scatterplot(x=Corebeta["Elements_plotted"][0], y=Corebeta["Elements_plotted"][4], hue=Corebeta["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax3, edgecolor='black')
ax3.legend([])

sns.scatterplot(x=Corebeta["Elements_plotted"][1], y=Corebeta["Elements_plotted"][5], hue=Corebeta["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax4, edgecolor='black')
ax4.legend([])

plt.savefig(os.path.join(dirName + '/' + Corebeta["corename"] + '_' + Formation_names + '_CrossPlot' + '.png'),dpi = 300)


##### Plot 2 plotted with respect to depth

fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(15,15),sharey=True)

plt.subplot(1, 9, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[Corebeta["RockClassification"]][i], coredata[Corebeta["RockClassification"]][i]]
    Z = [coredata[Corebeta["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Corebeta["Depth_model"]][i], coredata[Corebeta["Depth_model"]][i], coredata[Corebeta["Depth_model"]][i]+Corebeta["XRF_resolution"]]
       
    plt.fill(Q, Z,c=chemofacies_color[coredata[Corebeta["RockClassification"]][i]], linewidth=0.0)
    plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
    plt.xlim((0,6))
    plt.xlabel("RockClass", fontsize=18)
    plt.ylabel(Corebeta["Depth_model"], fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)  
    
    
plt.subplot(1,9,2)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][0]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
#plt.xlim([25,40])
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][0], fontsize=18)
plt.xlabel(os.path.join(Corebeta["Elements_plotted"][0]), fontsize=18)
    

plt.subplot(1, 9, 3)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][1]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][1], fontsize=18)

plt.subplot(1,9, 4)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][2]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][2], fontsize=18)


plt.subplot(1, 9, 5)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][3]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
#plt.xlim([0,175])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][3], fontsize=18)

plt.subplot(1,9,6)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][4]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
#plt.xlim([0,250])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][4], fontsize=18)

plt.subplot(1, 9, 7)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][5]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
#plt.xlim([0,250])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][5], fontsize=18)

plt.subplot(1,9,8)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][6]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
#plt.xlim([0,500])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][6], fontsize=18)

plt.subplot(1,9,9)
y_av = corepy.movingaverage(coredata[Corebeta["Elements_plotted"][7]], Corebeta["moving_avg"])
axs=plt.plot(y_av,coredata[Corebeta["Depth_model"]], color='blue')
plt.ylim((max(coredata[Corebeta["Depth_model"]]),min(coredata[Corebeta["Depth_model"]])))
#plt.xlim([0,500])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Corebeta["Elements_plotted"][7], fontsize=18)


plt.savefig(os.path.join(dirName + '/' + Corebeta["corename"] + '_' + Formation_names + '_Elementlog' + '.png'),dpi = 300)