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
#path_to_pickled_dictionary = sys.argv[1] #/data/schwartzlab/yana/human_VCF_1000_genome_project/WGS_files_from_1000_human_genome_project/PCA_analysis

pickled_dictionary_filtered = '/data/schwartzlab/yana/human_VCF_1000_genome_project/WGS_files_from_1000_human_genome_project/PCA_analysis/pickles/k_21_WGS_8_with_admixed_populations_intersection_across.p'
kmer_frequencies_dictionary = pickle.load( open( pickled_dictionary_filtered, "rb" ) )

#TODO: sort dictionary by keys() and make sure that vals are sorted too by files processesed
#Q: do I need to sort dictionary by keys? probably not


df = pd.DataFrame(kmer_frequencies_dictionary)



population = ['AMR_PEL', 'AMR_PEL', 'AMR_PEL', 'AMR_PEL', 'AMR_PEL', 'AMR_PEL',
              'EAS_CDX', 'EAS_CDX', 'EAS_CDX', 'EAS_CDX', 'EAS_CDX', 'EAS_CDX',
              'EAS_CHB', 'EAS_CHB', 'EAS_CHB', 'EAS_CHB', 'EAS_CHB', 'EAS_CHB', #admixed samples
              'EAS_JPT', 'EAS_JPT', 'EAS_JPT', 'EAS_JPT', 'EAS_JPT', 'EAS_JPT',
              'EUR_CEU', 'EUR_CEU', 'EUR_CEU', 'EUR_CEU', 'EUR_CEU', 'EUR_CEU', #admixed samples
              'EUR_FIN', 'EUR_FIN', 'EUR_FIN', 'EUR_FIN', 'EUR_FIN', 'EUR_FIN',
              'EUR_TSI', 'EUR_TSI', 'EUR_TSI', 'EUR_TSI', 'EUR_TSI', 'EUR_TSI',
              'SAS_ITU', 'SAS_ITU', 'SAS_ITU', 'SAS_ITU', 'SAS_ITU', 'SAS_ITU'] #we dont specify by sample number because there are only 4 populations and we want to have 4 clusters?

df['Population'] = population

features = df.columns.tolist()[0:-1] #['AAAAAAAAAAAAAAAAAAAAA', ... , 'TTTTTTTTTTCAAAAAAAAAA']

x = df.loc[:, features].values
y = df.loc[:,['Population']].values
std_x = StandardScaler().fit_transform(x)

#print(pd.DataFrame(data = x, columns = features).head())

pca = PCA(n_components = 2)
principalComponents = pca.fit_transform(std_x)

principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

finalDf = pd.concat([principalDf, df[['Population']]], axis = 1) #add a column with populations


#Visualize 2D Projection
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100), fontsize = 11)
ax.set_ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100), fontsize = 11)

targets = ['AMR_PEL', 'EAS_CDX', 'EAS_CHB', 'EAS_JPT', 'EUR_CEU', 'EUR_FIN', 'EUR_TSI', 'SAS_ITU'] #make sure they are listed in the correct order
colors = ['#fc3376', '#d42828', '#ff6700', '#ffda3c', '#000000', '#674ea8', '#660000', '#ea9990'] #['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'] #['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'] #is white visible?
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['Population'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()

plt.savefig("2D_PCA_8_with_admixed_populations_48_samples_from_kmer_freqs_new_colors.pdf")
plt.clf() #clear the plt variable so the plots don't overlap


#Clustering with K-means
inertias = []
ks = range(1, 10)
# Creating 10 K-Mean models while varying the number of clusters (k)
for k in range(1,10):
    model = KMeans(n_clusters=k)

    # Fit model to samples
    model.fit(finalDf.iloc[:,:2])

    # Append the inertia to the list of inertias
    inertias.append(model.inertia_)

plt.plot(range(1,10), inertias, '-p', color='gold')
plt.xlabel('number of clusters, k')
plt.ylabel('inertia')
plt.xticks(ks)
plt.savefig("elbow_method_plot_k_means_8_pops_w_admixed_21_mer_param.pdf")
plt.clf() #clear the plt variable so the plots don't overlap

model = KMeans(n_clusters=4)#from elbow method
model.fit(finalDf.iloc[:,:2])

labels = model.predict(finalDf.iloc[:,:2])
plt.scatter(finalDf['principal component 1'], finalDf['principal component 2'], c=labels)
plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100), fontsize = 11)
plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100), fontsize = 11)
plt.savefig("k_means_clustering_8_pops_w_admixed_21_mers_param.pdf")

plt.clf() #clear the plt variable so the plots don't overlap
