# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 11:24:16 2019

@author: Connor
"""

from sklearn import datasets,linear_model
import numpy as np
import matplotlib.pyplot as plt
import logisticmodel as lm
from math import exp, log

### Importation of data and set-up of dataframe for input into logistic model ###
iris = datasets.load_iris()

flower_types = iris.target[50:]
flower_features = iris.data[50:]

itemindex = np.nonzero(flower_types == 2)

flower_types[flower_types == 2] = 0

r = np.random.randint(low=0,high=100)

training_types = np.concatenate((flower_types[0:r],flower_types[r+1:100]))
training_features = np.concatenate((flower_features[0:r],flower_features[r+1:100]))

testing_type = flower_types[r]
testing_features = flower_features[r]

### Calling logistic model ###
x = lm.logistic_model(training_features,training_types,.1)

x.gradient_descent(10000,0.00001)
print("Predicted Class:",x.predict_classification(testing_features),"\nActual Class:",testing_type)
print("My model thetas:",x.thetas)

### Plotting J vs. Iteration # ###
fig = plt.figure()
plt.plot(x.J_list)
fig.suptitle("J vs. Iteration #",fontsize=18)
plt.xlabel("Iteration #",fontsize=16)
plt.ylabel("Cost J",fontsize=16)

### Sklearn initialization and calculation of final cost J ###
clf = linear_model.LogisticRegression().fit(flower_features,flower_types)
sklearn_thetas = (clf.coef_[0])
print("Sklearn model thetas:",sklearn_thetas)
sklearn_gz = []
for i in range(len(flower_features)):
	z = np.transpose(sklearn_thetas) * flower_features[i]
	sklearn_gz.append(1/(1+exp(-sum(z))))
sklearn_J = -1/len(flower_features) * sum([(flower_types[i] * log(sklearn_gz[i],10)) + (1-flower_types[i])*log((1-sklearn_gz[i]),10) for i in range(len(flower_features))])
print("Final J for my model:",x.J_list[-1])
print("Final J for Sklearn:",sklearn_J)
