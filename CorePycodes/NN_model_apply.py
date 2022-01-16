import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import pickle
import json
import corepytools as corepy
import xgboost as xgb

# NN_model_apply.py is a Python script runs Neural Network and XGBoost clustering algorithms on core XRF datasets
# File dependencies: 1) input file _XRF.csv data file in folder CoreOutput/CoreName/Formation, 2) settings.py
# File dependencies2: 3) Formation-specific _Training_Dataset.csv in \CoreData\CoreNeuralModel 
# Output: adds columns 'Chemofacies_NN' and 'Chemofacies_XGB' to .csv file in CoreOutput/CoreName/Formation


# 1) Define root path, 2) load Run_settings file for input variables
Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))

#loads the Corebeta .json file that provides information specific to each core
#Corebeta are .json files for each core name. MOre information about these .json files in CorePy description
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names isRun_settings["Formation"]
Formation_names=corepy.Formation_names(Run_settings["Formation"],Run_settings["Formation_2"])

# RootDir(corename, Formation_names) established the output folder structure
dirName=corepy.RootDir(Corebeta["corename"], Formation_names) 


# Data input - directs to core XRF datafile generated in PCAexample
coredata = corepy.OutputXRF(Run_settings["CoreOfStudy"],Formation_names)

## This is if you want to run the neural model on the attribute data file
## Have to uncomment the #coredata line 
Attribute_file = os.path.join(Root_path + '/CoreData/CoreAttributes/' + Run_settings['CoreOfStudy'] + '/' + Run_settings['CoreOfStudy'] +'_Attribute.csv') 
#coredata=pd.read_csv(Attribute_file)


# to prevent duplicating column names, these column names are dropped 
coredata = coredata.drop(columns=['Chemofacies_train', 'Chemofacies_NN', 'Chemofacies_XGB'],errors='ignore')

# Loads machine learning files generated from NN_model_build

NN_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'NN_model_' + Formation_names)
XGB_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'XGB_model_' + Formation_names)

infile = open(NN_file,'rb')
NN_model= pickle.load(infile)
infile.close()

infile = open(XGB_file,'rb')
XGB_model= pickle.load(infile)
infile.close()


# Machine learning section
# important to remember that Run_settings["elements"] has to match training dataset and coredataset
X = coredata[Run_settings["elements"]].values #makes an array of elements in coredata df

# scale the data
scaler = StandardScaler()
scaler.fit(X)

X_total = scaler.transform(X)

chemo_predict=NN_model.predict(X_total) #scaled original dataset. 
chemo_predict=chemo_predict.reshape(-1, 1)
chemo_prob=NN_model.predict_proba(X_total)


# This section is used to identify the unique names of the chemofacies in training dataset and make the headings in the output csv file
NeuralModel_TrainingDataSet = os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names  + '_TrainingDataset.csv')
NeuralModel_TrainingDataSet = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Run_settings["Depth_model"]], ascending=False)
Chemofacies_count=np.sort(NeuralModel_TrainingDataSet['Chemofacies_train'].unique())

Prediction_matrix_headings=['Chemofacies_NN']
for i in range(len(Chemofacies_count)):
    Prediction_matrix_headings.append('Prob'+str(Chemofacies_count[i]))

# This section concatenates the results and probabilities to the original file
# originally I included the probabilities in the output, but it made for a confusing datafile so I removed it
#Predicted_chemofacies=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = Prediction_matrix_headings)

# Makes a 1-column dataframe 'Chemofacies_NN' that is appended to the .csv output file
Predicted_chemofacies=pd.DataFrame(chemo_predict)
Predicted_chemofacies.columns = ["Chemofacies_NN"]


##### XGB Boost model ######

X_XGB = xgb.DMatrix(coredata[Run_settings["elements"]])
XGB_predict=XGB_model.predict(X_XGB) 
y_pred_XGB = np.asarray([np.argmax(line) for line in XGB_predict]) # an array of the predictions for each sample (largest value)
y_pred_XGB = pd.DataFrame(y_pred_XGB)
y_pred_XGB.columns = ['Chemofacies_XGB']


# Adds 'Predicted_chemofacies' dataframe to coredata, then adds XGB predicted chemofacies
Z = coredata.merge(Predicted_chemofacies, left_index=True, right_index=True)
Z = Z.merge(y_pred_XGB, left_index=True, right_index=True)

Z.to_csv (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '.csv'))

#Z.to_csv (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '_Attribute.csv'))





