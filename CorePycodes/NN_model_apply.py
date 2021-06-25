import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import pickle
#import seaborn as sns
import json
import corepytools as corepy

CoreOfStudy = 'Valcher'


Root_path = os.path.dirname(os.getcwd())
Run_settings=json.load(open(os.path.join(Root_path + '/CorePycodes/' + 'Run_settings' + '.json')))
Corebeta=json.load(open(os.path.join(Root_path + '/CoreData/CoreBeta/'   +  Run_settings['CoreOfStudy']  +'.json')))

Formation_names = '-'.join(Run_settings["Formation"]+Run_settings["Formation_2"]) # Would like to have Formation_names defined in Corebeta

dirName=corepy.RootDir(Run_settings["CoreOfStudy"], Formation_names) 


NN_file=os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + 'NN_model_' + Formation_names)

infile = open(NN_file,'rb')
NN_model= pickle.load(infile)
infile.close()

coredata = corepy.OutputXRF(Run_settings["CoreOfStudy"],Formation_names)

X = coredata[Run_settings["elements"]].values #makes an array of elements in coredata df

# scale the data
scaler = StandardScaler()
scaler.fit(X)

X_total = scaler.transform(X)

chemo_predict=NN_model.predict(X_total) #scaled original dataset. 
chemo_predict=chemo_predict.reshape(-1, 1)
chemo_prob=NN_model.predict_proba(X_total)


Root_path = os.path.dirname(os.getcwd())
NeuralModel_TrainingDataSet = os.path.join(Root_path + '/CoreData/CoreNeuralModel/' + Formation_names  + '_TrainingDataset.csv')
NeuralModel_TrainingDataSet = pd.read_csv(NeuralModel_TrainingDataSet).sort_values(by=[Run_settings["Depth_model"]], ascending=False)
Chemofacies_count=np.sort(NeuralModel_TrainingDataSet['Chemofacies_train'].unique())


#Chemofacies_count=np.unique(chemo_predict) #problem when not all chemofacies are identified. Chemofacies count (Prediction matrix headings) doesn equal

Prediction_matrix_headings=['Chemofacies_NN']
for i in range(len(Chemofacies_count)):
    Prediction_matrix_headings.append('Prob'+str(Chemofacies_count[i]))

#data=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = Prediction_matrix_headings)
data=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = Prediction_matrix_headings)

#data=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = ['Chemofacies_NN' , 'Prob1', 'Prob2' , 'Prob3', 'Prob4', 'Prob5','Prob6'])

Z=pd.concat([coredata, data], ignore_index=False)
Z = coredata.merge(data, left_index=True, right_index=True)

Z.to_csv (os.path.join(dirName + '/' +  Run_settings["CoreOfStudy"] + '_' + Formation_names + '.csv'))
