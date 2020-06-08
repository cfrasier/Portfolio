# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 11:19:43 2019

@author: Connor
"""

import numpy as np
import scipy.stats as stats

class lm:
	
	### Initialize values for statistical processes ###
	def __init__ (self,x,y,conf):
		self.x = x
		self.y = y
		self.conf = conf
		self.n = len(x)
		self.xbar = np.mean(x)
		self.ybar = np.mean(y)
		
		
		self.Syx = np.sum((y - self.ybar) * (x - self.xbar))
		self.Sxx = np.sum((x - self.xbar)**2)
		
		self.beta1hat = self.Syx/self.Sxx
		self.beta0hat = self.ybar - self.beta1hat * self.xbar
		
		self.yhat = self.beta0hat + self.beta1hat * x
		self.r = y - self.yhat
		self.sigmahat = np.sqrt(sum(self.r**2) / (self.n-2))
		
		self.SStotal = np.sum((y-self.ybar)**2)
		self.SSreg = np.sum((self.yhat - self.ybar)**2)
		self.SSerr = np.sum((y-self.yhat)**2)
		
		self.q=(1-self.conf)/2
		self.z = -stats.t.ppf(self.q, df = self.n-2)
		
	def estimateF (self):
		self.MStotal = self.SStotal/(self.n - 1)
		self.MSreg = self.SSreg/1
		self.MSerr = self.SSerr/(self.n-2)
		self.F = self.MSreg/self.MSerr
		self.F_test_pval = 1 - stats.f._cdf(self.F,dfn=1,dfd=self.n-2)
		
	def estimateR2 (self):
		self.R2 = self.SSreg/self.SStotal
		
	def calculateR2 (self):
		self.correlation_coefficient = np.corrcoef(self.x,self.y)
		self.R2 = self.correlation_coefficient[0,1]**2
		
	def confidenceintervalB1 (self):
		self.beta1hat_var = self.sigmahat**2/((self.n-1)*np.var(self.x))
		self.beta1hat_sd = np.sqrt(self.beta1hat_var)
		self.beta1hat_upperbound = self.beta1hat + self.z * self.beta1hat_sd
		self.beta1hat_lowerbound = self.beta1hat - self.z * self.beta1hat_sd
		self.beta1hat_tstatistic = self.beta1hat/self.beta1hat_sd
		self.beta1hat_ttestpval = 2*(1-stats.t.cdf(np.abs(self.beta1hat_tstatistic), df = self.n-2))
		
	def confidenceintervalB0 (self):
		self.beta1hat_var = self.sigmahat**2/((self.n-1)*np.var(self.x))
		self.beta0hat_var = self.beta1hat_var * np.sum(self.x**2)/self.n
		self.beta0hat_sd = np.sqrt(self.beta0hat_var)
		self.beta0hat_upperbound = self.beta0hat + self.z * self.beta0hat_sd
		self.beta0hat_lowerbound = self.beta0hat - self.z * self.beta0hat_sd
		self.beta0hat_tstatistic = self.beta0hat/self.beta0hat_sd
		self.beta0hat_ttestpval = 2*(1-stats.t.cdf(np.abs(self.beta0hat_tstatistic), df = self.n-2))
	
	def confidenceintervalRegressionline (self):
		self.sigmai = 1/self.n * (1 + ((self.x-self.xbar)/np.std(self.x))**2)
		self.yhat_sd = self.sigmahat * self.sigmai
		self.yhat_upperbound = self.yhat + self.z * self.yhat_sd
		self.yhat_lowerbound = self.yhat - self.z * self.yhat_sd

