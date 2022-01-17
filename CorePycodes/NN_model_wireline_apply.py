import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import pickle
#import seaborn as sns
import json
import corepytools as corepy
import xgboost as xgb

# This script applies XGBoost and NN supervised clustering algorithms on integrated XRF-Wireline log files
# Input: NN_model_wireline_Formation and XGB_model_wireline_Formation in folder /CoreData/CoreNeuralModel/ 
# Input: data file _WirelineLog.csv in selected core output folder 
# Output: '_WirelineLog_NN.csv' file in selected core output folder 

# Root_path, Run_settings, and Corebeta and the two .json core settings files with all input parameters
Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names is Run_settings["Formation"]
Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

# had to add separate dirName directory to link to _Wirelinelog.csv file
dirName=corepy.RootDir(Run_settings["CoreOfStudy"], Formation_names) 
coredata = (os.path.join(dirName + '/' +  Run_settings['CoreOfStudy'] + '_' + Formation_names + '_WirelineLog.csv'))
coredata=pd.read_csv(coredata)

# direct to machine learning models
NN_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'NN_model_wireline_' + Formation_names)
XGB_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'XGB_model_wireline_' + Formation_names)

infile = open(NN_file,'rb')
NN_model= pickle.load(infile)
infile.close()

# Wireline logs are user selected. data stored in Corebeta["WirelineLogs_NeuralModel"]
Model_logs= Corebeta["WirelineLogs_NeuralModel"]

X = coredata[Model_logs].values #makes an array of elements in coredata df

# scale the data
scaler = StandardScaler()
scaler.fit(X)
X_total = scaler.transform(X)

chemo_predict=NN_model.predict(X_total) #scaled original dataset. 
chemo_predict=chemo_predict.reshape(-1, 1)
chemo_prob=NN_model.predict_proba(X_total)


# This section is used to identify the unique names of the chemofacies in training dataset and make the headings in the output csv file
NeuralModel_TrainingDataSet = os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names  + '_WirelineLog_TrainingDataset.csv')
NeuralModel_TrainingDataSet = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Run_settings["Depth_model"]], ascending=False)
Chemofacies_count=np.sort(NeuralModel_TrainingDataSet['Chemofacies_NN'].unique())

Prediction_matrix_headings=['Electrofacies_NN']
for i in range(len(Chemofacies_count)):
    Prediction_matrix_headings.append('Prob'+str(Chemofacies_count[i]))

data=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = Prediction_matrix_headings)


# Decision tree model
infile = open(XGB_file,'rb')
XGB_model= pickle.load(infile)
infile.close()

X = coredata[Model_logs]


X_XGB = xgb.DMatrix(X)
XGB_predict=XGB_model.predict(X_XGB) 
y_pred_XGB = np.asarray([np.argmax(line) for line in XGB_predict]) # an array of the predictions for each sample (largest value)
y_pred_XGB = pd.DataFrame(y_pred_XGB)
y_pred_XGB.columns = ['Electrofacies_XGB']


Z=pd.concat([coredata, data], ignore_index=False)
Z = coredata.merge(data, left_index=True, right_index=True)
Z = Z.merge(y_pred_XGB, left_index=True, right_index=True)

#Output to .csv file in coredata output folder
Z.to_csv (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '_WirelineLog_NN.csv'))