import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
import matplotlib.patheffects as PathEffects
import json


CoreOfStudy = 'LloydHurt'
Root_path = os.path.dirname(os.getcwd())
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  CoreOfStudy  +'.json')))

infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

Formation_names=corepy.Formation_names(Corebeta["Formation"],Corebeta["Formation_2"])
## This section runs all necessary functions in CorePy
corepy.RootDir(Corebeta["corename"], Formation_names)
corepy.MakeXRFdf(Corebeta["corename"],Corebeta["elements"],Corebeta["outlier_multiplier"],Corebeta["Depth_model"],Formation_names)
coredata=corepy.MakeXRFdf(Corebeta["corename"],Corebeta["elements"],Corebeta["outlier_multiplier"],Corebeta["Depth_model"],Formation_names)

corepy.Remove_outliers(coredata)
corepy.Include_outliers(coredata)

coredata_no_outliers=corepy.Remove_outliers(coredata)
coredata_outliers=corepy.Include_outliers(coredata)
x_new=corepy.PCA_analysis(coredata_no_outliers,Corebeta["elements"]) # matrix of principal components
coredata_no_outliers=corepy.Kmeans_cluster(x_new,coredata_no_outliers,Corebeta["Principal_components"], Corebeta["clusters"],Corebeta["PC1"],Corebeta["PC2"])
coredata_outliers["Chemofacies_PCA"] = max(coredata_no_outliers.Chemofacies_PCA)+1
dirName=corepy.RootDir(Corebeta["corename"], Formation_names)  
coredata=corepy.WriteCSV(coredata_no_outliers,coredata_outliers,dirName,Corebeta["corename"],Formation_names,Corebeta["Depth_model"])

pca_explained=corepy.PCA_explained(coredata_no_outliers,Corebeta["elements"])

PCA_elbow=corepy.Elbow_method(x_new,Corebeta["Principal_components"])

pca_vectors=corepy.PCA_matrix_elements(coredata_no_outliers,Corebeta["elements"])


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
#unique=np.arange(Corebeta["clusters"])+1
#palette = dict(zip(unique, sns.color_palette()))

xs = x_new[:,Corebeta["PC1"]]
ys = x_new[:,Corebeta["PC2"]]
scalex = 1.0/(xs.max() - xs.min())
scaley = 1.0/(ys.max() - ys.min())


sns.scatterplot(coredata_no_outliers.PCA1*scalex, coredata_no_outliers.PCA2*scaley, hue=coredata_no_outliers.Chemofacies_PCA, s=30,palette=chemofacies_color,edgecolor='black', zorder=1, legend=False)

n = pca_vectors.shape[0]
for i in range(n):
   arrow_style = dict(arrowstyle = "-|>", color = 'k', shrinkA = 0, shrinkB = 0, lw = 1, ls = '-')
   plt.annotate('', xy = (pca_vectors[Corebeta["PC1"],i] * 1, pca_vectors[Corebeta["PC2"],i] * 1), xytext = (0,0), arrowprops = arrow_style, zorder = 2)
   txt_style = plt.text(pca_vectors[Corebeta["PC1"],i] * 1.1, pca_vectors[Corebeta["PC2"],i] * 1.1, Corebeta["elements"][i], color = 'w', ha = 'center', va = 'center', zorder = 3)
   txt_style.set_path_effects([PathEffects.withStroke(linewidth = 2, foreground = 'black')])
   plt.xlabel("PC{}".format(Corebeta["PC1"]+1))
   plt.ylabel("PC{}".format(Corebeta["PC2"]+1))
plt.savefig(os.path.join(dirName + '/' + Corebeta["corename"] + '_' + Formation_names + '_PCA' + '.png'),dpi = 300)


