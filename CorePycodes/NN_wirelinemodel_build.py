# This script builds a chemofacies training dataset for the Formation listed in settings "Formation_names"
# It searches for a Training dataset .csv file in the folder /CoreData/CoreNeuralModel/ and uses the chemofacies listed in column 'Chemofacies_NN'
# Output is a file in folder /CoreData/CoreNeuralModel/ listed for the formation

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

Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta


NeuralModel_TrainingDataSet = os.path.join( Root_path + '/CoreData/CoreNeuralModel/'  + Formation_names   +   '_WirelineLog_TrainingDataset.csv')
NeuralModel_TrainingDataSet = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Run_settings["Depth_model"]], ascending=False)


#NeuralModel_TrainingDataSet = CoreWirelinedata
Model_logs= Corebeta["WirelineLogs_NeuralModel"]
# Making training dataset for Neural model
y=NeuralModel_TrainingDataSet['Chemofacies_NN']
X = NeuralModel_TrainingDataSet[Model_logs].values #converts X from a df to an array
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,random_state=0)


# scale the data
scaler = StandardScaler()
scaler.fit(X_train) # check this. why is it here and does it need to be used by all datasets
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
X_total = scaler.transform(X)

# apply the neural network to the scaled data
# solver{‘lbfgs’, ‘sgd’, ‘adam’}  sgd: stochastic gradient descent. adam: stochastic gradient-based optimizer. lbfgs: an optimizer in the family of quasi-Newton methods
# activation{‘identity’, ‘logistic’, ‘tanh’, ‘relu’}
mlp = MLPClassifier(hidden_layer_sizes=(10,10,10),random_state=1,activation = 'relu',solver='sgd', max_iter=2000)
mlp.fit(X_train, y_train)

#run the model off the test data
y_pred = mlp.predict(X_test)
print(classification_report(y_test,y_pred))

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
sns.heatmap(cnf_matrix, annot=True)
plt.show()

#fig, ((ax1)) = plt.subplots(nrows=1, ncols=1, figsize=(5,5)) #sharex=True, sharey=True,
#plt.subplot(1,1, 1)
#plt.savefig(os.path.join(dirName + '/' + Run_settings['CoreOfStudy'] + '_' + Formation_names + '_PCA' + '.png'),dpi = 300)

#####run the model across the entire dataset to add a column of predicted chemofacies to the exported data sheet

chemo_predict=mlp.predict(X_total) #scaled original dataset. 
chemo_predict=chemo_predict.reshape(-1, 1)
#chemo_predict=pd.DataFrame(data=chemo_predict,columns=["predicted"])
chemo_prob=mlp.predict_proba(X_total)

## Issues here. THe number of Probabilities should be dependant on on number of chemifacies defined for Formation

Chemofacies_count=np.sort(NeuralModel_TrainingDataSet['Chemofacies_NN'].unique())

Prediction_matrix_headings=['Chemo_pred_wireline']

for i in range(len(Chemofacies_count)):
    Prediction_matrix_headings.append('Prob'+str(Chemofacies_count[i]))


data=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = Prediction_matrix_headings)

NN_wirelinefile=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'NN_model_wireline_' + Formation_names)

outfile = open(NN_wirelinefile,'wb')
pickle.dump(mlp,outfile)
outfile.close()


    








    

