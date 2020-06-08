import numpy as np
from math import exp, log
import pandas as pd
import matplotlib.pyplot as plt

wdbc = pd.read_csv('wdbc.data',header=None)
breast_cancer_diagnoses = np.asarray(wdbc.iloc[:,1].values)
breast_cancer_features = np.asarray(wdbc.drop(1,axis=1))

breast_cancer_diagnoses[breast_cancer_diagnoses == 'M'] = 1
breast_cancer_diagnoses[breast_cancer_diagnoses == 'B'] = 0

class ANN:

    def __init__(self,feature_list,class_list):
        self.x = feature_list
        self.y = class_list
        self.sample_shape = np.shape(self.x)[1]

    def logistic_activity(self,linear_combination):
        return 1/(1+exp(-sum(linear_combination)))

    def build_model(self,num_hidden_layers,num_nodes_per_hidden_layer,learning_rate,num_iterations):

        ### Initializing values for hidden layers and gradient descent ###
        self.num_iterations = num_iterations
        self.num_hidden_layers = num_hidden_layers
        self.num_nodes_per_hidden_layer = num_nodes_per_hidden_layer
        self.learning_rate = learning_rate        

        ### initializing empty arrays to be filled during forward propagation ###
        self.activity = np.empty((self.num_hidden_layers,self.num_nodes_per_hidden_layer+1))
        self.z = np.empty(np.shape(self.activity))
        self.thetas = {}
        self.big_delta = dict.fromkeys(range(0,self.num_hidden_layers+1),0)
        self.delta = {}
        self.D = {}
        self.Js = []
        for i in range(0,self.num_hidden_layers):
            if i == 0:
                self.thetas[i] = np.zeros((self.num_nodes_per_hidden_layer,self.sample_shape))
            else:
                self.thetas[i] = np.zeros((self.num_nodes_per_hidden_layer+1,self.num_nodes_per_hidden_layer + 1))
        self.thetas[self.num_hidden_layers] = np.zeros(self.num_nodes_per_hidden_layer + 1)
        #print(self.thetas)
        for iteration in range(self.num_iterations):
            self.sample_Js = []

            for sample in range(len(self.x)):
                
                ### perform forward propagation ###
                for i in range(0,self.num_hidden_layers):
                    for j in range(0,self.num_nodes_per_hidden_layer):
                        if i == 0:
                            #self.thetas[i][j] = np.append(self.thetas[i][j],1)
                            self.input_with_bias = np.append(self.x[sample],1)
                            print((self.thetas[i][j]),j,iteration,sample)
                            self.z = (np.transpose(np.append(self.thetas[i][j],1)) * self.input_with_bias)
                        else:
                            #self.thetas[i] = np.zeros((self.num_nodes_per_hidden_layer+1,self.num_nodes_per_hidden_layer + 1))
                            self.activity[i-1][self.num_nodes_per_hidden_layer] = 1
                            self.z = np.transpose(self.thetas[i][j]) * self.activity[i-1]
                        self.activity[i][j] = self.logistic_activity(self.z)
                        self.activity[i][self.num_nodes_per_hidden_layer]=1
                self.z = np.transpose(self.thetas[self.num_hidden_layers]) * self.activity[-1]
                self.output_activity = self.logistic_activity(self.z)
                self.delta[self.num_hidden_layers] = (self.output_activity - self.y[sample])



                for i in range(self.num_hidden_layers-1,-1,-1):
                    if i == self.num_hidden_layers-1:
                        self.current_activity = self.activity[i][0:-1]
                        self.delta[i] = np.transpose(self.delta[i+1]) * np.diag(self.thetas[i+1][0:-1] * np.diag(self.current_activity * (1-self.current_activity)))
                        self.delta[i] = np.transpose(self.delta[i])
                    else:
                        self.current_activity = self.activity[i][0:-1]
                        self.delta[i] = np.transpose(self.delta[i+1]) * np.diag(self.thetas[i+1][0:-1,0:-1] * np.diag(self.current_activity * (1-self.current_activity)))
                        self.delta[i] = np.transpose(self.delta[i])
                self.sample_Js.append(self.y[sample] * log(self.output_activity,10) + (1-self.y[sample]*(1-log(self.output_activity,10))))

                for i in range(0,self.num_hidden_layers+1):
                    if i == self.num_hidden_layers:
                        self.big_delta[i] = self.big_delta[i] + (self.output_activity) * self.delta[i]
                        self.D[i] = 1/len(self.x) * self.big_delta[i]
                        #print(self.thetas[i])
                        self.thetas[i] = np.transpose(self.thetas[i][0:-1]) - self.learning_rate * self.D[i]
                    elif i == 0:
                        self.big_delta[i] = self.big_delta[i] + np.transpose(np.asarray(self.x[sample][np.newaxis])) * self.delta[i]
                        self.D[i] = 1/len(self.x) * self.big_delta[i]
                        self.thetas[i] = (np.append(self.thetas[i][:,0:-1],1)) - self.learning_rate * np.transpose(self.D[i])
                    else:
                        self.big_delta[i] = self.big_delta[i] + (self.activity[i][0:-1]) * self.delta[i]
                        self.D[i] = 1/len(self.x) * self.big_delta[i]
                        self.thetas[i] = np.transpose(self.thetas[i][0:-1,0:-1]) - self.learning_rate * self.D[i]
            self.Js.append(-sum(self.sample_Js)/len(self.x))

wdbc.ANN = ANN(breast_cancer_features,breast_cancer_diagnoses)
wdbc.ANN.build_model(2,4,0.1,5)
#print(np.shape(wdbc.ANN.x))
#print(wdbc.ANN.activity)
print((wdbc.ANN.thetas))
#print((wdbc.ANN.delta))
#print(wdbc.ANN.big_delta)
#print(wdbc.ANN.D)
plt.plot(wdbc.ANN.Js)