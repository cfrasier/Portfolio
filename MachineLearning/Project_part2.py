# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 12:58:05 2019

@author: Connor
"""

import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import matplotlib.pyplot as plt

sk_lda = LDA(n_components = 1)
column_names = ['Age','Sex','Chest Pain','Resting Blood Pressure','Cholesterol','FBS','Resting ECG','Thalach','Exang','Oldpeak','Slope','CA','Thal','Diagnosis']
df = pd.read_csv('processed.cleveland.data',header=None,names=column_names,index_col=False)
df['Diagnosis'][df['Diagnosis'] > 0] = 1
df = df.replace('?',np.NaN)
df = df.dropna(0,'any')
df = df.sort_values(by='Diagnosis',axis=0)
#print(np.asarray(df['Diagnosis'][0:160]))

group1 = df[0:160]
group2 = df[160:len(df)+1]

print(group2)

true_positives = 0
true_negatives = 0
false_negatives = 0
false_positives = 0


for r in range(len(df)):
    training_data = pd.concat([df.iloc[0:r],df.iloc[r+1:len(df)]])
    testing_data = df.iloc[r]
    lda_model = sk_lda.fit_transform(training_data.iloc[:,0:13],training_data['Diagnosis'])
    if sk_lda.predict(np.asarray(testing_data.iloc[0:13]).reshape(1,-1))[0] == 1 and testing_data['Diagnosis'] == 1:
        true_positives += 1
    elif sk_lda.predict(np.asarray(testing_data.iloc[0:13]).reshape(1,-1))[0] == 0 and testing_data['Diagnosis'] == 0:
        true_negatives += 1
    elif sk_lda.predict(np.asarray(testing_data.iloc[0:13]).reshape(1,-1))[0] == 1 and testing_data['Diagnosis'] == 0:
        false_positives += 1
    elif sk_lda.predict(np.asarray(testing_data.iloc[0:13]).reshape(1,-1))[0] == 0 and testing_data['Diagnosis'] == 1:
        false_negatives += 1
        
accuracy = (true_positives + true_negatives)/(true_positives + true_negatives + false_negatives + false_positives)
print('Accuracy =',accuracy,'\nGroup 1 W variance =',np.var(lda_model[0:160]),'\nGroup 2 W variance =',np.var(lda_model[160:]))

print(np.var(lda_model[160:len(lda_model)]))

plt.scatter(lda_model[0:160],len(group1) * [1],label='Group 1 (Negative Diagnosis)')
plt.scatter(lda_model[160:],(len(group2) - 1) * [1], label = 'Group 2 (Positive Diagnosis)')
plt.legend()
plt.title('Data projected onto W')
plt.xlabel('W')
# =============================================================================
# with open('processed.cleveland.data') as infile:
#     for line in infile.readlines():
#         line = line.rstrip()
#         print(line)
# =============================================================================
