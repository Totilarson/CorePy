import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import seaborn as sns
from sklearn import metrics
import matplotlib.pyplot as plt
import os
import json
import corepytools as corepy

import xgboost as xgb
from xgboost import plot_importance

# This script builds a chemofacies training dataset for the Formation listed in settings "Formation_names"
# It searches for a Training dataset .csv file in the folder /CoreData/CoreBeta/ abnd uses the chemofacies listed in column 'Chemofacies_train'
# Output is a file in folder /CoreData/CoreNeuralModel/ listed for the formation


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


# Directory for stored Machine learning training datasets
NeuralModel_TrainingDataSet = os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names  + '_TrainingDataset.csv')
NeuralModel_TrainingDataSet = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Run_settings["Depth_model"]], ascending=False)


# Making training dataset for Neural model
y=NeuralModel_TrainingDataSet['Chemofacies_train']
X = NeuralModel_TrainingDataSet[Run_settings["elements"]].values #converts X from a df to an array

# options for NN model reagrding test size split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,random_state=0)


# scale the data
scaler = StandardScaler()
scaler.fit(X_train) # check this. why is it here and does it need to be used by all datasets
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
X_total = scaler.transform(X)

# apply the neural network to the scaled data
# solver{‘lbfgs’, ‘sgd’, ‘adam’}  sgd: stochastic gradient descent. adam: stochastic gradient-based optimizer. lbfgs: an optimizer in the family of quasi-Newton methods
# activation{‘identity’, ‘logistic’, ‘tanh’, ‘relu’}


# sklearn.neural_network.MLPClassifer
scaler = StandardScaler()
mlp = MLPClassifier(hidden_layer_sizes=(10,10,10),random_state=1,activation = 'relu',solver='sgd', max_iter=2000)
mlp.fit(X_train, y_train)


#run the model off the test data
y_pred_NN = mlp.predict(X_test)
print(classification_report(y_test,y_pred_NN))

cnf_matrix = metrics.confusion_matrix(y_test, y_pred_NN)
sns.heatmap(cnf_matrix, annot=True)
plt.show()

#####run the model across the entire dataset to add a column of predicted chemofacies to the exported data sheet

chemo_predict=mlp.predict(X_total) #scaled original dataset. 
chemo_predict=chemo_predict.reshape(-1, 1)
chemo_prob=mlp.predict_proba(X_total)


# This section automates the column headings so the number matches the number of chemofacies
Chemofacies_count=np.sort(NeuralModel_TrainingDataSet['Chemofacies_train'].unique())
Prediction_matrix_headings=['Chemo_pred']

for i in range(len(Chemofacies_count)):
    Prediction_matrix_headings.append('Prob'+str(Chemofacies_count[i]))

NN_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'NN_model_' + Formation_names)

outfile = open(NN_file,'wb')
pickle.dump(mlp,outfile)
outfile.close()







##### XGBoost model######


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,random_state=0)
feature_names = Run_settings["elements"] # feature names



dtrain = xgb.DMatrix(X_train, label=y_train,feature_names=feature_names)
dtest = xgb.DMatrix(X_test, label=y_test,feature_names=feature_names)

param = {
    'max_depth': 10,  # the maximum depth of each tree. too high and will overfit. Noticed with Iris dataset that if the number is less than the number of features it skips a feature
    'eta': 0.3,  # the training step for each iteration
    'silent': 1,  # logging mode - quiet
    'objective': 'multi:softprob',  # error evaluation for multiclass training
    'num_class': 9}  # the number of classes that exist in this datset
num_round = 5  # the number of training iterations

XGB_model = xgb.train(param, dtrain, num_round) #XGBoost model 

preds = XGB_model.predict(dtest) # dtest is built off of X_test
y_pred_XGB = np.asarray([np.argmax(line) for line in preds]) # an array of the predictions for each sample (largest value)

#Feature importance
fig, (ax1) = plt.subplots(ncols=1, figsize=(20,5))
ax1 = plot_importance(XGB_model)
plt.show()

cnf_matrix = metrics.confusion_matrix(y_test, y_pred_XGB)
sns.heatmap(cnf_matrix, annot=True)
plt.show()

XGB_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'XGB_model_' + Formation_names)

outfile = open(XGB_file,'wb')
pickle.dump(XGB_model,outfile)
outfile.close()

#import corepytools as corepy
#coredata = corepy.OutputXRF(Run_settings["CoreOfStudy"],Formation_names)
#X_XGB = NeuralModel_TrainingDataSet[Run_settings["elements"]]
X = NeuralModel_TrainingDataSet[Run_settings["elements"]]
ddata = xgb.DMatrix(X)

preds_2 = XGB_model.predict(ddata) # dtest is built off of X_test

y_pred_XGB_2 = np.asarray([np.argmax(line) for line in preds_2]) # an array of the predictions for each sample (largest value)
