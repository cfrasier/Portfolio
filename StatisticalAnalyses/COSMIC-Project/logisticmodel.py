# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 13:32:43 2019

@author: Connor
"""

import numpy as np
from math import exp, log

class logistic_model:
	
	### Initialize model object, setting up arrays for thetas and x-values ###
	def __init__(self,x,y,learning_rate):
		self.samples = np.asarray(x)
		self.flower_types = y
		self.learning_rate = learning_rate
		self.sample_shape = np.shape(self.samples)[1]
		self.thetas = np.zeros(self.sample_shape)
	
	### Method to perform gradient descent on dataset ###
	def gradient_descent(self,num_iterations,stopping_point):
		
		### Setup of lists to store J values through the iterations ###
		self.dJ_list = []
		self.J_list =  []
		self.delta_Js = []
		
		for iteration in range((num_iterations)):
			self.gz = []
			for i in range(len(self.samples)):

				### Perform linear combination of values and calculate g(z) ###
				z = np.transpose(self.thetas) * self.samples[i]
				self.gz.append(1/(1+exp(-sum(z))))
			
			### Calculate dJ/d0, update thetas, and calculate Delta J for current iteration ###
			self.dJ = 1/len(self.samples) * sum([(self.gz[i] - self.flower_types[i]) * self.samples[i] for i in range(len(self.samples))])
			self.dJ_list.append(self.dJ)
			self.thetas = self.thetas - self.learning_rate * self.dJ
			J = -1/len(self.samples) * sum([(self.flower_types[i] * log(self.gz[i],10)) + (1-self.flower_types[i])*log((1-self.gz[i]),10) for i in range(len(self.samples))])
			self.J_list.append(J)
			delta_J = abs(self.J_list[iteration] - self.J_list[iteration-1])
			self.delta_Js.append(delta_J)
			if delta_J < stopping_point and iteration != 0: break
	
	### Prediction method for testing data ###
	def predict_classification(self,x):
		self.testing_data = x
		testing_z = np.transpose(self.thetas) * self.testing_data
		testing_gz = 1/(1+exp(-sum(testing_z)))
		return (testing_gz)

