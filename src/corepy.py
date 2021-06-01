import os
import numpy as np
import pandas as pd
import glob
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns

def sum(x,y): # this is only here to test the package upload
    return x+y


def RootDir(corename, Formation_names):
    root_dir = 'CorePy'
    main_dir = ['CoreData', 'CoreOutput', 'CoreTubes']			# Loading the list of sub-directories
    sub_dir= ['CoreAttributes', 'CoreXRF']    
    
    
    for i in range(0, len(main_dir)):
        dirName = str(root_dir) + '/' + str(main_dir[i])
        if not os.path.exists(dirName):
            os.makedirs(dirName)
    		      
    # builds the necessary subdirectory folders

    for i in range(0, len(sub_dir)):
        dirName = str(root_dir) + '/' + str(main_dir[0]) + '/' + str(sub_dir[i])
        if not os.path.exists(dirName):
		        os.makedirs(dirName)

    # build corename folder    
    
    for i in range(0, len(corename)):
        dirName = str(root_dir) + '/' + str(main_dir[1]) + '/' + str(corename) 
        if not os.path.exists(dirName):
		        os.makedirs(dirName)

    # Build Formation Folder
    for i in range(0, len(Formation_names)):
        dirName = str(root_dir) + '/' + str(main_dir[1]) + '/' + str(corename) + '/' + str(Formation_names) 
        if not os.path.exists(dirName):
		        os.makedirs(dirName)
        return dirName        # this is needed to direct output files
    
def movingaverage(interval, moving_avg):
    window= np.ones(int(moving_avg))/float(moving_avg)
    return np.convolve(interval, window, 'same')
                

def MakeXRFdf(corename,elements,outlier_multiplier,Depth_model):   # bad form here. need to link better but I don't know how to link below RootDir
     
    XRF_file = os.path.join(str('./CorePy/Coredata/CoreXRF/') + corename + '_XRF.csv')
    LODT5 = pd.read_csv(os.path.join(str('./CorePy/Coredata/CoreXRF/') + 'T5iLOD_XRF.csv'))

    files=glob.glob(XRF_file)

    for file in files:
        coredata=pd.read_csv(file)
        coredata[elements]=np.maximum(coredata[elements],LODT5[elements])
        Element_outlier=(coredata[elements]).mean()+outlier_multiplier*(coredata[elements]).std()
        coredata['Outliers']=((coredata[elements])>Element_outlier).any(axis='columns')
        coredata = coredata.sort_values([Depth_model])
        return coredata
    
    
def Remove_outliers(coredata):
    X=(coredata[coredata['Outliers'] == False]) #excludes outliers from the dataset being evaluated
    return X

def Include_outliers(coredata):
    Y=(coredata[coredata['Outliers'] == True]) #excludes outliers from the dataset being evaluated
    return Y

def PCA_analysis(X,elements):
    scaler = StandardScaler() #create a standard scaler object
    pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
    scaler.fit(X[elements].values)
    x_new = pca.fit_transform(scaler.transform(X[elements].values)) #
    return x_new

def Kmeans_cluster(x_new,X,Principal_components, clusters):
    x_cluster = x_new[:, np.arange(Principal_components)] #PCs used in clustering
    kmeans = KMeans(n_clusters=clusters) #select the number of clusters
    kmeans.fit(x_cluster) #results from PCA
    Chemofacies_PCA = kmeans.predict(x_cluster)+1 #array of the chemofacies classification for each row
    X['Chemofacies_PCA']=Chemofacies_PCA #makes a new column based on above conditional format
    
    PCA1=0
    PCA2=2
    xs = x_new[:,PCA1]
    ys = x_new[:,PCA2]
    X['PCA1']=xs #makes a new column based on above conditional format
    X['PCA2']=ys #makes a new column based on above conditional format
    #features= np.arange(len(elements))
        
    return X

def WriteCSV(X,Y,dirName,corename,Formation_names,Depth_model):
    coredata=pd.concat([X, Y], ignore_index=True)
    coredata.to_csv  (os.path.join(dirName + '/' + corename + '_' + Formation_names + '.csv'))
    coredata = coredata.sort_values([Depth_model])
    return coredata 

# builds a color dict used in all plots for each chemofacies
def ColorPalette(ColorScheme):
    palette = dict(zip(ColorScheme, sns.color_palette()))
    outfile = open('chemocolor','wb')
    pickle.dump(palette,outfile)
    outfile.close()