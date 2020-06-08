# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 12:59:41 2019

@author: Connor
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn import linear_model
import Homework1
import random

diabetes = datasets.load_diabetes()

x = diabetes.data[:,2]
y = diabetes.target
train_conf_val = 0.95

### Subsetting data ###
x_test, y_test = zip(*random.sample(list(zip(x,y)), 20))
x_train, y_train = zip(*set(zip(x,y)) - set(zip(x_test,y_test)))

x_train = np.asarray(x_train)
y_train = np.asarray(y_train)

x_test = np.asarray(x_test)
y_test = np.asarray(y_test)

line_width_1 = 2
line_width_2 = 2
marker_1 = '.' # point
marker_2 = 'o' # circle
marker_size = 12
line_style_1 = ':' # dotted line
line_style_2 = '-' # solid line

### Initialization of linear model instances for training and test data ###
diabetes_model_train = Homework1.lm(x_train,y_train,train_conf_val)
diabetes_model_test = Homework1.lm(x_test,y_test,train_conf_val)

### Initialization of sklearn model data ###
sklearn_x_test = x_test.reshape(-1,1)
sklearn_x_train = x_train.reshape(-1,1)

reg = linear_model.LinearRegression()
reg_data = np.asarray(zip(x_test,y_test))
reg.fit(sklearn_x_train,y_train.reshape(-1,1))
sklearn_y_predicted = reg.predict(sklearn_x_test)

### Setting up variables to draw plots ###
y_theoretical = diabetes_model_train.beta0hat + diabetes_model_train.beta1hat * diabetes_model_test.x
x_testing = diabetes_model_test.x
y_testing = diabetes_model_test.y
yhat_testing = diabetes_model_test.yhat

### Plotting different algorithms ###
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(2,2,1)
ax.scatter(x_testing,y_testing,color='red',marker=marker_1,linewidth=line_width_1)
ax.plot(x_testing,y_theoretical,color='green',label='theoretical')
ax.plot(x_testing,yhat_testing,color='blue',label='predicted')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title("My model")
ax.legend(loc='lower right', fontsize=9)

ax2 = fig.add_subplot(2,2,2)
ax2.scatter(x_testing,y_testing,color='red',marker=marker_1,linewidth=line_width_1)
ax2.plot(x_testing,sklearn_y_predicted,color='purple',label='sklearn')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title("Sklearn model")
ax2.legend(loc='lower right', fontsize=9)