import numpy as np
import matplotlib.pyplot as plt
import pandas as pd #dataframe features
import seaborn as sns
import pickle
import os
import settings
import math
#import scipy.signal

WellLogs_plotted=['GR','NPHI','ILD','SFL','SP'] #Lloyd Hurt
attribute_plotted=['Carbonates','TECTOSILICATES','TotalClay','TOC_percent'] #LloydHurt


Elements_plotted=['Al','Ca','Si','Fe','Mg','Sr','V','Mo','Ni','Cu','Ti','Zr']
attribute_plotted=['TOC','HI'] #Stewart

wirelineimport  = os.path.join(settings.output_dir,settings.corename + '_' + settings.Formation_names + '_' + 'Wireline_NeuralModel' + settings.suffix)
wirelineimport  = os.path.join(settings.output_dir,settings.corename + '_' + settings.Formation_names + '_' + 'LAS' + settings.suffix)
wirelinedata=pd.read_csv(wirelineimport).sort_values(['DEPT']).reset_index(drop=True)

moving_avg=6

infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()


dataimport  = os.path.join(settings.output_dir,settings.corename + '_' + settings.Formation_names + '_' + 'NeuralModel' + settings.suffix)
coredata=pd.read_csv(dataimport)
coredata = coredata.sort_values([settings.Depth_model])


attributeimport  = os.path.join(settings.output_dir,settings.corename + '_' + settings.Formation_names + '_' + 'Attribute_NeuralModel' + settings.suffix)
attributedata=pd.read_csv(attributeimport)
attributedata = attributedata.sort_values([settings.Depth_model])
#coredata=attributedata

sns.set_style('white')

##### This section collected the descriptive statistics for each chemofacies based on 'attribute_plotted' array. Then adds columns that are renamed
Q=attributedata.groupby("Chemofacies_NN").median()[attribute_plotted]
QQ=attributedata.groupby("Chemofacies_NN").std().count()
QQQ=attributedata.groupby("Chemofacies_NN").count()

for i in range(len(attribute_plotted)):
   Q=Q.rename(columns={attribute_plotted[i]:os.path.join(attribute_plotted[i] + '_median')})

attributedata = pd.merge(attributedata, Q, left_on='Chemofacies_NN',right_index=True,)
attributedata = attributedata.sort_values([settings.Depth_model])



#attributedata.to_csv  (os.path.join(settings.output_dir,settings.corename + '_' + settings.Formation_names + 'TOC'+ settings.suffix))
#attributeimport  = os.path.join(settings.output_dir,settings.corename + '_' + settings.Formation_names + 'TOC'+ settings.suffix)
#attributedata=pd.read_csv(attributeimport)
#attributedata = attributedata.sort_values([settings.Depth_model])
#coredata=attributedata

## This computes the running average and also prints the colums to coredata for export to TecLog
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


fig, axs = plt.subplots(nrows=1, ncols=6, figsize=(15,15),sharey=True)

plt.subplot(1, 7, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[settings.RockClassification][i], coredata[settings.RockClassification][i]]
    Z = [coredata[settings.Depth_model][i]+settings.XRF_resolution, coredata[settings.Depth_model][i], coredata[settings.Depth_model][i], coredata[settings.Depth_model][i]+settings.XRF_resolution]
   
    
    plt.fill(Q, Z,c=chemofacies_color[coredata[settings.RockClassification][i]], linewidth=0.0)
    plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
    plt.xlim((0,6))
    plt.xlabel("RockClass", fontsize=18)
    plt.ylabel(settings.Depth_model, fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)  
    
    
plt.subplot(1, 7,2)
axs=plt.plot(wirelinedata[WellLogs_plotted[1]],wirelinedata.DEPT, color='blue')
#axs=sns.scatterplot(attribute_plotted[], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
#axs=plt.plot(wirelinedata[WellLogs_plotted[6]],wirelinedata.DEPT, color='red',linestyle='--', linewidth=0.5)
plt.yticks([])
#plt.xscale("log")
plt.xticks(fontsize=14)
#plt.xscale('log')
plt.xlabel(WellLogs_plotted[1], fontsize=18)
plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
#axs.legend([])
plt.xlim(0,150)
#plt.ylim(2901,2877)

plt.subplot(1, 7, 3)
axs=plt.plot(wirelinedata[WellLogs_plotted[4]],wirelinedata.DEPT, color='blue')

#axs=plt.plot(wirelinedata[WellLogs_plotted[3]],wirelinedata.DEPT, color='red')
#axs=sns.scatterplot(attribute_plotted[6], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
plt.yticks([])
#axs.legend([])

plt.xticks(fontsize=14)
plt.xlabel(WellLogs_plotted[4], fontsize=18)
plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
plt.xlim(0.35,-0.15)
#plt.ylim(2901,2877)

plt.subplot(1, 7, 4)
axs=plt.plot(wirelinedata[WellLogs_plotted[2]],wirelinedata.DEPT, color='blue')

#axs=plt.plot(wirelinedata[WellLogs_plotted[3]],wirelinedata.DEPT, color='red')
#axs=sns.scatterplot(attribute_plotted[6], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
plt.yticks([])
#axs.legend([])

plt.xticks(fontsize=14)
plt.xlabel(WellLogs_plotted[2], fontsize=18)
plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
plt.xlim(0,1000)
#plt.xscale("log")
#plt.ylim(2901,2877)

plt.subplot(1, 7,5)
axs=plt.plot(wirelinedata[WellLogs_plotted[3]],wirelinedata.DEPT, color='blue')

#axs=plt.plot(wirelinedata[WellLogs_plotted[3]],wirelinedata.DEPT, color='red')
#axs=sns.scatterplot(attribute_plotted[6], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
plt.yticks([])
#axs.legend([])

plt.xticks(fontsize=14)
plt.xlabel(WellLogs_plotted[3], fontsize=18)
plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
plt.xlim(2.25,2.75)
#plt.xscale("log")
#plt.ylim(2901,2877)           
 
plt.subplot(1,7,6)
axs=sns.scatterplot(attribute_plotted[0], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
axs.legend([])
y_av = movingaverage(attributedata.TOC_median, moving_avg)

axs=plt.plot(y_av,attributedata[settings.Depth_model], color='blue', linewidth=1)
#plt.xlim([0,50])
plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(attribute_plotted[0], fontsize=18)
    
#'Carbonates','TECTOSILICATES','TotalClay','TOC_percent'

plt.subplot(1,7,7)
axs=sns.scatterplot(attribute_plotted[1], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
axs.legend([])
y_av = movingaverage(attributedata.HI_median, moving_avg)
#y_av = movingaverage(coredata[Elements_plotted[4]], moving_avg)
axs=plt.plot(y_av,attributedata[settings.Depth_model], color='blue', linewidth=1)
#plt.xlim([0,50])
plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
plt.yticks([])
plt.xticks(fontsize=14)
#plt.xlabel('GR&RES', fontsize=18)
#plt.xlabel(os.path.join(Elements_plotted[4]), fontsize=18)

plt.xlabel(attribute_plotted[1], fontsize=18)

plt.subplot(1, 7,7)
#axs=sns.scatterplot(attribute_plotted[2], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
#axs=plt.plot(wirelinedata[WellLogs_plotted[3]],wirelinedata.DEPT, color='red')
#y_av = movingaverage(attributedata.TotalClay_median, moving_avg)
#axs=plt.plot(y_av,attributedata[settings.Depth_model], color='blue', linewidth=1)

#y_av = movingaverage(attributedata.Porosity_Ambient_median, moving_avg)
#axs=plt.plot(y_av,coredata[settings.Depth_model], color='blue', linewidth=1)
#plt.xlim([0,50])
#plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
#plt.yticks([])
#plt.xticks(fontsize=14)
#plt.xlabel(attribute_plotted[2], fontsize=18)
#plt.xlabel(os.path.join(Elements_plotted[7]+'/'+Elements_plotted[0]), fontsize=18)

#plt.subplot(1, 7, 7)
#axs=sns.scatterplot(attributedata[attribute_plotted[3]], settings.Depth_model, data=attributedata,hue=settings.RockClassification, palette=chemofacies_color)
#axs.legend([])
#y_av = movingaverage(attributedata.TOC_percent_median, moving_avg)
#axs=plt.plot(wirelinedata[WellLogs_plotted[2]],wirelinedata.DEPT, color='red')

#plt.ylim((max(coredata[settings.Depth_model]),min(coredata[settings.Depth_model])))
##plt.yticks([])
#plt.xticks(fontsize=14)
#plt.xlabel(os.path.join(attribute_plotted[3]), fontsize=18)
#plt.xlabel(os.path.join(Elements_plotted[6]+'/'+Elements_plotted[0]), fontsize=18)
#plt.xlim([0,50])



plt.savefig(settings.output_dir + "/" + settings.corename + '_' + settings.Formation_names + '_' + 'Attribute_Log' + '.png',dpi = 300)


fig, (ax1,ax2) = plt.subplots(ncols=2, figsize=(10,5))
#sns.boxplot(x=settings.RockClassification, y=attribute_plotted[0], hue=settings.RockClassification, palette=chemofacies_color, data=attributedata,ax=ax1,width=3.5)
#sns.boxplot(x=settings.RockClassification, y=attribute_plotted[1], hue=settings.RockClassification, palette=chemofacies_color, data=attributedata,ax=ax2,width=3.5)#, width = 3.5)
#sns.boxplot(x=settings.RockClassification, y=attribute_plotted[2], hue=settings.RockClassification, palette=chemofacies_color, data=attributedata,ax=ax3)#, width = 3.5)
#sns.boxplot(x=settings.RockClassification, y=attribute_plotted[3], hue=settings.RockClassification, palette=chemofacies_color, data=attributedata,ax=ax4)#, width = 3.5)
#sns.boxplot(x=settings.RockClassification, y=attribute_plotted[4], hue=settings.RockClassification, palette=chemofacies_color, data=attributedata,ax=ax5)
#sns.boxplot(x=settings.RockClassification, y=attribute_plotted[5], hue=settings.RockClassification, palette=chemofacies_color, data=attributedata,ax=ax6)

#ax1.legend([])
#ax2.legend([])

sns.boxplot( x=settings.RockClassification, y=attribute_plotted[0],data=attributedata,palette=chemofacies_color,ax=ax1);
sns.boxplot( x=settings.RockClassification, y=attribute_plotted[1],data=attributedata,palette=chemofacies_color,ax=ax2);

#plt.show()
plt.savefig(settings.output_dir + "/" + settings.corename + '_' + settings.Formation_names + '_' + 'Attribute_boxplot' + '.png',dpi = 300)

#ax6.legend([])
fig.tight_layout()
plt.savefig(settings.output_dir + "/" + settings.corename + '_' + settings.Formation_names + '_' + 'Attribute_boxplot' + '.png',dpi = 300)

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10,5),sharey=True)
plt.subplot(1, 2, 1)
#axs=sns.scatterplot(attribute_plotted[10], attribute_plotted[9], data=attributedata,hue='Formation_2', edgecolor='black')
#plt.legend([])
plt.xlim([0,200])
plt.ylim([0,1000])

plt.subplot(1, 2, 2)
#axs=sns.scatterplot(attribute_plotted[10], attribute_plotted[9], data=attributedata,hue=settings.RockClassification, palette=chemofacies_color,edgecolor='black')

#plt.legend([])
plt.xlim([0,200])
plt.ylim([0,1000])

#plt.savefig(settings.output_dir + "/" + settings.corename + '_' + settings.Formation_names + '_' + 'VanKrevelen' + settings.imagesuffix,dpi = 300)


attributedata.groupby('Chemofacies_NN')['TOC_percent'].describe()
#attributedata.groupby('Chemofacies_NN')['DS_GrainDensity'].describe()
#attributedata.groupby('Chemofacies_NN')['Formation_2'].describe()

