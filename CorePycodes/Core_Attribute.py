import numpy as np
import matplotlib.pyplot as plt
import pandas as pd #dataframe features
import seaborn as sns
import pickle
import os
import math
import corepytools as corepy
import json

Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))


Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

dirName=corepy.RootDir(Run_settings["CoreOfStudy"], Formation_names) 

infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

Formation_names = '-'.join(Run_settings["Formation"] + Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

# import the files with attributes
coredata = corepy.OutputXRF(Run_settings['CoreOfStudy'],Formation_names) # This directs to the output file

attributeimport  = (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Attribute.csv'))
attributedata=pd.read_csv(attributeimport)


# define the elements and attributes to be plotted
# default for this version is five attributes but upgrading to make this dynamic
attribute_plotted= Corebeta['Attribute_plotted']
Elements_plotted=Run_settings["Elements_plotted"]

fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(ncols=5, figsize=(30,5))
sns.boxplot(x=Run_settings["RockClassification"], y=attribute_plotted[0], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=attributedata,ax=ax1,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=attribute_plotted[1], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=attributedata,ax=ax2,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=attribute_plotted[2], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=attributedata,ax=ax3,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=attribute_plotted[3], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=attributedata,ax=ax4,dodge =False,width=0.75)
sns.boxplot(x=Run_settings["RockClassification"], y=attribute_plotted[4], hue=Run_settings["RockClassification"], palette=chemofacies_color, data=attributedata,ax=ax5,dodge =False,width=0.75)

ax1.legend([])
ax2.legend([])
ax3.legend([])
ax4.legend([])
ax5.legend([])

plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_AttributeBoxplot' + '.png'),dpi = 300)
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_AttributeBoxplot' + '.eps'),format='eps',dpi = 600)


# This section defines descriptive statistics for each chemofacies. Median, Q3, and Q1
Median_calc=attributedata.groupby(Run_settings["RockClassification"]).quantile(0.50)[attribute_plotted]
Q3_calc=attributedata.groupby(Run_settings["RockClassification"]).quantile(0.75)[attribute_plotted]
Q1_calc=attributedata.groupby(Run_settings["RockClassification"]).quantile(0.25)[attribute_plotted]


# loops through all atributes plotted to report the median, Q1 and Q3 value on each row based on chemofacies
for i in range(len(attribute_plotted)):

   Median_calc=Median_calc.rename(columns={attribute_plotted[i]:os.path.join(attribute_plotted[i] + '_median')})
   
   Q3_calc=Q3_calc.rename(columns={attribute_plotted[i]:os.path.join(attribute_plotted[i] + '_Q3')})

   Q1_calc=Q1_calc.rename(columns={attribute_plotted[i]:os.path.join(attribute_plotted[i] + '_Q1')})
   

#Attribute_corelog merges results from descriptive stats that is then written to a .csv file
Attribute_corelog = pd.merge(coredata, Median_calc, left_on=Run_settings["RockClassification"],right_index=True,)
Attribute_corelog = pd.merge(Attribute_corelog, Q3_calc, left_on=Run_settings["RockClassification"],right_index=True,)
Attribute_corelog = pd.merge(Attribute_corelog, Q1_calc, left_on=Run_settings["RockClassification"],right_index=True,)
Attribute_corelog = Attribute_corelog.sort_values([Run_settings['Depth_model']])

Attribute_corelog.to_csv (os.path.join(dirName + '/' +  Run_settings['CoreOfStudy'] + '_' + Formation_names + '_Attribute_statistics.csv'))



# plots attributes with respect to depth
n= 9

fig, axs = plt.subplots(nrows=1, ncols=n, figsize=(15,15),sharey=True)

coredata = Attribute_corelog # cheating here. Should rename throughout

plt.subplot(1, n, 1)
for i in range(len(Attribute_corelog)):
    Q = [0, 0, coredata[Run_settings["RockClassification"]][i]+2, coredata[Run_settings["RockClassification"]][i]+2]
    Z = [coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i], coredata[Run_settings["Depth_model"]][i]+Corebeta["XRF_resolution"]]
       
    plt.fill(Q, Z,c=chemofacies_color[coredata[Run_settings["RockClassification"]][i]], linewidth=0.0)
    plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
    plt.xlim((0,6))
    plt.xlabel("RockClass", fontsize=18)
    plt.ylabel(Run_settings["Depth_model"], fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    
    
plt.subplot(1, n, 2)
y_av = corepy.movingaverage(Attribute_corelog[Run_settings["Elements_plotted"][2]]/Attribute_corelog[Run_settings["Elements_plotted"][1]], Run_settings["moving_avg"])
axs=plt.plot(y_av,Attribute_corelog[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,10])
plt.ylim((max(Attribute_corelog[Run_settings["Depth_model"]]),min(Attribute_corelog[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
#plt.xscale('log')
plt.xlabel(Run_settings["Elements_plotted"][3], fontsize=18)
plt.xlabel('Si/Al', fontsize=18)

plt.subplot(1,n, 3)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][6]]/coredata[Run_settings["Elements_plotted"][2]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
#plt.xlim([0,0.02])
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
#plt.xscale('log')
plt.xlabel(Run_settings["Elements_plotted"][2], fontsize=18)
plt.xlabel('Mo/Al', fontsize=18)


plt.subplot(1, n, 4)
y_av = corepy.movingaverage(coredata[Run_settings["Elements_plotted"][8]]/coredata[Run_settings["Elements_plotted"][2]], Run_settings["moving_avg"])
axs=plt.plot(y_av,coredata[Run_settings["Depth_model"]], color='blue')
plt.ylim((max(coredata[Run_settings["Depth_model"]]),min(coredata[Run_settings["Depth_model"]])))
#plt.xlim([0,10])
plt.yticks([])
plt.xticks(fontsize=14)
#plt.xscale('log')
plt.xlabel(Run_settings["Elements_plotted"][1], fontsize=18)
plt.xlabel('Ni/Al', fontsize=18)
 
plt.subplot(1,n,5)
y_av = corepy.movingaverage(Attribute_corelog[(os.path.join(attribute_plotted[0]  + '_median'))], Run_settings["moving_avg"])
axs = sns.scatterplot(x=attribute_plotted[0] , y=Run_settings["Depth_model"], hue=Run_settings["RockClassification"],s=150, edgecolor='black',data = attributedata,palette=chemofacies_color) 
axs.legend([])
axs=plt.plot(y_av,Attribute_corelog[Run_settings["Depth_model"]], color='blue',linewidth=1.0)

#plt.xlim([0,30])
plt.ylim((max(Attribute_corelog[Run_settings["Depth_model"]]),min(Attribute_corelog[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(attribute_plotted[0], fontsize=18)
plt.ylabel('')


plt.subplot(1,n,6)
y_av = corepy.movingaverage(Attribute_corelog[(os.path.join(attribute_plotted[1]  + '_median'))], Run_settings["moving_avg"])
axs = sns.scatterplot(x=attribute_plotted[1] , y=Run_settings["Depth_model"], edgecolor='black',hue=Run_settings["RockClassification"], s=150,data = attributedata,palette=chemofacies_color) 
axs.legend([])
axs=plt.plot(y_av,Attribute_corelog[Run_settings["Depth_model"]], color='blue',linewidth=1.0)


plt.xlim([0,30])
plt.ylim((max(Attribute_corelog[Run_settings["Depth_model"]]),min(Attribute_corelog[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(attribute_plotted[1], fontsize=18)
plt.ylabel('')


plt.subplot(1,n,7)
y_av = corepy.movingaverage(Attribute_corelog[(os.path.join(attribute_plotted[2]  + '_median'))], Run_settings["moving_avg"])

axs=plt.plot(y_av,Attribute_corelog[Run_settings["Depth_model"]], color='blue',linewidth=1.0)
axs = sns.scatterplot(x=attribute_plotted[2] , y=Run_settings["Depth_model"],edgecolor='black', hue=Run_settings["RockClassification"],s=150, data = attributedata,palette=chemofacies_color) 
axs.legend([])

#plt.xlim([50,100])
plt.ylim((max(Attribute_corelog[Run_settings["Depth_model"]]),min(Attribute_corelog[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(attribute_plotted[2], fontsize=18)
plt.ylabel('')


plt.subplot(1,n,8)
y_av = corepy.movingaverage(Attribute_corelog[(os.path.join(attribute_plotted[3]  + '_median'))], Run_settings["moving_avg"])

axs = sns.scatterplot(x=attribute_plotted[3] , y=Run_settings["Depth_model"],edgecolor='black', hue=Run_settings["RockClassification"],s=150, data = attributedata,palette=chemofacies_color) 
axs.legend([])
axs=plt.plot(y_av,Attribute_corelog[Run_settings["Depth_model"]], color='blue',linewidth=1.0)

#plt.xlim([0,3])
plt.ylim((max(Attribute_corelog[Run_settings["Depth_model"]]),min(Attribute_corelog[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(attribute_plotted[3], fontsize=18)
plt.ylabel('')

plt.subplot(1,n,9)
y_av = corepy.movingaverage(Attribute_corelog[(os.path.join(attribute_plotted[4]  + '_median'))], Run_settings["moving_avg"])

axs = sns.scatterplot(x=attribute_plotted[4] , y=Run_settings["Depth_model"],edgecolor='black', hue=Run_settings["RockClassification"],s=150, data = attributedata,palette=chemofacies_color) 
axs.legend([])
axs=plt.plot(y_av,Attribute_corelog[Run_settings["Depth_model"]], color='blue',linewidth=1.0)

#plt.xlim([0,3])
plt.ylim((max(Attribute_corelog[Run_settings["Depth_model"]]),min(Attribute_corelog[Run_settings["Depth_model"]])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(attribute_plotted[4], fontsize=18)
plt.ylabel('')

plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Attributelog' + '.png'),dpi = 300)
plt.savefig(os.path.join(dirName + '/' + Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Attributelog' + '.eps'),format='eps',dpi = 600)