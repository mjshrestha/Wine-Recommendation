#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd #Library to handle with dataframes
import matplotlib.pyplot as plt # Library to plot graphics
import numpy as np # To handle with matrices
import seaborn as sns # to build modern graphics
from scipy.stats import kurtosis, skew # it's to explore some statistics of numerical values


# In[2]:


df_wine1 = pd.read_csv('winemag-lngs-lats-precip-temp.csv', index_col=0)


# In[3]:


plt.figure(figsize=(14,6))

country = df_wine1.country.value_counts()[:20]

g = sns.countplot(x='country', data=df_wine1[df_wine1.country.isin(country.index.values)])
g.set_title("Country Of Wine Origin Count", fontsize=20)
g.set_xlabel("Country", fontsize=15)
g.set_ylabel("Wine Count", fontsize=15)
g.set_xticklabels(g.get_xticklabels(),rotation=45)
plt.figure(figsize=(16,12))

plt.subplot(2,1,1)
g = sns.boxplot(x='country', y='price',
                  data=df_wine1.loc[(df_wine1.country.isin(country.index.values))])
g.set_title("Price by Country Of Wine Origin", fontsize=20)
g.set_xlabel("Country", fontsize=15)
g.set_ylabel("Price '$'", fontsize=15)
g.set_xticklabels(g.get_xticklabels(),rotation=45)

plt.subplots_adjust(hspace = 0.8,top = 0.9)

plt.show()


# In[4]:


#Province of wine origin
plt.figure(figsize=(14,15))

country_province = df_wine1['country_province'].value_counts()[:20]

plt.subplot(3,1,1)
g = sns.countplot(x='country_province', 
                  data=df_wine1.loc[(df_wine1.country_province.isin(country_province.index.values))])
g.set_title("Province Of Wine Origin ", fontsize=20)
g.set_xlabel("Country_Provinces", fontsize=15)
g.set_ylabel("Wine Count", fontsize=15)
g.set_xticklabels(g.get_xticklabels(),rotation=90)

plt.subplot(3,1,2)
g1 = sns.boxplot(y='price', x='country_province',
                  data=df_wine1.loc[(df_wine1.country_province.isin(country_province.index.values))])
g1.set_title("Province Of Wine Origin ", fontsize=20)
g1.set_xlabel("Province", fontsize=15)
g1.set_ylabel("Price '$'", fontsize=15)
g1.set_xticklabels(g1.get_xticklabels(),rotation=90)

plt.subplots_adjust(hspace = 1.5,top = 0.9)

plt.show()


# In[5]:


plt.figure(figsize=(14,16))

winery = df_wine1.winery.value_counts()[:20]

plt.subplot(3,1,1)
g = sns.countplot(x='winery', 
                  data=df_wine1.loc[(df_wine1.winery.isin(winery.index.values))])
g.set_title("Top 20 most frequent Winery", fontsize=20)
g.set_xlabel(" ", fontsize=15)
g.set_ylabel("Wine Count", fontsize=15)
g.set_xticklabels(g.get_xticklabels(),rotation=90)

plt.subplot(3,1,2)
g1 = sns.boxplot(y='price', x='winery',
                  data=df_wine1.loc[(df_wine1.winery.isin(winery.index.values))])
g1.set_title("Price by Winery", fontsize=20)
g1.set_xlabel("", fontsize=15)
g1.set_ylabel("Price", fontsize=15)
g1.set_xticklabels(g1.get_xticklabels(),rotation=90)

plt.subplots_adjust(hspace = 1.5,top = 0.9)

plt.show()


# In[6]:


plt.figure(figsize=(14,16))

variety = df_wine1.variety.value_counts()[:20]

plt.subplot(3,1,1)
g = sns.countplot(x='variety', 
                  data=df_wine1.loc[(df_wine1.variety.isin(variety.index.values))])
g.set_title("Top 20 Variety ", fontsize=20)
g.set_xlabel(" ", fontsize=15)
g.set_ylabel("Count", fontsize=15)
g.set_xticklabels(g.get_xticklabels(),rotation=90)

plt.subplot(3,1,2)
g1 = sns.boxplot(y='price', x='variety',
                  data=df_wine1.loc[(df_wine1.variety.isin(variety.index.values))])
g1.set_title("Price by Variety", fontsize=20)
g1.set_xlabel("", fontsize=15)
g1.set_ylabel("Price", fontsize=15)
g1.set_xticklabels(g1.get_xticklabels(),rotation=90)

plt.subplots_adjust(hspace = 1.5,top = 0.9)

plt.show()


# In[ ]:




