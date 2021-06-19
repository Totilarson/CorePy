import pandas as pd
import numpy as np
#from sklearn import preprocessing
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

CoreOfStudy = 'Public'

Root_path = os.path.dirname(os.getcwd())
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  CoreOfStudy + '.json')))


Formation_names = '-'.join(Corebeta["Formation"]+Corebeta["Formation_2"]) # Would like to have Formation_names defined in Corebeta

Root_path = os.path.dirname(os.getcwd())
NeuralModel_TrainingDataSet = os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names  + '_TrainingDataset.csv')
NeuralModel_TrainingDataSet = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Corebeta["Depth_model"]], ascending=False)


# Making training dataset for Neural model
y=NeuralModel_TrainingDataSet['Chemofacies_train']
X = NeuralModel_TrainingDataSet[Corebeta["elements"]].values #converts X from a df to an array
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

#####run the model across the entire dataset to add a column of predicted chemofacies to the exported data sheet

chemo_predict=mlp.predict(X_total) #scaled original dataset. 
chemo_predict=chemo_predict.reshape(-1, 1)
#chemo_predict=pd.DataFrame(data=chemo_predict,columns=["predicted"])
chemo_prob=mlp.predict_proba(X_total)

## Issues here. THe number of Probabilities should be dependant on on number of chemifacies defined for Formation

Chemofacies_count=np.sort(NeuralModel_TrainingDataSet['Chemofacies_train'].unique())

Prediction_matrix_headings=['Chemo_pred']

for i in range(len(Chemofacies_count)):
    Prediction_matrix_headings.append('Prob'+str(Chemofacies_count[i]))


data=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = Prediction_matrix_headings)

NN_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'NN_model_' + Formation_names)

outfile = open(NN_file,'wb')
pickle.dump(mlp,outfile)
outfile.close()


    


