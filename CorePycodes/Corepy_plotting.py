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
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['Lease_Name']  +'.json')))

# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names isRun_settings["Formation"]
Formation_names=corepy.Formation_names(Run_settings["Formation"],Run_settings["Formation_2"])

# loads the color palette into a dict called "chemofacies_color
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()
 
# RootDir(corename, Formation_names) established the output folder structure
dirName=corepy.RootDir(Run_settings["Lease_Name"], Formation_names) 

# import XRF file from core output folder. OutputXRF(corename,Formation_names)
coredata = corepy.OutputXRF(Run_settings['Lease_Name'],Formation_names) 
# use this to import the training dataset. Need to set 


coredata=coredata.sort_values(by=[Run_settings['Depth_model']]) #sorts data by depth


#attributeimport  = (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Attribute.csv'))
#attributedata=pd.read_csv(attributeimport)

## Plots made to evaluate chemofacies results 
fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12), (ax13, ax14, ax15, ax16)) = plt.subplots(nrows=4, ncols=4, sharex=False, sharey=False, figsize=(20,20))

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][2], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax1, edgecolor='black')
ax1.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][12], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax2, edgecolor='black')
ax2.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][13], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax3, edgecolor='black')
ax3.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][3], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax4, edgecolor='black')
ax4.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][7], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax5, edgecolor='black')
ax5.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][8], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax6, edgecolor='black')
ax6.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][6], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax7, edgecolor='black')
ax7.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][1], y=Run_settings["Elements_plotted"][5], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax8, edgecolor='black')
ax8.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][0], y=Run_settings["Elements_plotted"][9], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax9, edgecolor='black')
ax9.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][0], y=Run_settings["Elements_plotted"][4], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax10, edgecolor='black')
ax10.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][0], y=Run_settings["Elements_plotted"][14], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax11, edgecolor='black')
ax11.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][0], y=Run_settings["Elements_plotted"][10], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax12, edgecolor='black')
ax12.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][2], y=Run_settings["Elements_plotted"][12], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax13, edgecolor='black')
ax13.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][2], y=Run_settings["Elements_plotted"][16], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax14, edgecolor='black')
ax14.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][3], y=Run_settings["Elements_plotted"][15], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax15, edgecolor='black')
ax15.legend([])

sns.scatterplot(x=Run_settings["Elements_plotted"][3], y=Run_settings["Elements_plotted"][17], hue=Run_settings["RockClassification"],data=coredata, palette=chemofacies_color,ax=ax16, edgecolor='black')
ax16.legend([])

plt.savefig(os.path.join(dirName + '/' + Run_settings["Lease_Name"] + '_' + Formation_names + '_CrossPlot_' + Run_settings["RockClassification"] + '.png'),dpi = 300)
#plt.savefig(os.path.join(dirName + '/' + Run_settings["Lease_Name"] + '_' + Formation_names + '_CrossPlot_' + Run_settings["RockClassification"] + '.eps'),format='eps',dpi = 600)


##### Plot 2 plotted with respect to depth

n=7

fig, axs = plt.subplots(nrows=1, ncols=n, figsize=(15,15),sharey=True)

plt.subplot(1, n, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[Run_settings["RockClassification"]][i]+2, coredata[Run_settings["RockClassification"]][i]+2]
    Z = [coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"]]
       
    plt.fill(Q, Z,c=chemofacies_color[coredata[Run_settings["RockClassification"]][i]], linewidth=0.0)
    plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
    plt.xlim((0,6))
    #plt.xlabel(Run_settings["RockClassification"], fontsize=18)
    plt.xlabel('Rockclass_NN', fontsize=18)
    plt.ylabel(Run_settings["Depth_model"], fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)  
    #plt.ylim(10892,10820)

plt.subplot(1,n,2)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_Depth"][0]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,1])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Run_settings["Elements_Depth"][0], fontsize=18)
plt.xlabel(os.path.join(Run_settings["Elements_Depth"][0]), fontsize=18)

    
#plt.ylim(10892,10820)
plt.subplot(1, n, 3)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_Depth"][1]]/coredata[Run_settings["Elements_Depth"][0]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.xlim([0,75])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.yticks([])
plt.xticks(fontsize=14)
#plt.xscale('log')
plt.xlabel(Run_settings["Elements_plotted"][3], fontsize=18)
plt.xlabel('Sr/Ca', fontsize=18)

#plt.ylim(10892,10820)
plt.subplot(1,n, 4)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_Depth"][2]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.xlim([0,200])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel('Mn', fontsize=18)

#plt.ylim(10892,10820)
plt.subplot(1, n, 5)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_Depth"][3]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,200])
#plt.yticks([])
#plt.xscale('log')
plt.xticks(fontsize=14)

plt.xlabel('Al', fontsize=18)

#plt.ylim(10892,10820)
plt.subplot(1,n,6)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_Depth"][4]]/coredata[Run_settings["Elements_Depth"][3]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.xlim([0,75])
#plt.yticks([])
#plt.xscale('log')
plt.xticks(fontsize=14)

plt.xlabel('Mo/Al', fontsize=18)
#plt.ylim(10892,10820)

plt.subplot(1,n,7)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_Depth"][5]]/coredata[Run_settings["Elements_Depth"][3]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.xlim([0,75])
#plt.yticks([])
#plt.xscale('log')
plt.xticks(fontsize=14)

plt.xlabel('Ni/Al', fontsize=18)
#plt.ylim(10892,10820)


plt.savefig(os.path.join(dirName + '/' + Run_settings["Lease_Name"] + '_' + Formation_names + '_Elementlog_' + Run_settings["RockClassification"] + '.png'),dpi = 300)
plt.savefig(os.path.join(dirName + '/' + Run_settings["Lease_Name"] + '_' + Formation_names + '_Elementlog_' + Run_settings["RockClassification"] + '.eps'),format='eps', dpi = 600)


 
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

plt.savefig(os.path.join(dirName + '/' + Run_settings["Lease_Name"] + '_' + Formation_names + '_PieChart_' + Run_settings["RockClassification"] + '.png'),dpi = 300)
#plt.savefig(os.path.join(dirName + '/' + Run_settings["Lease_Name"] + '_' + Formation_names + '_PieChart_' + Run_settings["RockClassification"] + '.eps'),format='eps', dpi = 600)


fig, axs = plt.subplots(nrows=1, ncols=1)
plt.subplot(1, 1, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[Run_settings["RockClassification"]][i]+2, coredata[Run_settings["RockClassification"]][i]+2]
    Z = [coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"]]
         
    plt.fill(Q, Z,c=chemofacies_color[coredata[Run_settings["RockClassification"]][i]], linewidth=0.0)
    plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
    plt.xlim((0,6))
    plt.yticks([])
    plt.xticks([])
    
    
    
    
    
bottom_core = str(round(max(coredata[Run_settings["Depth_model"]])))
top_core = str(round(min(coredata[Run_settings["Depth_model"]])))
plt.tight_layout()
plt.savefig(os.path.join(Root_path + '/CoreOutput/CrossSection/' + Formation_names + '/'  + Run_settings["Lease_Name"] + '_' + Formation_names +  '_' + top_core + '_' + bottom_core + '_' + '.png'),dpi = 600)
