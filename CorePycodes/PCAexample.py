import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import corepytools as corepy
import matplotlib.patheffects as PathEffects
import json

# PCAexample.py is a Python script that collects input data, builds folder structure, runs PCA and Kmeans cluster analysis
# File dependencies: 1) are a_XRF.csv core data and T5iLOD.csv file in /Coredata/COreXRF, 2)  settings.py, and 3) .json files
# Two .json files: 1) names after core of study, and 2) chemocolor.json
# outputs: a folder CoreOutput/CoreName/Formation, a summary plot, and a csv file with columns added to input csv file
# outliers are identified (csv column), values are replaced with detection limits, Kmeans cluster are identified (csv column), PCA1 and PCA2 values are added

# Root_path, Run_settings, and Corebeta and the two .json core settings files with all input parameters
Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names is Run_settings["Formation"]
Formation_names=corepy.Formation_names(Run_settings["Formation"],Run_settings["Formation_2"])



# loads the color palette into a dict called "chemofacies_color
infile = open('chemocolor','rb')
chemofacies_color= pickle.load(infile)
infile.close()  

# RootDir(corename, Formation_names) established the output folder structure
dirName=corepy.RootDir(Corebeta["corename"], Formation_names) 

 
# This section runs all necessary functions stored in CorePy
# coredata is a dataframe from an input .csv file ( _XRF). detection limits and outlier identification is performed 
corepy.RootDir(Run_settings['CoreOfStudy'], Formation_names)
corepy.MakeXRFdf(Run_settings['CoreOfStudy'],Run_settings["elements"],Run_settings["outlier_multiplier"],Run_settings["Depth_model"],Formation_names)
coredata=corepy.MakeXRFdf(Run_settings['CoreOfStudy'],Run_settings["elements"],Run_settings["outlier_multiplier"],Run_settings["Depth_model"],Formation_names)

# TESTING: Training datasets can be substituted for coredata by using these two lines
#coredata_Training = (os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names + '_TrainingDataset.csv'))
#coredata=pd.read_csv(coredata_Training)

# Remove_outliers and Include_outliers are defined in corepytools are return two dataframes: coredata_no_outliers and coredata_outliers
# This is important to remove outliers for PCA, and then adding back the outliers (labeled as outliers) to the final output csv file
coredata_no_outliers=corepy.Remove_outliers(coredata)
coredata_outliers=corepy.Include_outliers(coredata)

# PCA_analysis(coredata_no_outliers,elements) defined in corepytools
# x_new is a dataframe of PCA results
x_new=corepy.PCA_analysis(coredata_no_outliers,Run_settings["elements"]) # matrix of principal components

# coredata_no_outliers dataframe gets columns added: PCA1 and PCA2 values, and Chemofacies_PCA clusters
coredata_no_outliers=corepy.Kmeans_cluster(x_new,coredata_no_outliers,Run_settings["Principal_components"], Run_settings["clusters"], Run_settings["PC1"], Run_settings["PC2"])

# outliers get clustered. Since the number of Kmeans clusters is a variable, outliers are one greater than the number of Kmeans. 
coredata_outliers["Chemofacies_PCA"] = max(coredata_no_outliers.Chemofacies_PCA)+1


#PCA_explained, PCAS_elbow, and pca_vectors defined in corepytools. Used for plotting and interpretation
pca_explained=corepy.PCA_explained(coredata_no_outliers,Run_settings["elements"])
PCA_elbow=corepy.Elbow_method(x_new,Run_settings["Principal_components"])
pca_vectors=corepy.PCA_matrix_elements(coredata_no_outliers,Run_settings["elements"])

# Plotting PCA and Kmeans results

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


### OUTPUT FILES ####

# high resolution (.eps) and lower resolution (.png) files are created
plt.savefig(os.path.join(dirName + '/' + Run_settings['CoreOfStudy'] + '_' + Formation_names + '_PCA' + '.png'),dpi = 300)
plt.savefig(os.path.join(dirName + '/' + Run_settings['CoreOfStudy'] + '_' + Formation_names + '_PCA' + '.eps'), format = 'eps',dpi = 600)

# Outlier and no_outlier dataframes are appended and written as .csv file and saved in output folder
coredata=corepy.WriteCSV(coredata_no_outliers,coredata_outliers,dirName,Run_settings['CoreOfStudy'],Formation_names,Run_settings["Depth_model"])
