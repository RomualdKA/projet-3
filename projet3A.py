#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 19:40:07 2020

@author: formateur
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
import seaborn as sns
fn='/home/formateur/Bureau/chucknoris.csv'
Chuck = pd.read_csv(fn)
print(Chuck)

#Nous allons à faire l'etude statistiques de nos données
#Chuck.head()
#Chuck['class'].value_counts()
#Chuck.count()
#Chuck.shape
#Chuck.describe()
#Chuck['Note sur 5'].hist()
#Chuck['Nombre de votes'].hist()
#sns.distplot

#Cette etape me permet de faire la statistique descriptive de mes données
#Chuck["lib_zone"].describe()
#Chuck1=Chuck.groupby(['Blague']).mean()[['Note sur 5','Nombre de votes']]
#Chuck1.plot.bar(stacked=False)
#Allons un peu plus loin dans notre analyse descriptive 
#Chuck.groupby(['Blague','Note sur 5','Nombre de votes']).mean()

#Chuck['Blague','Note sur 5'].hist()
#Chuck['Nombre de votes','Note sur 5'].hist()

#A présent calculons la correlation 
#k = pd.DataFrame()
#k['Nombre de votes'] = np.arange(5)+3
#k['Note sur 5'] = [1, 2, 3, 4, 5]
#pyplot.scatter(k['Nombre de votes'], k['Note sur 5'], s = 150, c = 'red', marker = '*', edgecolors = 'blue')
#del Chuck['Blague']
#print(Chuck)
#del Chuck['Id']
#Chuck.corr()
#k.corr('pearson')
#Chuck.corr(method='pearson')

#Chuck.corr(method='spearman')
#sns.heatmap(Chuck.corr())
#print(Chuck2.corr())
Chuck2=Chuck[['Note sur 5','Nombre de votes']]
sns.heatmap(Chuck2.corr(), annot=True)
#df.corr(method='spearman')
sns.scatterplot(Chuck2['Nombre de votes'],Chuck2['Note sur 5'],color='red')
	
#Chuck.corr(method='spearman').style.format("{:.2}").background_gradient(cmap=pyplot.get_cmap('coolwarm'))
#pyplot.show
