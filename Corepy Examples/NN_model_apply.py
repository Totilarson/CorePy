import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import pickle
import seaborn as sns
import json
import corepytools as corepy

CoreOfStudy = 'Public'

## Importing core data
Corebeta=json.load(open(os.path.join(CoreOfStudy + '.json')))
Formation_names = '-'.join(Corebeta["Formation"]+Corebeta["Formation_2"]) # Would like to have Formation_names defined in Corebeta
dirName=corepy.RootDir(Corebeta["corename"], Formation_names) 
NN_file=os.path.join('NN_model_' + Formation_names)

infile = open(NN_file,'rb')
NN_model= pickle.load(infile)
infile.close()

coredata = corepy.OutputXRF(Corebeta['corename'],Formation_names)

X = coredata[Corebeta["elements"]].values #makes an array of elements in coredata df

# scale the data
scaler = StandardScaler()
scaler.fit(X)

X_total = scaler.transform(X)

chemo_predict=NN_model.predict(X_total) #scaled original dataset. 
chemo_predict=chemo_predict.reshape(-1, 1)
chemo_prob=NN_model.predict_proba(X_total)

Chemofacies_count=np.unique(chemo_predict)

Prediction_matrix_headings=['Chemofacies_NN']
for i in range(len(Chemofacies_count)):
    Prediction_matrix_headings.append('Prob'+str(Chemofacies_count[i]))

data=pd.DataFrame(np.concatenate((chemo_predict,chemo_prob),axis=1),columns = Prediction_matrix_headings)


Z=pd.concat([coredata, data], ignore_index=False)
Z = coredata.merge(data, left_index=True, right_index=True)