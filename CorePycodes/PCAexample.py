import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
import matplotlib.patheffects as PathEffects
import json
#import settings


#CoreOfStudy = 'Valcher'
#CoreOfStudy= Run_settings['CoreOfStudy']
Root_path = os.path.dirname(os.getcwd())

Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))


## I need to fix this color selection part
#corepy.ColorPalette(Corebeta['ColorScheme']) # I want to change color to json using chemofacies_color=json.load(open('ColorScheme.json'))


infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

Formation_names=corepy.Formation_names(Run_settings["Formation"],Run_settings["Formation_2"])
## This section runs all necessary functions in CorePy
corepy.RootDir(Run_settings['CoreOfStudy'], Formation_names)
corepy.MakeXRFdf(Run_settings['CoreOfStudy'],Run_settings["elements"],Run_settings["outlier_multiplier"],Run_settings["Depth_model"],Formation_names)
coredata=corepy.MakeXRFdf(Run_settings['CoreOfStudy'],Run_settings["elements"],Run_settings["outlier_multiplier"],Run_settings["Depth_model"],Formation_names)

corepy.Remove_outliers(coredata)
corepy.Include_outliers(coredata)

coredata_no_outliers=corepy.Remove_outliers(coredata)
coredata_outliers=corepy.Include_outliers(coredata)
x_new=corepy.PCA_analysis(coredata_no_outliers,Run_settings["elements"]) # matrix of principal components
coredata_no_outliers=corepy.Kmeans_cluster(x_new,coredata_no_outliers,Run_settings["Principal_components"], Run_settings["clusters"], Run_settings["PC1"], Run_settings["PC2"])
coredata_outliers["Chemofacies_PCA"] = max(coredata_no_outliers.Chemofacies_PCA)+1
dirName=corepy.RootDir(Corebeta["corename"], Formation_names)  
coredata=corepy.WriteCSV(coredata_no_outliers,coredata_outliers,dirName,Run_settings['CoreOfStudy'],Formation_names,Run_settings["Depth_model"])

pca_explained=corepy.PCA_explained(coredata_no_outliers,Run_settings["elements"])

PCA_elbow=corepy.Elbow_method(x_new,Run_settings["Principal_components"])

pca_vectors=corepy.PCA_matrix_elements(coredata_no_outliers,Run_settings["elements"])


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

xs = x_new[:,Run_settings["PC1"]]
ys = x_new[:,Run_settings["PC2"]]
scalex = 1.0/(xs.max() - xs.min())
scaley = 1.0/(ys.max() - ys.min())


sns.scatterplot(coredata_no_outliers.PCA1*scalex, coredata_no_outliers.PCA2*scaley, hue=coredata_no_outliers.Chemofacies_PCA, s=30,palette=chemofacies_color,edgecolor='black', zorder=1, legend=False)

n = pca_vectors.shape[0]
for i in range(n):
   arrow_style = dict(arrowstyle = "-|>", color = 'k', shrinkA = 0, shrinkB = 0, lw = 1, ls = '-')
   plt.annotate('', xy = (pca_vectors[Run_settings["PC1"],i] * 1, pca_vectors[Run_settings["PC2"],i] * 1), xytext = (0,0), arrowprops = arrow_style, zorder = 2)
   txt_style = plt.text(pca_vectors[Run_settings["PC1"],i] * 1.1, pca_vectors[Run_settings["PC2"],i] * 1.1, Run_settings["elements"][i], color = 'w', ha = 'center', va = 'center', zorder = 3)
   txt_style.set_path_effects([PathEffects.withStroke(linewidth = 2, foreground = 'black')])
   plt.xlabel("PC{}".format(Run_settings["PC1"]+1))
   plt.ylabel("PC{}".format(Run_settings["PC2"]+1))
plt.savefig(os.path.join(dirName + '/' + Run_settings['CoreOfStudy'] + '_' + Formation_names + '_PCA' + '.png'),dpi = 300)


