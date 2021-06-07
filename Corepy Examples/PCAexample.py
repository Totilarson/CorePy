import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
#from sklearn.preprocessing import StandardScaler
#from sklearn.decomposition import PCA
import numpy as np
import matplotlib.patheffects as PathEffects


## User defined variables - start

# Data that is specific to the core XRF data stored in the  //CoreData/CoreXRF
corename = 'Public' #core name being studied

Formation = ['Eagle Ford'] # Filter the Formation column by specific formations
Formation_2=[] # This function is not built in yet, but can be used to sample members within a formation 
Formation_names = '-'.join(Formation+Formation_2) # this is used to make the directory specific to the formations


# depending on the clustering approach there will be different categories. Here, Chemofacies_PCA is a column output in the ouut .csv file
RockClassification = 'Chemofacies_PCA' # A column in the output .csv file will have this title
Depth_model='Depth_calculated'# 'XRF_adjusted_depth' and 'Wireline_Depth' are options in the data file. 


# Principal component analysis and K-means clusters variables
# the elements being evaluated can be changed. 29 are listed here. They can be removed if necessary
elements =  ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Ti','Mn', 'Fe', 'Ba', 'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'As', 'Pb', 
             'Th', 'Rb', 'U', 'Sr', 'Y', 'Zr', 'Nb', 'Mo']
outlier_multiplier = 4 ## outlier_multiplier refers to how many standard deviations away from mean are included as outliers
clusters = 4 ## clusters refers to the number of K-means clusters to be used
Principal_components = 4 ## Principal_components refers to the number (n) of principal components applied to K-means clustering algorithm (zero through n)

# For plotting purposes PC1 and PC2 are used to plot PCA results and also add two columns onto the output .csv datafile
PC1=0
PC2=1


# Colorscheme helps keep a consistent color pattern across all plots
ColorScheme=[1,     2,      3,    4,    5,      6,     7,     8,   9 , 10 ] 
#           blue, orange, green, red, purple, brown, pink, grey, gold, teal


# plotting variable. These can be changed depending on interest. 
Elements_plotted=['Ca','Al','Si','K','Mg','Mo','V','Ni']
moving_avg=3 # used to smooth out high resolution data
XRF_resolution=2/12 # used to build chemofacies stacking pattern. 2/12 refers to 2" xrf scanning resolution


## This section runs all necessary functions in CorePy

corepy.MakeXRFdf(corename,elements,outlier_multiplier,Depth_model,Formation_names)
coredata=corepy.MakeXRFdf(corename,elements,outlier_multiplier,Depth_model,Formation_names)

corepy.Remove_outliers(coredata)
corepy.Include_outliers(coredata)

coredata_no_outliers=corepy.Remove_outliers(coredata)
coredata_outliers=corepy.Include_outliers(coredata)
x_new=corepy.PCA_analysis(coredata_no_outliers,elements) # matrix of principal components
coredata_no_outliers=corepy.Kmeans_cluster(x_new,coredata_no_outliers,Principal_components, clusters,PC1,PC2)
coredata_outliers["Chemofacies_PCA"] = max(coredata_no_outliers.Chemofacies_PCA)+1
dirName=corepy.RootDir(corename, Formation_names)  
coredata=corepy.WriteCSV(coredata_no_outliers,coredata_outliers,dirName,corename,Formation_names,Depth_model)

pca_explained=corepy.PCA_explained(coredata_no_outliers,elements)

PCA_elbow=corepy.Elbow_method(x_new,Principal_components)

pca_vectors=corepy.PCA_matrix_elements(coredata_no_outliers,elements)


## I need to fix this color selection part
corepy.ColorPalette(ColorScheme) 
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

fig, ((ax1, ax2, ax3)) = plt.subplots(nrows=1, ncols=3, figsize=(15,5)) #sharex=True, sharey=True,
plt.subplot(1,3, 1)

plt.plot(pca_explained,marker='o',linestyle='--', color = "black")
plt.ylabel('Cumulative explained variance')
plt.xlabel('Principle components')
plt.axhline(y=0.75, color='red', linestyle = '--')
#plt.ylim(0,1) 

plt.subplot(1, 3, 2)

K = range(1,15) # range of K-means clusters evaluated
plt.plot(K, PCA_elbow, 'bx-')
plt.xlabel('k-means clusters')
plt.ylabel('Distortion')

plt.subplot(1, 3, 3)
unique=np.arange(clusters)+1
palette = dict(zip(unique, sns.color_palette()))

xs = x_new[:,PC1]
ys = x_new[:,PC2]
scalex = 1.0/(xs.max() - xs.min())
scaley = 1.0/(ys.max() - ys.min())


sns.scatterplot(coredata_no_outliers.PCA1*scalex, coredata_no_outliers.PCA2*scaley, hue=coredata_no_outliers.Chemofacies_PCA, s=30,palette=palette,edgecolor='black', zorder=1, legend=False)

n = pca_vectors.shape[0]
for i in range(n):
   arrow_style = dict(arrowstyle = "-|>", color = 'k', shrinkA = 0, shrinkB = 0, lw = 1, ls = '-')
   plt.annotate('', xy = (pca_vectors[PC1,i] * 1, pca_vectors[PC2,i] * 1), xytext = (0,0), arrowprops = arrow_style, zorder = 2)
   txt_style = plt.text(pca_vectors[PC1,i] * 1.1, pca_vectors[PC2,i] * 1.1, elements[i], color = 'w', ha = 'center', va = 'center', zorder = 3)
   txt_style.set_path_effects([PathEffects.withStroke(linewidth = 2, foreground = 'black')])
   plt.xlabel("PC{}".format(PC1+1))
   plt.ylabel("PC{}".format(PC2+1))
plt.savefig(os.path.join(dirName + '/' + corename + '_' + Formation_names + '_PCA' + '.png'),dpi = 300)


## Plots made to evaluate chemofacies results 
fig, ((ax1, ax2,), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False, figsize=(10,10))

sns.scatterplot(x=Elements_plotted[0], y=Elements_plotted[2], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax1, edgecolor='black')
ax1.legend([])

sns.scatterplot(x=Elements_plotted[0], y=Elements_plotted[3], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax2, edgecolor='black')
ax2.legend([])

sns.scatterplot(x=Elements_plotted[1], y=Elements_plotted[4], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax3, edgecolor='black')
ax3.legend([])

sns.scatterplot(x=Elements_plotted[0], y=Elements_plotted[5], hue=RockClassification,data=coredata, palette=chemofacies_color,ax=ax4, edgecolor='black')
ax4.legend([])

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

plt.subplot(1,9, 4)
y_av = corepy.movingaverage(coredata[Elements_plotted[2]], moving_avg)
axs=plt.plot(y_av,coredata[Depth_model], color='blue')
#plt.xlim([0,10])
plt.ylim((max(coredata[Depth_model]),min(coredata[Depth_model])))
plt.yticks([])
plt.xticks(fontsize=14)
plt.xlabel(Elements_plotted[2], fontsize=18)


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