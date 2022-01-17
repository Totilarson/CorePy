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

import xgboost as xgb
from xgboost import plot_importance

# This script runs XGBoost and NN supervised clustering algorithms on integrated XRF-Wireline log files
# Input: Labeled Training dataset _WirelineLog_TrainingDataset.csv file in the folder /CoreData/CoreNeuralModel/
# Input: Wireline logs applied have to be specified CoreBeta["WirelineLogs_NeuralModel"] 
# Output: NN_model_wireline_Formation and XGB_model_wireline_Formation in folder /CoreData/CoreNeuralModel/ 

# Root_path, Run_settings, and Corebeta and the two .json core settings files with all input parameters
Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

# Formation_names is an expansion idea to select sub-Formations
# Creates a str variable to select Formation-specific rows from csv input file. 
# For now Formation_names is Run_settings["Formation"]
Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

# Import labelled training dataset. 
NeuralModel_TrainingDataSet = os.path.join( Root_path + '/CoreData/CoreNeuralModel/'  + Formation_names   +   '_WirelineLog_TrainingDataset.csv')
NeuralModel_TrainingDataSet = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Run_settings["Depth_model"]], ascending=False)


# User-selected logs for Wireline model are stored in the corbeta file. 
Model_logs= Corebeta["WirelineLogs_NeuralModel"]


## Neural Network Clustering model

y=NeuralModel_TrainingDataSet['Chemofacies_NN'] # Making training dataset for Neural model
X = NeuralModel_TrainingDataSet[Model_logs].values #converts X from a df to an array
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,random_state=0)

scaler = StandardScaler() # scale the data
scaler.fit(X_train) # check this. why is it here and does it need to be used by all datasets
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
X_total = scaler.transform(X)

# apply the neural network to the scaled data
# solver{‘lbfgs’, ‘sgd’, ‘adam’}  sgd: stochastic gradient descent. adam: adaptive moment estimation. lbfgs: an optimizer in the family of quasi-Newton methods
# activation{‘identity’, ‘logistic’, ‘tanh’, ‘relu’}
mlp = MLPClassifier(hidden_layer_sizes=(10,10,10),random_state=1,activation = 'relu',solver='adam', max_iter=2000)
mlp.fit(X_train, y_train)

#run the model off the test data
y_pred = mlp.predict(X_test)
print(classification_report(y_test,y_pred))

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
sns.heatmap(cnf_matrix, annot=True)
plt.show()

# Output Neural network model
NN_wirelinefile=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'NN_model_wireline_' + Formation_names)
outfile = open(NN_wirelinefile,'wb')
pickle.dump(mlp,outfile)
outfile.close()



##### XGBoost model######


y=NeuralModel_TrainingDataSet['Chemofacies_XGB']
X = NeuralModel_TrainingDataSet[Model_logs].values #converts X from a df to an array
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,random_state=0)

feature_names = Model_logs
    
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

plot_importance(XGB_model)
plt.show()


cnf_matrix = metrics.confusion_matrix(y_test, y_pred_XGB)
sns.heatmap(cnf_matrix, annot=True)
plt.show()

# Export XGBoost model 
XGB_wirelinefile=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'XGB_model_wireline_' + Formation_names)

outfile = open(XGB_wirelinefile,'wb')
pickle.dump(XGB_model,outfile)
outfile.close()




    


