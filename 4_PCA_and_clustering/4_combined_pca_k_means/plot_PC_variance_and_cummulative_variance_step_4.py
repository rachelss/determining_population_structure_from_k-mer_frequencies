import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from os import listdir
from os.path import isfile, join
import pickle


#read files into a dictionary
pickled_dictionary_filtered = '/data/schwartzlab/yana/human_VCF_1000_genome_project/WGS_files_from_1000_human_genome_project/PCA_analysis/pickles/k_21_WGS_18_with_1_super_pop_3_sub_pop_w_admixed_populations_intersection_across.p'
kmer_frequencies_dictionary = pickle.load(open( pickled_dictionary_filtered, "rb"))

df = pd.DataFrame(kmer_frequencies_dictionary)


features = df.columns.tolist()[0:-1] #['AAAAAAAAAAAAAAAAAAAAA', ... , 'TTTTTTTTTTCAAAAAAAAAA']

x = df.loc[:, features].values
#y = df.loc[:,['Population']].values
std_x = StandardScaler().fit_transform(x) # Standardize the data to have a mean of ~0 and a variance of 1

#select first 13 PCs of the data to plot the barplot to see the variance
pca = PCA(n_components=19)
principalComponents = pca.fit_transform(std_x)

print(pca.explained_variance_ratio_) #print to a file

#plot the bar plot of the 19 PCs
PC = range(1, pca.n_components_+1)
plt.bar(PC, pca.explained_variance_ratio_, color='gold')
plt.xlabel('Principal Components')
plt.ylabel('Variance %')
plt.xticks(PC)
plt.savefig("plot_variance_19_PCs_1_super_pop_3_pop_w_admixed_EAS_21mers.pdf")

#plot the cumulative variance explained
plt.figure(figsize = (12,9))
plt.plot(PC, pca.explained_variance_ratio_.cumsum(), marker = 'o', linestyle = '--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.xticks(PC)
plt.savefig("Cumulative_Explained_Variance_1_super_pop_3_pop_w_admixed_EAS_21_mers.pdf")
plt.clf()
