import pandas as pd
import numpy as np
import scipy.stats
import logisticmodel as lm
import matplotlib.pyplot as plt
from statistics import mean
from math import exp
samples = []

with open("samples.txt") as infile:
    for line in infile.readlines():
        line = line.rstrip()
        samples.append(line) 

big_df = pd.DataFrame()
for sample in samples:
    sample_dict = {}
    with open("COSMIC_study_329.txt") as infile:
        for line in infile.readlines():
            line = line.rstrip()
            line_items = line.split()
            if sample in line:
                sample_dict[line_items[2]] = line_items[4]
    df = pd.DataFrame.from_dict(sample_dict, orient = 'index',columns = [sample])
    big_df = pd.concat([big_df,df],axis = 1,sort = True)

big_df = big_df.replace('0',pd.np.nan)
big_df = big_df.dropna(how='any')

#print(big_df)

### Test for normality ###
bignump = big_df.to_numpy().astype(float)
#print(len(bignump))
not_normal_list = []
for i in range(0,len(bignump)):
    if scipy.stats.shapiro(bignump[i])[1] > 0.05:
        #print(i, "is not normally distributed",bignump[i])
        not_normal_list.append(i)


### splitting data into alive and dead categories ###
alive_samples = big_df.iloc[:,0:8]
dead_samples = big_df.iloc[:,8:]

### Test for Equal Variances ###
alivenump = alive_samples.to_numpy().astype(float)
deadnump = dead_samples.to_numpy().astype(float)

# =============================================================================
# unequal_variances_list = []
# for i in range(0,len(alivenump)):
#     if scipy.stats.bartlett((alivenump[i]),(deadnump[i]))[1] > 0.05:
#         unequal_variances_list.append(i)
#     else:
#         continue
# =============================================================================


### Testing each gene for significant difference between alive and dead group (Two-Tailed) ###
signif_list = []
plot_statistics = []
for i in range(0,len(alivenump)):
# =============================================================================
#     if i in unequal_variances_list and i not in not_normal_list:
#         if (scipy.stats.ttest_ind(alivenump[i],deadnump[i],equal_var=False)[1]) < 0.15:
#             signif_list.append(i)
# =============================================================================
# =============================================================================
#     if i in not_normal_list:
#         if (scipy.stats.wilcoxon(alivenump[i],deadnump[i][0:8])[1]) < 0.15:
#             print(scipy.stats.wilcoxon(alivenump[i],deadnump[i][0:8]))
#             signif_list.append(i)
#     elif i not in not_normal_list:
# =============================================================================
    plot_statistics.append(scipy.stats.ttest_ind(alivenump[i],deadnump[i])[0])
    if (scipy.stats.ttest_ind(alivenump[i],deadnump[i])[1]) < 0.20:
       signif_list.append(i)

df = 15
points = np.linspace(scipy.stats.t.ppf(0.01,df),scipy.stats.t.ppf(0.99,df),1000)
rv = scipy.stats.t(df)
# =============================================================================
# plt.plot(points,rv.pdf(points))
# plt.scatter(plot_statistics,rv.pdf(plot_statistics),c='red')
# plt.axvline(x=-1.341,c='green')
# plt.axvline(x=1.341,c='green')
# plt.title("T-distribution, df = 15",fontsize=18)
# plt.xlabel("T",fontsize=15)
# plt.ylabel("Propability density",fontsize=16)
# =============================================================================

### Subsetting data into k-categories based on p-value thresholds listed above ###
regression_df = big_df.iloc[signif_list]
x = (regression_df.transpose().to_numpy().astype(float))
y = np.append(np.repeat(0,8),np.repeat(1,9))
k = 3
k_sets = np.array_split(x,k)
indices = np.random.permutation(x.shape[0])

sets = np.array_split(indices,k)

gene_of_interest = 2
accuracies = []
precisions = []
plotting_vals = []
plotting_types = []
plotting_theta = []
for i in range(len(sets)):
	test_set = sets[i]
	training_set = np.concatenate(np.delete(sets,i))
	test_samples = x[test_set]
	test_types = y[test_set]
	training_samples = x[training_set]
	training_types = y[training_set]
	model = lm.logistic_model(training_samples,training_types,0.01)
	model.gradient_descent(10000,0.00001)
	true_positives = 0
	true_negatives = 0
	false_negatives = 0
	false_positives = 0
	print(model.thetas)
	for j in range(len(test_samples)):
		print("Predicted Class:",model.predict_classification(test_samples[j]),"\tActual Class:",test_types[j])
		if model.predict_classification(test_samples[j]) >= 0.50 and test_types[j] == 1:
			true_positives += 1
		elif model.predict_classification(test_samples[j]) >= 0.50 and test_types[j] == 0:
			false_positives += 1
		elif model.predict_classification(test_samples[j]) < 0.50 and test_types[j] == 0:
			true_negatives += 1
		elif model.predict_classification(test_samples[j]) < 0.50 and test_types[j] == 1:
			false_negatives += 1
		plotting_vals.append(test_samples[j][gene_of_interest])
		plotting_types.append(test_types[j])
	plotting_theta.append(model.thetas[gene_of_interest])
	accuracies.append((len(test_set)/len(x))*(true_positives + true_negatives)/(true_positives + true_negatives + false_negatives + false_positives))
	precisions.append((len(test_set)/len(x))*(true_positives)/(true_positives + false_positives))
# =============================================================================
# 	fig = plt.figure()
# 	plt.plot(model.J_list)
# 	fig.suptitle("J vs. Iteration #",fontsize=18)
# 	plt.xlabel("Iteration #",fontsize=16)
# 	plt.ylabel("Cost J",fontsize=16)
# =============================================================================

plot_thet = mean(plotting_theta)
plot_vals = []
lin_x = np.arange(-3,4,0.01)
for x in lin_x:
	plot_vals.append(1/(1+exp(-x *plot_thet)))
plt.scatter(plotting_vals,plotting_types,c='red')
plt.plot(lin_x,plot_vals)
plt.title("Probability of Good Prognosis with Gene X",fontsize=18)
plt.xlabel("Gene Expression (Z-score)",fontsize=15)
plt.ylabel("Probability of Good Prognosis",fontsize=16)
print("Model Accuracy:",sum(accuracies))
print("Model Precision:",sum(precisions))



