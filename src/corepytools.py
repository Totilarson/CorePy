import os
import numpy as np
import pandas as pd
import glob
import pickle
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from PIL import Image
import re

def sumdumbfun(x,y): # this is only here to test the package during development
    return x*y*y

## RootDir establishes the export and data folder structure
def RootDir(corename, Formation_names):
    main_dir = ['CoreData', 'CoreOutput']
    sub_dir= ['CoreAttributes', 'CoreXRF','CoreBoxPhotos', 'CoreTubes']    
        
    for i in range(0, len(main_dir)):
        dirName = str(main_dir[i])
        if not os.path.exists(dirName):
            os.makedirs(dirName)
    		      
    # builds the necessary subdirectory folders

    for i in range(0, len(sub_dir)):
        dirName =  str(main_dir[0]) + '/' + str(sub_dir[i])
        if not os.path.exists(dirName):
		        os.makedirs(dirName)
 
    for i in range(0, len(corename)):
        dirName =  str(main_dir[1]) + '/' + str(corename)
        if not os.path.exists(dirName):
		        os.makedirs(dirName)

    for i in range(0, len(Formation_names)):
        dirName =  str(main_dir[1]) + '/' + str(corename) + '/' + str(Formation_names) 
        if not os.path.exists(dirName):
		        os.makedirs(dirName)
        return dirName        # this is needed to direct output files


def movingaverage(interval, moving_avg):
    window= np.ones(int(moving_avg))/float(moving_avg)
    return np.convolve(interval, window, 'same')
                

def MakeXRFdf(corename,elements,outlier_multiplier,Depth_model,Formation_names):   # bad form here. need to link better but I don't know how to link below RootDir

    XRF_file = os.path.join(str('./Coredata/CoreXRF/') + corename + '_XRF.csv')
    LODT5 = pd.read_csv(os.path.join(str('./Coredata/CoreXRF/') + 'T5iLOD_XRF.csv'))

    files=glob.glob(XRF_file)

    for file in files:
        coredata=pd.read_csv(file)
        coredata[elements]=np.maximum(coredata[elements],LODT5[elements])
        coredata= coredata[   coredata['Formation']==Formation_names]
        Element_outlier=(coredata[elements]).mean()+outlier_multiplier*(coredata[elements]).std()
        coredata['Outliers']=((coredata[elements])>Element_outlier).any(axis='columns')
        coredata = coredata.sort_values([Depth_model])
        return coredata
    
    
def Remove_outliers(coredata):
    coredata_no_outliers=(coredata[coredata['Outliers'] == False]) #excludes outliers from the dataset being evaluated
    return coredata_no_outliers

def Include_outliers(coredata):
    coredata_outliers=(coredata[coredata['Outliers'] == True]) #excludes outliers from the dataset being evaluated
    return coredata_outliers

def PCA_analysis(coredata_no_outliers,elements):
    scaler = StandardScaler() #create a standard scaler object
    pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
    scaler.fit(coredata_no_outliers[elements].values)
    x_new = pca.fit_transform(scaler.transform(coredata_no_outliers[elements].values)) #
    return x_new

def PCA_explained(coredata_no_outliers,elements):
    scaler = StandardScaler() #create a standard scaler object
    pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
    scaler.fit(coredata_no_outliers[elements].values)
    pca.fit_transform(scaler.transform(coredata_no_outliers[elements].values)) #
    pca_explained=pca.explained_variance_ratio_.cumsum()
    return pca_explained

def PCA_matrix_elements(coredata_no_outliers,elements):

    scaler = StandardScaler() #create a standard scaler object
    pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
    scaler.fit(coredata_no_outliers[elements].values)
    pca.fit_transform(scaler.transform(coredata_no_outliers[elements].values)) #
    pca_elements_matrix=pca.components_
    return pca_elements_matrix


def Kmeans_cluster(x_new,coredata_no_outliers,Principal_components, clusters,PC1,PC2):
    x_cluster = x_new[:, np.arange(Principal_components)] #PCs used in clustering
    kmeans = KMeans(n_clusters=clusters) #select the number of clusters
    kmeans.fit(x_cluster) #results from PCA
    Chemofacies_PCA = kmeans.predict(x_cluster)+1 #array of the chemofacies classification for each row
    coredata_no_outliers['Chemofacies_PCA']=Chemofacies_PCA #makes a new column based on above conditional format
    coredata_no_outliers['PCA1']=x_new[:,PC1] #Adds PCA1 to coredata file for reference
    coredata_no_outliers['PCA2']=x_new[:,PC2] #Adds PCA2 to coredata file for reference
    #features= np.arange(len(elements))
    return coredata_no_outliers

def Elbow_method(x_new,Principal_components):
    distortions = []
    X = x_new[:, np.arange(Principal_components)] #PCs used in clustering
    K = range(1,15)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
    return distortions

def WriteCSV(coredata_no_outliers,coredata_outliers,dirName,corename,Formation_names,Depth_model):
    coredata=pd.concat([coredata_no_outliers, coredata_outliers], ignore_index=True)
    coredata.to_csv  (os.path.join(dirName + '/' + corename + '_' + Formation_names + '.csv'))
    coredata = coredata.sort_values([Depth_model])
    return coredata 

# builds a color dict used in all plots for each chemofacies
def ColorPalette(ColorScheme):
    palette = dict(zip(ColorScheme, sns.color_palette()))
    outfile = open('chemocolor','wb')
    pickle.dump(palette,outfile)
    outfile.close()
    
def cropCorebox(cropArea, imageFileName,imageFolder,newFolderPath):
    imagePath = os.path.join(imageFolder, imageFileName)
    imgOpen = Image.open(imagePath)
    imgCrop = imgOpen.crop(cropArea)
    croppedimagePath = os.path.join(newFolderPath, imageFileName)
    imgCrop.save(croppedimagePath)
    imgOpen.close()
 
def ImageDir(corename):
    main_dir = ['CoreData']
    sub_dir= ['CoreBoxPhotos','CoreTubes']

    for i in range(0, len(main_dir)):
        dirName =  str(main_dir[i])
        if not os.path.exists(dirName):
            os.makedirs(dirName)
            
    for i in range(0, len(sub_dir)):
        dirName = str(main_dir[0]) + '/' + str(sub_dir[i])
        if not os.path.exists(dirName):
		        os.makedirs(dirName)
                
                
def OutputXRF(corename,Formation_names):   # bad form here. need to link better but I don't know how to link below RootDir
     
    XRF_file = os.path.join(str('./CoreOutput/') + corename + '/' + Formation_names + '/' + corename + '_' + Formation_names + '.csv')
    OutputXRF=pd.read_csv(XRF_file)
    return OutputXRF

def natural_sort(file_names):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(file_names, key = alphanum_key)