# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 15:43:03 2019

@author: Connor
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import matplotlib.pyplot as plt
from Homework1 import lm
import seaborn as sns


### PART 1: PCA and Linear Regression ###
df = pd.read_csv('linear_regression_test_data.csv',index_col=0)
x = np.asarray(df['x']).reshape(-1,1)
y = np.asarray(df['y']).reshape(-1,1)
y_theoretical = np.asarray(df['y_theoretical']).reshape(-1,1)
pca = PCA(n_components=1)
pc1 = -1 * pca.fit(x).transform(x)
pc_df = pd.DataFrame(data=pc1)

linear_model = lm(x,y,0.95)
new_y_theoretical = linear_model.beta0hat + linear_model.beta1hat * linear_model.x

fig1 = plt.subplots()
plt.scatter(x,y,label = 'y-values')
plt.plot(x,y_theoretical,color='green',label = 'y-theoretical')
plt.scatter(x,pc1,label = 'PC1')
plt.plot(linear_model.x, new_y_theoretical, color='purple',label = 'Linear Regression line')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')

### PART 2: PCA and LDA ###

df2 = pd. read_csv('dataset_1.csv')
#print(df2)
pca = PCA(n_components=2)
pc2 = pca.fit(df2).transform(df2)
pc_df2 = pd.DataFrame(data=pc2,columns = ['PC1','PC2'])
pc_df2['Cluster'] = df2['label']
print('Variance group 1 PC1:',np.var(pc_df2['PC1'][0:30]),'\nVariance group 2 PC1:',np.var(pc_df2['PC1'][30:60]))
print('Variance group 1 PC2:',np.var(pc_df2['PC2'][0:30]),'\nVariance group 2 PC2:',np.var(pc_df2['PC2'][30:60]))

xlda = np.asarray(df2['V2']).reshape(-1,1)
labels = np.asarray(df2['label'])
sk_lda = LDA(n_components = 1)
lda_sklearn = sk_lda.fit_transform(xlda,labels)

w_list = [np.transpose(lda_sklearn[i]/df2['V2'][i]) for i in range(0,len(xlda))]
print(np.transpose(lda_sklearn))
print(w_list)
print('W variance group 1:', np.var(lda_sklearn[0:30]),'\nGroup 2:',np.var(lda_sklearn[30:60]))

fig2 = plt.subplots()
plt.scatter(df2['V1'][0:30],df2['V2'][0:30],label = 'V1 vs V2 group 1', color = 'red')
plt.scatter(df2['V1'][30:60],df2['V2'][30:60],label = 'V1 vs V2 group 2', color = 'blue')
# =============================================================================
# plt.scatter(df2['V1'][0:30],pc_df2['PC2'][0:30], label = 'V1 vs PC1 group1',color = 'purple')
# plt.scatter(df2['V1'][30:60],pc_df2['PC2'][30:60], label = 'V1 vs PC1 group2',color = 'green')
# =============================================================================
plt.legend()
plt.ylabel('V2')
plt.xlabel('V1')

fig3 = plt.subplots()
plt.scatter(lda_sklearn[0:30],pc_df2['PC1'][0:30],label = 'Group 1')
plt.scatter(lda_sklearn[30:60],pc_df2['PC1'][30:60], label = 'Group 2')
plt.legend()
plt.xlabel('W')
plt.ylabel('PC1')
plt.title('W vs PC1')

fig4 = plt.subplots()
plt.scatter(w_list[0:30],len(pc_df2['PC1'][0:30]) * [1], label = 'Group 1')
plt.scatter(w_list[30:60],len(pc_df2['PC1'][30:60]) * [1], label = 'Group 2')
plt.legend()
plt.xlabel('PC2')

sns.lmplot(x='PC1', y ='PC2',data=pc_df2, fit_reg=False, hue='Cluster',legend = True)
