##PCAexample.py lists the inputs used in all the functions stored under corepy
##

import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepy


## User defined variables - start

# Data that is specific to the core XRF data stored in the  //CoreData/CoreXRF
corename = 'Public' #core name being studied

Formation = ['Eagle Ford'] # List of strings. Filters the formation of investigation # List of strings. Filters the formation of investigation
Formation_2=[]
Formation_names = '-'.join(Formation+Formation_2) #this is used to make the directory specific to the formations

# depending on the clustering approach there will be different categories. Here, Chemofacies_PCA is a column output in the ouut .csv file
RockClassification = 'Chemofacies_PCA'
Depth_model='Depth_calculated'# 'XRF_adjusted_depth' and 'Wireline_Depth' are options in the data file. 


# the elements being evaluated can be changed. 29 are listed here. They can be removed if necessary
elements =  ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'As', 'Pb', 
             'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']


#statistics variables
outlier_multiplier = 4      # how many standard deviations away from mean are included as outliers
clusters = 4                # number of K-means clusters to be used

# number of principal components applied to K-means clustering algorithm. 
Principal_components =4     # The number can range from 1 to maximum number of elements. 


# Colorscheme helps keep a consistent color pattern across all plots
ColorScheme=[1,     2,      3,    4,    5,      6,     7,     8,   9 , 10 ] 
#           blue, orange, green, red, purple, brown, pink, grey, gold, teal


# plotting variable. These can be changed depending on interest. 
Elements_plotted=['Ca','Al','Si','Ni','Cu','Zn','U','Mo','V','Sr']
moving_avg=3 # used to smooth out high resolution data
XRF_resolution=2/12 # used to build chemofacies stacking pattern. 2/12 refers to 2" xrf scanning resolution


## runs all necessary functions in CorePy
corepy.RootDir(corename, Formation_names)
corepy.MakeXRFdf(corename,elements,outlier_multiplier,Depth_model)
coredata=corepy.MakeXRFdf(corename,elements,outlier_multiplier,Depth_model)

corepy.Remove_outliers(coredata)
corepy.Include_outliers(coredata)

X=corepy.Remove_outliers(coredata)
Y=corepy.Include_outliers(coredata)
x_new=corepy.PCA_analysis(X,elements) # matrix of principal components
X=corepy.Kmeans_cluster(x_new,X,Principal_components, clusters)
Y["Chemofacies_PCA"] = max(X.Chemofacies_PCA)+1
dirName=corepy.RootDir(corename, Formation_names)  
coredata=corepy.WriteCSV(X,Y,dirName,corename,Formation_names,Depth_model)


## I need to fix this color selection part
corepy.ColorPalette(ColorScheme) 
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  



## Plots made to evaluate chemofacies results 
fig, ((ax1, ax2,), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False, figsize=(10,10))

sns.scatterplot(x=elements[2], y=elements[3], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax1, edgecolor='black')
ax1.legend([])

sns.scatterplot(x=elements[2], y=elements[6], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax2, edgecolor='black')
ax2.legend([])

sns.scatterplot(x=elements[7], y=elements[1], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax3, edgecolor='black')
ax3.legend([])

sns.scatterplot(x=elements[2], y=elements[28], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax4, edgecolor='black')
ax4.legend([])
# 3 and 15 for Ni Si.    2 and 28 for Mo vs Al     7 and 24 for Sr and Ca. 

plt.savefig(os.path.join(dirName + '/' + corename + '_' + Formation_names + '_CrossPlot' + '.png'),dpi = 300)



##### Plot 2 plotted with respect to depth

fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(15,15),sharey=True)

plt.subplot(1, 9, 1)
for i in range(len(coredata)):
    Q = [0, 0, coredata[RockClassification][i], coredata[RockClassification][i]]
    
    Z = [coredata[Depth_model][i]+XRF_resolution, coredata[Depth_model][i], coredata[Depth_model][i], coredata[Depth_model][i]+XRF_resolution]
   
    
    plt.fill(Q, Z,c=chemofacies_color[coredata[RockClassification][i]], linewidth=0.0)
    plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
    plt.xlim((0,6))
    plt.xlabel("RockClass", fontsize=18)
    plt.ylabel(Depth_model, fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)  
    
    
plt.subplot(1,9,2)
y_av = corepy.movingaverage(coredata[Elements_plotted[0]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
#plt.xlim([25,40])
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[0], fontsize=18)
plt.xlabel(os.path.join(Elements_plotted[0]), fontsize=18)
    

plt.subplot(1, 9, 3)
y_av = corepy.movingaverage(coredata[Elements_plotted[1]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[1], fontsize=18)
#plt.xlabel(os.path.join(Elements_plotted[1]), fontsize=18)

plt.subplot(1,9, 4)
y_av = corepy.movingaverage(coredata[Elements_plotted[2]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[2], fontsize=18)
#plt.xlabel(os.path.join(Elements_plotted[1]), fontsize=18)


plt.subplot(1, 9, 5)
y_av = corepy.movingaverage(coredata[Elements_plotted[3]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
#plt.xlim([0,175])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[3], fontsize=18)

plt.subplot(1,9,6)
y_av = corepy.movingaverage(coredata[Elements_plotted[4]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
#plt.xlim([0,250])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[4], fontsize=18)

plt.subplot(1, 9, 7)
y_av = corepy.movingaverage(coredata[Elements_plotted[5]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
#plt.xlim([0,250])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[5], fontsize=18)

plt.subplot(1,9,8)
y_av = corepy.movingaverage(coredata[Elements_plotted[6]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
#plt.xlim([0,500])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[6], fontsize=18)

plt.subplot(1,9,9)
y_av = corepy.movingaverage(coredata[Elements_plotted[7]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
#plt.xlim([0,500])
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[7], fontsize=18)


plt.savefig(os.path.join(dirName + '/' + corename + '_' + Formation_names + '_Elementlog' + '.png'),dpi = 300)
