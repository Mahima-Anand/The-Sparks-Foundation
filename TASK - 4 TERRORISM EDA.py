#TASK 4 - TERRORISM
#import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from simple_colors import *
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
from scipy import signal


# %%
df = pd.read_csv(r'C:\Users\HP\Documents\DS\Sparks\globalterrorism.csv', encoding='ISO-8859-1')
df.isnull().sum()


# %%
dfcopy = df.copy()
dfcopy.head()
dfcopy.dropna(axis = 1, how = 'all')


# %%
dfcopy.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','provstate':'state',
                       'region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed',
                       'nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type',
                       'weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)


# %%
dfcopy=dfcopy[['Year','Month','Day','Country','state','Region','city','latitude','longitude','AttackType','Killed',
               'Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]

#filling the null value with zero
dfcopy['Wounded'] = dfcopy['Wounded'].fillna(0).astype(int)
dfcopy['Killed'] = dfcopy['Killed'].fillna(0).astype(int)   


# %%
dfcopy.shape
dfcopy.isnull().sum()


# %%
count = 0
for i in dfcopy['Day']:
    if (i==0):
      count+=1
    else:
      count=count
print("Number of days entered as 0: ",count)

count1=0
for j in dfcopy['Month']:
    if (j==0):
      count1+=1
    else:
      count1=count1
print("Number of months enterd as 0: ",count1)


# %%
dfcopy['Day']=dfcopy['Day'].apply(lambda x: np.random.randint(1,32) if x == 0 else x)
dfcopy['Month']=dfcopy['Month'].apply(lambda x: np.random.randint(1,13) if x == 9 else x)


# %%
#Checking for days
count = 0
for i in dfcopy['Day']:
    if (i == 0):
      count+=1
    else:
      count=count
print("Number of days entered as 0: ",count)

#Count for months
count1=0
for j in dfcopy['Month']:
    if (j==0):
      count1+=1
    else:
      count1=count1
print("Number of months enterd as 0: ",count1)


# %%
#missing value percentage
def null_val_(dfcopy): 
    null_val = dfcopy.isnull().sum()
    null_val_p = 100 * dfcopy.isnull().sum()/len(dfcopy)
    null_val_ = pd.concat([null_val, null_val_p], axis=1)
    null_val_last = null_val_.rename(
    columns = {0 : 'Null Values', 1 : 'Percentage '})
    return null_val_last
null_val_(dfcopy)


# %%
dfcopy['Motive'].fillna(value='NA', inplace=True) 
dfcopy['Summary'].fillna(value='NA', inplace=True)
dfcopy['Target'].fillna(value='NA', inplace=True)
dfcopy["longitude"].fillna(dfcopy["longitude"].mean(), inplace=True)
dfcopy["latitude"].fillna(dfcopy["latitude"].mean(), inplace=True)
dfcopy['city'].fillna(value='NA', inplace=True)
dfcopy['state'].fillna(value='NA', inplace=True)
dfcopy.isnull().sum()


# %%
print("The country with highest terror attack: \033[1m"+red(dfcopy['Country'].value_counts().index[0])+"\033[0m")
print("Regions with highest terrorist attacks: \033[1m"+green(dfcopy['Region'].value_counts().index[0])+"\033[0m")
print("Highest people killed in an attack \033[1m",blue(dfcopy['Killed'].max()),"\033[0m","that took place in \033[1m"+red(dfcopy.loc[dfcopy['Killed'].idxmax()].Country)+"\033[0m")
print("City with the highest number of attacks: \033[1m"+red(dfcopy['city'].value_counts().index[1])+"\033[0m")
print("Year with the most attacks: \033[1m",blue(dfcopy['Year'].value_counts().idxmax()),"\033[0m")
print("Month with the most attacks: \033[1m"+cyan(dfcopy['Month'].value_counts().idxmax())+"\033[0m")
print("Group with the most attacks: \033[1m"+magenta(dfcopy['Group'].value_counts().index[1])+"\033[0m")
print("Most Attack Types: \033[1m"+cyan(dfcopy['AttackType'].value_counts().idxmax())+"\033[0m")


# %%
f,ax = plt.subplots(figsize=(8,8))
sns.heatmap(dfcopy.corr(),cmap="summer",annot=False, linewidths=.4, fmt =".1f=", ax=ax)


# %%
plt.subplots(figsize=(15,6))
sns.countplot('Year',data=dfcopy,palette="Reds",edgecolor=sns.color_palette('dark',7))
plt.xticks(rotation=90)
plt.title("Number of Terrorist Activity each Year")
plt.show()


# %%
plt.subplots(figsize=(15,6))
sns.countplot('AttackType',data=dfcopy,palette='jet_r',order=dfcopy['AttackType'].value_counts().index)
plt.xticks(rotation=90)
plt.title("Attacking methods by terrorists")
plt.show()


# %%
plt.subplots(figsize=(15,6))
sns.countplot('Target_type',data=dfcopy,palette='cividis',order=dfcopy['Target_type'].value_counts().index)
plt.xticks(rotation=90)
plt.title("Favorite Targets")
plt.show()


# %%
sns.countplot('Region',data=dfcopy,palette='Paired',edgecolor=sns.color_palette('dark',7),order=dfcopy['Region'].value_counts().index)
plt.xticks(rotation=90)
plt.title('Number Of Terrorist Activities By Region')
plt.show()


# %%
terror_region=pd.crosstab(dfcopy.Year,dfcopy.Region)
terror_region.plot(color=sns.color_palette('nipy_spectral_r',12))
fig=plt.gcf()
fig.set_size_inches(18,6)
plt.show()


# %%
pd.crosstab(dfcopy.Region,dfcopy.AttackType).plot.barh(stacked=True,width=1,color=sns.color_palette('RdYlBu',9))
fig=plt.gcf()
fig.set_size_inches(12,8)
plt.title("Attack types in each country")
plt.show()


# %%
plt.subplots(figsize=(18,6))
sns.barplot(dfcopy['Country'].value_counts()[:15].index,dfcopy['Country'].value_counts()[:15].values,palette='rainbow')
plt.title('Top Affected Countries')
plt.show()


# %%
f,ax = plt.subplots(figsize=(18,10))
dfcopy.Killed.plot(kind="line",color = "r", label="number of kills",linewidth=5, alpha=0.5, grid=True, linestyle=":")
dfcopy.Wounded.plot(color="b", label="number of wounds",linewidth=5, alpha=0.5, grid=True,linestyle=":")
plt.legend(loc="upper right")
plt.xlabel("Number of attacks", size=15)
plt.ylabel("People", size=15)
plt.title("Line Plot - number of attacks and how much people are wounded and killed")


# %%
coun_terror=dfcopy['Country'].value_counts()[:15].to_frame()
coun_terror.columns=['Attacks']
coun_kill=dfcopy.groupby('Country')['Killed'].sum().to_frame()
coun_terror.merge(coun_kill,left_index=True,right_index=True,how='left').plot.bar(width=0.9)
fig=plt.gcf()
fig.set_size_inches(18,6)
plt.title('number of attacks the no. of people killed')
plt.show()


# %%
sns.lmplot(x='Year', y='Killed',data=dfcopy,fit_reg=False,hue='Weapon_type',legend=True ,                    
           palette="rainbow",aspect=15/10)
plt.xlabel("year")
plt.ylabel("kills") 
plt.title("Year vs Kill Scatter Plot")


# %%
sns.barplot(dfcopy['Group'].value_counts()[1:15].values,dfcopy['Group'].value_counts()[1:15].index,palette=('cubehelix'))
plt.xticks(rotation=90)
fig=plt.gcf()
fig.set_size_inches(10,8)
plt.title('Terrorist Organisation with Highest Terror Attacks')
plt.show()


# %%
dfcopy = dfcopy[dfcopy.Group == 'Taliban']


# %%
plt.figure(figsize = (13,7))
sns.barplot(dfcopy['Year'].value_counts().index,dfcopy['Year'].value_counts().values, palette = 'viridis')
plt.title('Terror Attack over the years by Taliban',fontsize=15)
plt.xlabel('Years',fontsize=15)
plt.ylabel('Number of Attacks',fontsize=15)
plt.xticks(rotation= 70)
plt.grid()
plt.show()


# %%
plt.figure(figsize=(13,7))
dfcopy.groupby(['Year'])['Killed'].sum().plot(kind='bar',colormap='rainbow')
plt.title('People Killed by Taliban over the Years',fontsize=15)
plt.xlabel('Years',fontsize=15)
plt.ylabel('Number of people killed',fontsize=15)
plt.xticks(rotation=70)
plt.grid()
plt.show()


