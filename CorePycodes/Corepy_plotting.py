import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
import matplotlib.patheffects as PathEffects
import json
import pandas as pd


Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

## I need to fix this color selection part
#corepy.ColorPalette(Corebeta['ColorScheme']) # I want to change color to json using chemofacies_color=json.load(open('ColorScheme.json'))


   #C:\Users\larsont\Box\GitRepos\CorePy\CoreData\CoreNeuralModel

infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

#chemofacies_color2=json.load(open('ColorScheme.json'))

Formation_names = '-'.join(Run_settings["Formation"] + Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

coredata = corepy.OutputXRF(Run_settings['CoreOfStudy'],Formation_names) # This directs to the output file


# use this coredata to visualize the training datasets
#coredata = (os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names + '_TrainingDataset.csv'))
#coredata=pd.read_csv(coredata)


# This directs to the training dataset
coredata=coredata.sort_values(by=[Run_settings['Depth_model']])


dirName=corepy.RootDir(Run_settings['CoreOfStudy'], Formation_names) 

## Plots made to evaluate chemofacies results 
fig, ((ax1, ax2,), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False, figsize=(10,10))

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][2], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax1, edgecolor='black')
ax1.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][3], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax2, edgecolor='black')
ax2.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][0], y=Run_settings["Elements_plotted"][4], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax3, edgecolor='black')
ax3.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][5], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax4, edgecolor='black')
ax4.legend([])

plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_CrossPlot' + '.png'),dpi = 300)


##### Plot 2 plotted with respect to depth

fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(15,15),sharey=True)

plt.subplot(1, 9, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[Run_settings["RockClassification"]][i], coredata[Run_settings["RockClassification"]][i]]
    Z = [coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"]]
       
    plt.fill(Q, Z,c=chemofacies_color[coredata[Run_settings["RockClassification"]][i]], linewidth=0.0)
    plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
    plt.xlim((0,6))
    plt.xlabel("RockClass", fontsize=18)
    plt.ylabel(Run_settings["Depth_model"], fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)  
    
    
plt.subplot(1,9,2)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][0]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([25,40])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][0], fontsize=18)
plt.xlabel(os.path.join(Run_settings["Elements_plotted"][0]), fontsize=18)
    

plt.subplot(1, 9, 3)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][1]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][1], fontsize=18)

plt.subplot(1,9, 4)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][2]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][2], fontsize=18)


plt.subplot(1, 9, 5)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][3]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,175])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][3], fontsize=18)

plt.subplot(1,9,6)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][4]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,250])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][4], fontsize=18)

plt.subplot(1, 9, 7)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][5]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,250])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][5], fontsize=18)

plt.subplot(1,9,8)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][6]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,500])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][6], fontsize=18)

plt.subplot(1,9,9)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][7]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,500])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][7], fontsize=18)


plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Elementlog' + '.png'),dpi = 300)


plt.subplot(1, 1, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[Run_settings["RockClassification"]][i], coredata[Run_settings["RockClassification"]][i]]
    Z = [coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"]]
       
    plt.fill(Q, Z,c=chemofacies_color[coredata[Run_settings["RockClassification"]][i]], linewidth=0.0)
    plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
    plt.xlim((0,6))
    plt.yticks([])
    plt.xticks([])
    
    
bottom_core = str(round(max(coredata[Run_settings["Depth_model"]])))
top_core = str(round(min(coredata[Run_settings["Depth_model"]])))
plt.tight_layout()
plt.savefig(os.path.join(Root_path + '/CoreOutput/CrossSection/' + Formation_names + '/'  + Run_settings["CoreOfStudy"] + '_' + Formation_names +  '_' + top_core + '_' + bottom_core + '_' + '.png'),dpi = 600)



fig, (ax1) = plt.subplots(ncols=1, figsize=(5,5))
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][8]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax1)
plt.ylim([0,75])
ax1.legend([])
