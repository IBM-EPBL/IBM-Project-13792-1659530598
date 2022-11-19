# -*- coding: utf-8 -*-
"""ckd (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ppYiKchD6LuvRMP7XtjR3V8KVOVfx8S4

## Importing Libaries
"""

import pandas as pd
import numpy as np 
from collections import Counter as c 
import matplotlib.pyplot as plt
import seaborn as sns 
import missingno as msno 
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder 
from sklearn.linear_model import LogisticRegression
import pickle

"""## Reading the dataset"""

data=pd.read_csv(r"/content/sample_data/chronickidneydisease.csv")   ## Loading the dataset

data.head()

data.tail()

data.drop(["id"],axis=1,inplace=True)  # dropping the column "id"

data.columns

"""# Renaming the columns"""

data.columns=['age','blood_pressure','specific_gravity','albumin','sugar','red_blood_cells','pus_cells',
              'pus_cell_clumps','bacteria','blood glucose random','blood_urea','serum_creatinine','sodium','potassium',
              'haemoglobin','packed_cell_volume','white_blood_cell_count','red_blood_cell_count','hypertension',
              'diabetesmellitus','coronary_artery_disease','appetite','pedal_edema','anemia','class']
data.columns

"""# Understanding datatype"""

data.info()

"""## Target column"""

data['class'].unique()

"""## Rectifying target coulmn"""

data['class']=data['class'].replace("ckd\t","ckd")
data['class'].unique()

categorical_columns=set(data.dtypes[data.dtypes=='O'].index.values)  #fetching object or categorical columns
print(categorical_columns)

for i in categorical_columns:
    print("Columns : ",i)
    print(c[data[i]])
    print("*"*120+'\n')

"""## Removing columns which are not categorical"""

categorical_columns.remove('red_blood_cell_count')
categorical_columns.remove('packed_cell_volume')
categorical_columns.remove('white_blood_cell_count')
print(categorical_columns)

"""## Numerical columns"""

continuous_columns=set(data.dtypes[data.dtypes!='O'].index.values)    #fetching numerical columns
print(continuous_columns)

for i in continuous_columns:
    print("Columns : ",i)
    print(c[data[i]])
    print("*"*120+'\n')

"""## Removing columns which are not numerical"""

continuous_columns.remove('specific_gravity')
continuous_columns.remove('albumin')
continuous_columns.remove('sugar')
print(continuous_columns)

"""## Adding columns which we found continuous"""

continuous_columns.add('red_blood_cell_count')
continuous_columns.add('packed_cell_volume')
continuous_columns.add('white_blood_cell_count')
print(continuous_columns)

"""## Adding columns which we found categorical"""

categorical_columns.add('specific_gravity')
categorical_columns.add('albumin')
categorical_columns.add('sugar')
print(categorical_columns)

"""## Rectifying the categorical column classes"""

data['coronary_artery_disease']=data.coronary_artery_disease.replace('\tno','no')
c(data['coronary_artery_disease'])

data['diabetesmellitus']=data.diabetesmellitus.replace(to_replace={'\tyes':'yes','\tno':'no',' yes':'yes'})
c(data['diabetesmellitus'])

"""## Null values"""

data.isnull().any()          #returns true if column has any missing values

data.isnull().sum()  #returns the count of missing values

data.packed_cell_volume=pd.to_numeric(data.packed_cell_volume,errors='coerce')
data.white_blood_cell_count=pd.to_numeric(data.white_blood_cell_count,errors='coerce')
data.red_blood_cell_count=pd.to_numeric(data.red_blood_cell_count,errors='coerce')

"""##  Handling continuous/numeric columns null values"""

data['blood glucose random'].fillna(data['blood glucose random'].mean(),inplace=True)
data['blood_pressure'].fillna(data['blood_pressure'].mean(),inplace=True)
data['blood_urea'].fillna(data['blood_urea'].mean(),inplace=True)
data['haemoglobin'].fillna(data['haemoglobin'].mean(),inplace=True)
data['packed_cell_volume'].fillna(data['packed_cell_volume'].mean(),inplace=True)
data['potassium'].fillna(data['potassium'].mean(),inplace=True)
data['red_blood_cell_count'].fillna(data['red_blood_cell_count'].mean(),inplace=True)
data['serum_creatinine'].fillna(data['serum_creatinine'].mean(),inplace=True)
data['sodium'].fillna(data['sodium'].mean(),inplace=True)
data['white_blood_cell_count'].fillna(data['white_blood_cell_count'].mean(),inplace=True)

data['age'].fillna(data['age'].mode()[0],inplace=True)
data['hypertension'].fillna(data['hypertension'].mode()[0],inplace=True)
data['pus_cell_clumps'].fillna(data['pus_cell_clumps'].mode()[0],inplace=True)
data['appetite'].fillna(data['appetite'].mode()[0],inplace=True)
data['albumin'].fillna(data['albumin'].mode()[0],inplace=True)
data['pus_cells'].fillna(data['pus_cells'].mode()[0],inplace=True)
data['red_blood_cells'].fillna(data['red_blood_cells'].mode()[0],inplace=True)
data['coronary_artery_disease'].fillna(data['coronary_artery_disease'].mode()[0],inplace=True)
data['bacteria'].fillna(data['bacteria'].mode()[0],inplace=True)
data['anemia'].fillna(data['anemia'].mode()[0],inplace=True)
data['sugar'].fillna(data['sugar'].mode()[0],inplace=True)
data['diabetesmellitus'].fillna(data['diabetesmellitus'].mode()[0],inplace=True)
data['pedal_edema'].fillna(data['pedal_edema'].mode()[0],inplace=True)
data['specific_gravity'].fillna(data['specific_gravity'].mode()[0],inplace=True)

"""## Label encoding"""

from sklearn.preprocessing import LabelEncoder
for i in categorical_columns:
    print("LABEL ENCODING OF:",i)
    Le=LabelEncoder()
    print(c(data[i]))
    data[i]=Le.fit_transform(data[i])
    print(c(data[i]))
    print("*"*100)

"""## Creating dependent and independent variables"""

selected_columns=['red_blood_cells','pus_cells','blood glucose random','blood_urea','pedal_edema','anemia',
                  'diabetesmellitus','coronary_artery_disease']
x=pd.DataFrame(data,columns=selected_columns)
y=pd.DataFrame(data,columns=['class'])
print(x.shape)
print(y.shape)

"""## Splitting the data into train and test"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=2)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

"""## Build a machine learning model"""

from sklearn.linear_model import LogisticRegression 
lgr=LogisticRegression() 
lgr.fit(x_train,y_train)

y_pred=lgr.predict(x_test)
y_pred1=lgr.predict([[129,99,1,0,0,1,0,1]])
print(y_pred)
c(y_pred)

accuracy_score(y_test,y_pred)

"""## Confusion matrix"""

confusion_mat = confusion_matrix(y_test,y_pred)
confusion_mat

"""## Dumping our model into pickle form"""

pickle.dump(lgr,open('CKD.pkl','wb'))

with open('/content/CKD.pkl','rb') as f:
  mp=pickle.load(f)

mp.predict([[129,99,1,1,1,1,0,1]])