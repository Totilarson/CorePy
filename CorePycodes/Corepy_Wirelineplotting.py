import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
import matplotlib.patheffects as PathEffects
import json
import pandas as pd
import numpy as np


Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))


Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

dirName=corepy.RootDir(Run_settings["CoreOfStudy"], Formation_names) 
## I need to fix this color selection part
#corepy.ColorPalette(Corebeta['ColorScheme']) # I want to change color to json using chemofacies_color=json.load(open('ColorScheme.json'))


infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

#chemofacies_color2=json.load(open('ColorScheme.json'))

Formation_names = '-'.join(Run_settings["Formation"] + Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

#coredata = corepy.OutputXRF(Run_settings['CoreOfStudy'],Formation_names) # This directs to the output file

coredata=(os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '_WirelineLog_NN.csv'))
coredata=pd.read_csv(coredata)

Model_logs= Corebeta["WirelineLogs_NeuralModel"]

# This directs to the training dataset
coredata=coredata.sort_values(by=[Run_settings['Depth_model']])


dirName=corepy.RootDir(Run_settings['CoreOfStudy'], Formation_names) 

##### Plot 2 plotted with respect to depth
n=7 #c number of columns
fig, axs = plt.subplots(nrows=1, ncols=n, figsize=(15,15),sharey=True)

plt.subplot(1, n, 1)
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
    
    
plt.subplot(1, n, 2)
for i in range(len(coredata)):
    Q = [0, 0, coredata['Electrofacies_NN'][i], coredata['Electrofacies_NN'][i]]
    Z = [coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"]]
       
    plt.fill(Q, Z,c=chemofacies_color[coredata['Electrofacies_NN'][i]], linewidth=0.0)
    plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
    plt.xlim((0,6))
    plt.xlabel("Electrofacies", fontsize=18)
    #plt.ylabel(Run_settings["Depth_model"], fontsize=18)
    plt.xticks(fontsize=14)
    #plt.yticks(fontsize=14)
    plt.yticks([])
    

plt.subplot(1, n, 3)
axs=plt.plot(coredata[Model_logs[0]],coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Model_logs[0], fontsize=18)

plt.subplot(1, n, 4)
axs=plt.plot(coredata[Model_logs[1]],coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Model_logs[1], fontsize=18)


plt.subplot(1, n, 5)
axs=plt.plot(coredata[Model_logs[2]],coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Model_logs[2], fontsize=18)

plt.subplot(1, n, 6)
axs=plt.plot(coredata[Model_logs[3]],coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,200])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Model_logs[3], fontsize=18)

plt.subplot(1, n, 7)
axs=plt.plot(coredata[Model_logs[4]],coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Model_logs[4], fontsize=18)


plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Wirelinelog' + '.png'),dpi = 300)

fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(ncols=5, figsize=(20,5))
sns.boxplot(x=Run_settings["RockClassification"], y=Model_logs[0], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax1)
sns.boxplot(x=Run_settings["RockClassification"], y=Model_logs[1], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax2)
sns.boxplot(x=Run_settings["RockClassification"], y=Model_logs[2], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax3)
sns.boxplot(x=Run_settings["RockClassification"], y=Model_logs[3], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax4)
sns.boxplot(x=Run_settings["RockClassification"], y=Model_logs[4], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax5)
ax1.legend([])
ax2.legend([])
ax3.legend([])
ax4.legend([])
ax5.legend([])
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_ElectrofaciesBoxplot' + '.png'),dpi = 300)

fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(ncols=5, figsize=(20,4))
sns.boxplot(x='Electrofacies_NN', y=Model_logs[0], hue='Electrofacies_NN', palette=chemofacies_color, data=coredata,ax=ax1)
sns.boxplot(x='Electrofacies_NN', y=Model_logs[1], hue='Electrofacies_NN', palette=chemofacies_color, data=coredata,ax=ax2)
sns.boxplot(x='Electrofacies_NN', y=Model_logs[2], hue='Electrofacies_NN', palette=chemofacies_color, data=coredata,ax=ax3)
sns.boxplot(x='Electrofacies_NN', y=Model_logs[3], hue='Electrofacies_NN', palette=chemofacies_color, data=coredata,ax=ax4)
sns.boxplot(x='Electrofacies_NN', y=Model_logs[4], hue='Electrofacies_NN', palette=chemofacies_color, data=coredata,ax=ax5)
ax1.legend([])
ax2.legend([])
ax3.legend([])
ax4.legend([])
ax5.legend([])
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Electrofacies2Boxplot' + '.png'),dpi = 300)


fig, (ax1,ax2,ax3) = plt.subplots(ncols=3, figsize=(15,5))

b_plot= sns.scatterplot(x='NPHI', y='RHO8', hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color, edgecolor='black',ax=ax1)
b_plot.set(ylim=(3,1.9))
b_plot.set(xlim=(0,0.4))
b_plot.legend([])


#calcite=np.array([[0.0,30], [2.7,2.2]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot # blue
#quartz=np.array([[0.0,30], [2.6,2.075]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot # orange
#dolomite=np.array([[0.0,30], [2.85,2.38]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot # green
calcite=np.array([[0.0,3.0], [.27,.22]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot # blue
quartz=np.array([[0.0,3.0], [.26,.2075]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot # orange
dolomite=np.array([[0.0,3.0], [.285,.238]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot # green
ax1.plot(calcite[0], calcite[1]);
ax1.plot(dolomite[0], dolomite[1]);
ax1.plot(quartz[0], quartz[1]);
ax1.grid()



#limestone=np.array([[3.9,5.1]/10, [1.94,2.71]/10]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
limestone=np.array([[.39,.51], [.194,.271]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
#dolomite=np.array([[3.1,2.5], [2.87,2.025]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
#sandstone=np.array([[1.8,1.4], [2.65,1.91]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
dolomite=np.array([[.31,.25], [.287,.2025]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
sandstone=np.array([[.18,.14], [.265,.191]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot


b_plot= sns.scatterplot(x='PEF8', y='RHO8', hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color, edgecolor='black',ax=ax2)
#ax2.plot(limestone[0], limestone[1]);
#ax2.plot(dolomite[0], dolomite[1]);
#ax2.plot(sandstone[0], sandstone[1]);
#b_plot.set(ylim=(3,1.9))
#b_plot.set(xlim=(0,6))
b_plot.legend([])
ax2.grid()

#limestone=np.array([[3.9,5.1], [1.94,2.71]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
#dolomite=np.array([[3.1,2.5], [2.87,2.025]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
#sandstone=np.array([[1.8,1.4], [2.65,1.91]]) # x and y coordinates for calcite porosity on NPHI-RHOB plot
b_plot= sns.scatterplot(x='RHO8', y='HGR', hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color, edgecolor='black',ax=ax3)
#plt.plot(limestone[0], limestone[1]);
#plt.plot(dolomite[0], dolomite[1]);
#plt.plot(sandstone[0], sandstone[1]);
#b_plot.set(ylim=(3,1.9))
#b_plot.set(xlim=(0,6))
b_plot.legend([])
ax3.grid()

plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_WirelineCrossplot' + '.png'),dpi = 300)


