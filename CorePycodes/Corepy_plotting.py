import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
import json
import pandas as pd


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

# import XRF file from core output folder. OutputXRF(corename,Formation_names)
coredata = corepy.OutputXRF(Run_settings['CoreOfStudy'],Formation_names) 
# use this to import the training dataset. Need to set 
#coredata=pd.read_csv((os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names + '_TrainingDataset.csv')))

coredata=coredata.sort_values(by=[Run_settings['Depth_model']]) #sorts data by depth


#attributeimport  = (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Attribute.csv'))
#attributedata=pd.read_csv(attributeimport)

## Plots made to evaluate chemofacies results 
fig, ((ax1, ax2,), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2, sharex=False, sharey=False, figsize=(10,15))

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][2], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax1, edgecolor='black')
ax1.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][0], y=Run_settings["Elements_plotted"][4], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax2, edgecolor='black')
ax2.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][5], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax3, edgecolor='black')
ax3.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][6], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax4, edgecolor='black')
ax4.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][7], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax5, edgecolor='black')
ax5.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][8], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax6, edgecolor='black')
ax6.legend([])

plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_CrossPlot_' + Run_settings["RockClassification"] + '.png'),dpi = 300)
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_CrossPlot_' + Run_settings["RockClassification"] + '.eps'),format='eps',dpi = 600)


##### Plot 2 plotted with respect to depth

n=6

fig, axs = plt.subplots(nrows=1, ncols=13, figsize=(15,15),sharey=True)

plt.subplot(1, n, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[Run_settings["RockClassification"]][i]+2, coredata[Run_settings["RockClassification"]][i]+2]
    Z = [coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"]]
       
    plt.fill(Q, Z,c=chemofacies_color[coredata[Run_settings["RockClassification"]][i]], linewidth=0.0)
    plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
    plt.xlim((0,6))
    plt.xlabel(Run_settings["RockClassification"], fontsize=18)
    plt.xlabel('Rockclass', fontsize=18)
    plt.ylabel(Run_settings["Depth_model"], fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)  

  
plt.subplot(1,n,2)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][0]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,1])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_plotted"][0], fontsize=18)
plt.xlabel(os.path.join(Run_settings["Elements_plotted"][0]), fontsize=18)

    

plt.subplot(1, n, 3)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][2]]/coredata[Run_settings["Elements_plotted"][1]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.yticks([])
plt.xticks(fontsize=14)
#plt.xscale('log')
plt.xlabel(Run_settings["Elements_plotted"][3], fontsize=18)
plt.xlabel('Si/Al', fontsize=18)

plt.subplot(1,n, 4)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][5]]/coredata[Run_settings["Elements_plotted"][1]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,0.02])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel('Mo/Al', fontsize=18)


plt.subplot(1, n, 5)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][6]]/coredata[Run_settings["Elements_plotted"][1]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,10])
#plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel('V/Al', fontsize=18)

plt.subplot(1,n,6)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][7]]/coredata[Run_settings["Elements_plotted"][1]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.xlim([0,200])
#plt.yticks([])
#plt.xscale('log')
plt.xticks(fontsize=14)

plt.xlabel('Ni/Al', fontsize=18)

plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Elementlog_' + Run_settings["RockClassification"] + '.png'),dpi = 300)
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Elementlog_' + Run_settings["RockClassification"] + '.eps'),format='eps', dpi = 600)


fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(ncols=5, figsize=(25,5))
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][0]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax1,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][1]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax2,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][2]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax3,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][3]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax4,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][4]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax5,dodge =False,width=0.75)
ax1.legend([])
ax2.legend([])
ax3.legend([])
ax4.legend([])
ax5.legend([])
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_MajorElementBoxplot_' + Run_settings["RockClassification"] + '.png'),dpi = 300)

fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(ncols=5, figsize=(25,5))
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][5]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax1,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][6]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax2,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][7]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax3,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][8]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax4,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=coredata[Run_settings["Elements_plotted"][9]], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=coredata,ax=ax5,dodge =False,width=0.75)
ax1.legend([])
ax2.legend([])
ax3.legend([])
ax4.legend([])
ax5.legend([])
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_TraceElementBoxplot_' + Run_settings["RockClassification"] + '.png'),dpi = 300)

fig, (ax1) = plt.subplots(ncols=1, figsize=(5,5))


# Pie chart calculation and plotting for chemofacies


coredata_pie=(coredata[coredata['Formation'] == Formation_names])

#coredata_pie=(coredata[coredata['Formation_2'] == 'AC-D'])


coredata_pie=coredata_pie[Run_settings["RockClassification"]].value_counts()

coredata_pie = pd.DataFrame(coredata_pie)
coredata_pie.reset_index(inplace=True)
coredata_pie = coredata_pie.rename(columns = {'index': Run_settings["RockClassification"], Run_settings["RockClassification"]: 'Count'}, inplace = False)


plt.pie(coredata_pie.Count,colors=[chemofacies_color[key] for key in coredata_pie[Run_settings["RockClassification"]]],
        #shadow=False,
        #labels=df['Chemofacies_NN'],
       #explode=(0,0,0,0, 0, 0, 0),
    # with the start angle at 90%
        startangle=90,
        #with the percent listed as a fraction
        #autopct='%1.1f%%',
        #pctdistance=1.2,
        )

plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_PieChart_' + Run_settings["RockClassification"] + '.png'),dpi = 300)
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_PieChart_' + Run_settings["RockClassification"] + '.eps'),format='eps', dpi = 600)


fig, axs = plt.subplots(nrows=1, ncols=1)
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
