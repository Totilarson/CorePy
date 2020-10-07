#==========================================
# Title:  PCAchemofacies.py
# Author: Toti Larson & Esben Pedersen
# Date:   09/16/2020
# Description:  PCAchemofacies.py is run after initialization via settings.py and is where chemofacies analysis is performed
# Version: 1.0
# Output files: 1) One  .csv file that adds two columns to the original XRF data file (Outliers, and Chemofacies)
#               2) Three .png files that show the PCA variance, a biplot, and a scatter plot showing the analytical outliers 
#   Changelog:
#==========================================

# Import libraries and dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd #dataframe features
import seaborn as sns
import os
import settings
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.patheffects as PathEffects

dataimport = os.path.join(settings.coredata_dir,settings.corename + settings.suffix)
coredata = pd.read_csv(dataimport)
LODT5 = pd.read_csv(settings.LOD_T5)

#Sort coredata by depth and select Formation of interest
if settings.Formation != ['all']:
    coredata = coredata[coredata['Formation'].apply(lambda x: any(s in x[:len(s)] for s in settings.Formation))]
coredata.sort_values(by=[settings.Depth_model]) #sorts coredata by depth

#Add LOD to the xrf dataset and identify outliers 
coredata[settings.elements]=np.maximum(coredata[settings.elements],LODT5[settings.elements]) #add LOD to each element
Element_outlier=(coredata[settings.elements]).mean()+settings.outlier_multiplier*(coredata[settings.elements]).std()
coredata['Outliers']=((coredata[settings.elements])>Element_outlier).any(axis='columns')

X=(coredata[coredata['Outliers'] == False]) #excludes outliers

scaler = StandardScaler() #create a standard scaler object
pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
scaler.fit(X[settings.elements].values)
x_new = pca.fit_transform(scaler.transform(X[settings.elements].values)) #
features= np.arange(len(settings.elements))

#plot the variance captured by principal components.
fig, ((ax4, ax5)) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(10,5))
plt.subplot(1, 2, 1)

plt.plot(pca.explained_variance_ratio_.cumsum(),marker='o',linestyle='--', color = "black")
plt.ylabel('Cumulative explained variance')
plt.xlabel('Principle components')
plt.axhline(y=0.75, color='red', linestyle = '--')
plt.subplot(1, 2, 2)
plt.bar(features,pca.explained_variance_ratio_, color='black')
plt.xlabel('Principle components')
plt.ylabel('variance %')
plt.tight_layout()
plt.savefig(settings.output_dir + "/" + settings.corename + '_' + settings.Formation_names + '_' + 'Variance' + settings.imagesuffix,dpi = 300)

# K-means cluster analysis
x_cluster = x_new[:, np.arange(settings.Principal_components)] #PCs used in clustering

kmeans = KMeans(n_clusters=settings.clusters) #select the number of clusters
kmeans.fit(x_cluster) #results from PCA
Chemofacies = kmeans.predict(x_cluster)+1 #arrayt of the chemofacies classification for each row
X['Chemofacies']=Chemofacies #makes a new column based on above conditional format

#scaling used for plotting
xs = x_new[:,settings.PCA1]
ys = x_new[:,settings.PCA2]
scalex = 1.0/(xs.max() - xs.min())
scaley = 1.0/(ys.max() - ys.min())

fig, (ax1) = plt.subplots(ncols=1, figsize=(7,5))
unique=np.arange(settings.clusters)+1
palette = dict(zip(unique, sns.color_palette()))

sns.scatterplot(x_cluster[:,settings.PCA1]*scalex, x_cluster[:, settings.PCA2]*scaley, hue=Chemofacies, s=30,palette=palette,ax=ax1,edgecolor='black', zorder=5)
centers = kmeans.cluster_centers_
sns.scatterplot(centers[:, settings.PCA1]*scalex, centers[:,settings.PCA2]*scaley,marker="x",s=200,facecolor="black", ax=ax1, linewidth = 2, edgecolor='black',zorder=7);

n = pca.components_.shape[0]
for i in range(n):
    arrow_style = dict(arrowstyle = "-|>", color = 'k', shrinkA = 0, shrinkB = 0, lw = 0.5, ls = '-')
    plt.annotate('', xy = (pca.components_[0,i] * 1.5, pca.components_[1,i] * 1.5), xytext = (0,0), arrowprops = arrow_style)
    txt_style = plt.text(pca.components_[0,i] * 1.6, pca.components_[1,i] * 1.6, settings.elements[i], color = 'w', ha = 'center', va = 'center', zorder = 10)
    txt_style.set_path_effects([PathEffects.withStroke(linewidth = 1, foreground = 'black')])

    plt.xlim(-0.6,0.8)
    plt.ylim(-0.6,0.8)
    plt.axhline(y=0, color='gray', linestyle = '--', alpha = 0.5, zorder = 1)
    plt.axvline(x=0, color='gray', linestyle = '--', alpha = 0.5, zorder = 1)
    plt.xlabel("PC{}".format(settings.PCA1+1))
    plt.ylabel("PC{}".format(settings.PCA2+1))
    plt.grid(zorder=0)

plt.savefig(settings.output_dir + "/" + settings.corename + '_' + settings.Formation_names + '_' + 'Biplot' + settings.imagesuffix,dpi = 300)

 
# Y turns an analytical outlier into a chemofacies that is one greater than the maximum number of chemofacies through K-means
Y=(coredata[coredata['Outliers'] == True])
Y["Chemofacies"] =max(X.Chemofacies)+1

# Z concats X (dataframe used in PCA that excludes outliers) and Y(dataframe of analytical outliers)
# Z gets written as a .csv file in an export folder. Basically adds "Outliers" and "Chemofacies" to the original datafile
Z=pd.concat([X, Y], ignore_index=True)
Z.to_csv (os.path.join(settings.output_dir,settings.corename + '_' + settings.Formation_names + settings.suffix))

#visualization of the outliers. I chose Al vs. Si and Ca vs. Sr. 
fig, (ax1,ax2) = plt.subplots(ncols=2, figsize=(10,5))
sns.scatterplot(x="Al", y="Si", hue="Outliers",data=coredata,ax=ax1, edgecolor='black')
sns.scatterplot(x="Ca", y="Sr", hue="Outliers",data=coredata,ax=ax2, edgecolor='black')
plt.tight_layout()
plt.savefig(settings.output_dir + "/" + settings.corename + '_' + settings.Formation_names + '_' + 'outliers' + settings.imagesuffix,dpi = 300)
