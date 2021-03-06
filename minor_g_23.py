# -*- coding: utf-8 -*-
"""Minor G_23

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_1JzVqt7Bx2g2fYl0YcVdluOotprqbd9

# Jaypee Institute of Information Technology

## Minor Project Group Number- 23

## Team Members-:<br />
Teghdeep Kapoor  18104050 <br />
Vardhika Jain 18104051<br />
Tanya Pandhi  18104064

---

## COURSE RECOMMENDATION SYSTEM TO IMPROVE LEARNING RATE OF STUDENTS IN THE COVID SCENARIO

In higher education, Courses ought to provide a deeper insight of the trending advancements in the field of specialization for undergraduate students. Making choice of elective courses during the pre-final or final year of the undergraduates play a crucial role as it helps in shaping their career or area of specialization for the better learning. However, as per the current educational scenarios, the undergraduates remain mostly confused on what to choose as they either lack in having the sufficient initial knowledge of the elective subjects or are having knowledge overflow of all subjects and so are unable to decide which one to choose. In such scenarios, they often seek the advice of their instructors or friends and mostly go with the cohort choice. However, going with the flow often creates a gap between their actual skills set and the required skills set for the elective subject that they have preferred as their choice. In later stages, this results in loss of interest of the students in the enrolled elective subject and hence a degraded academic performance is encountered by the institution. Similarly, as a result of this, there can be numerous limitations, gaps or concerns arising either in case of students or institutions in real world educational scenarios. A personalized recommender system recommends efficient course subjects to the students that indirectly predicts the academic success of different courses beforehand and along with this also preserves the student subject interests.

### Importing Pandas and Numpy for Data Preprocessing
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import tree

"""### Reading Data"""

url='https://raw.githubusercontent.com/IntellectualCoders/Minor-project/master/FinalData.csv'
df=pd.read_csv(url)

df

"""### Removing NaN values from Data"""

print(df.shape)
df.dropna(inplace=True,how='any')
print(df.shape)

df.info()

df['Preference Of Elective'].unique()

df.groupby(['Preference Of Elective']).mean()

"""### Data manipulation converting categorical data into dummy variables"""

pref = pd.get_dummies(df['Preference Of Elective'])
alc = pd.get_dummies(df['Alloted Elective'])

pref

alc

df1 = pd.concat([df,alc],ignore_index=False,axis=1,verify_integrity=False)

df1.shape

"""### Renaming Colums for Better Understanding"""

df1.rename(columns={'AR_VR':'A_AR_VR','CC':'A_CC','CS':'A_CS','IOT':'A_IOT','ML':'A_ML','NLP':"A_NLP",'SVV':"A_SVV"},inplace=True)

df1

df2 = pd.concat([df1,pref],axis=1)

df2.drop(['Preference Of Elective','Alloted Elective'],axis=1,inplace=True)

df2.shape

df2.columns

df2.rename(columns={'AR_VR':"P_AR_VR",'CC':"P_CC",'CS':"P_CS",'IOT':"P_IOT",'ML':"P_ML",'NLP':"P_NLP",'SVV':"P_SVV"},inplace=True)

df2

"""---

## Data Visualization
"""

from sklearn.decomposition import PCA

pca = PCA(n_components=2)

cols= list(df2.columns.values)

df1['Alloted Elective'] = pd.Categorical(pd.factorize(df1['Alloted Elective'])[0] + 1)
df1['Preference Of Elective'] = pd.Categorical(pd.factorize(df1['Preference Of Elective'])[0] + 1)
df1

df_visual = df1[cols[1:11]]
df_visual

principalComponents = pca.fit_transform(df_visual)

principal_Df = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2 '])
allotelect = pd.Categorical(pd.factorize(df1['Alloted Elective'])[0] + 1)
prefelect = pd.Categorical(pd.factorize(df1['Preference Of Elective'])[0] + 1)
df12= pd.DataFrame(data= prefelect, columns=['hue2'])
df11= pd.DataFrame(data = allotelect, columns=['hue'])
df11

principal_Df = pd.concat([principal_Df,df11,df12],axis=1)

principal_Df.tail()

print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

plt.figure(figsize=(16,10))
sns.scatterplot(
    x='principal component 1',
    y=principalComponents[:,1],
    palette=sns.color_palette("hls", 7),
    hue = 'hue',
    data = principal_Df,
    legend="full"
)

plt.figure(figsize=(16,10))
sns.scatterplot(
    x='principal component 1',
    y=principalComponents[:,1],
    palette=sns.color_palette("hls", 7),
    hue = 'hue2',
    data = principal_Df,
    legend="full"
)

"""---
<br />

## Rank 1 Calculation

### User to User Collaborative Filtering
"""

test =[54.0,	55.0,	19.0,	14.0,	47.0,	48.0,	15.0,	55.0,	45.0,	43.0]

cols= list(df2.columns.values)

df3 = df2[cols[1:11]]
df3

"""### Calculating Cosine Similarity of Active Student with past students data"""

from scipy import spatial

df4 = pd.DataFrame(columns = ['Cosine Similarity']) 
for ind,rows in df3.iterrows():
  a = spatial.distance.cosine(test,rows)
  df4 = df4.append({'Cosine Similarity':a}, ignore_index = True) 
df4

df5 = pd.concat([df1,df4],ignore_index=False,axis=1,verify_integrity=False)
df5=df5.sort_values(by=['Cosine Similarity'])
df5

"""### Selecting top 5 percent data similar to student"""

df6 = pd.DataFrame(columns = ['Cosine Similarity']) 
for ind,rows in df5.iterrows():
  if rows['Cosine Similarity'] <= 0.05:
   df6 = df6.append({'Student_ID': rows['Student_ID'],'Alloted Elective': rows['Alloted Elective'] ,'Marks In Alloted Elective': rows['Marks In Alloted Elective'],'Cosine Similarity':rows['Cosine Similarity']}, ignore_index = True) 
df6

"""### Calculating Mean for each Elective """

SVV_avg = df6.loc[df6['Alloted Elective']== 1]

CS_avg = df6.loc[df6['Alloted Elective']== 2]

CC_avg = df6.loc[df6['Alloted Elective']== 3]

AR_VR_avg = df6.loc[df6['Alloted Elective']== 4]

ML_avg = df6.loc[df6['Alloted Elective']== 5]

NLP_avg = df6.loc[df6['Alloted Elective']== 6]

IOT_avg = df6.loc[df6['Alloted Elective']== 7]

rank1 = [
 AR_VR_avg['Marks In Alloted Elective'].mean(),
CC_avg['Marks In Alloted Elective'].mean(),
CS_avg['Marks In Alloted Elective'].mean(),
IOT_avg['Marks In Alloted Elective'].mean(),
ML_avg['Marks In Alloted Elective'].mean(),
NLP_avg['Marks In Alloted Elective'].mean(),
SVV_avg['Marks In Alloted Elective'].mean()]

rank1

"""### Calculating KNN Weighted Average for each elective"""

SVV_count=0
SVV_sum=0
for i,row in SVV_avg.iterrows():
  SVV_sum = SVV_sum + (1-row['Cosine Similarity'])
  SVV_count = SVV_count + (row['Marks In Alloted Elective'] * (1-row['Cosine Similarity']))
SVV_final = SVV_count/SVV_sum
SVV_final

CS_count=0
CS_sum=0
for i,row in CS_avg.iterrows():
  CS_sum = CS_sum + (1-row['Cosine Similarity'])
  CS_count = CS_count + (row['Marks In Alloted Elective'] * (1-row['Cosine Similarity']))
CS_final = CS_count/CS_sum
CS_final

"""---

## Rank 2 Calculation

### Categorization of Data
Estimation of Marks to nearest multiple of 5
"""

for ind,rows in df2.iterrows():   # binning the marks in allocated
    rows['Marks In Alloted Elective'] = rows['Marks In Alloted Elective']-rows['Marks In Alloted Elective']%5 
    df2.loc[ind,'Marks In Alloted Elective'] = rows['Marks In Alloted Elective']

cols= list(df2.columns.values)

"""### Spiliting of Training and Testing Data"""

df2

X = df2[cols[20:27] +cols[1:11]]
Y = df2[cols[13:20]]
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2, random_state = 0)

Y_train

X_train

"""## Applying Educational Data Mining Techniques

### Applying Decision Tree Classifier
"""

from sklearn.tree import DecisionTreeClassifier

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_SVM_train,Y_SVM_train)

clf.score(X_SVM_train,Y_SVM_train)

clf.get_depth()

"""### Prediciting Test Data"""

from sklearn.metrics import classification_report, confusion_matrix

Y_pred = clf.predict(X_SVM_test)

Y_pred

"""### Accuracy of Decision Tree"""

from sklearn import metrics

print("Accuracy:",metrics.accuracy_score(Y_SVM_test, Y_pred))

print(classification_report(Y_SVM_test,Y_pred))

"""### Displaying Decision Tree"""

from sklearn.metrics import confusion_matrix
mat = confusion_matrix(Y_SVM_test, Y_pred)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=df11.iloc[:,0].unique(), yticklabels=df11.iloc[:,0].unique())
plt.xlabel('true label')
plt.ylabel('predicted label');

"""### Applying SVM Classifier"""

from sklearn import svm
from sklearn import metrics

df1
cols_SVM= list(df1.columns.values)

df1['Alloted Elective'] = pd.Categorical(pd.factorize(df1['Alloted Elective'])[0] + 1)
df1['Preference Of Elective'] = pd.Categorical(pd.factorize(df1['Preference Of Elective'])[0] + 1)
df1

X_SVM = df1[ cols_SVM[1:12]]
Y_SVM = df1[cols_SVM[12]]
X_SVM

Y_SVM

X_SVM_train,X_SVM_test,Y_SVM_train,Y_SVM_test = train_test_split(X_SVM,Y_SVM,test_size=0.2,random_state=0)

"""### Fitting SVM Model"""

clf_SVM = svm.SVC(kernel = 'linear', C = 1)
clf_SVM.fit(X_SVM_train, Y_SVM_train)

y_SVM_pred = clf_SVM.predict(X_SVM_test)
y_SVM_pred

"""### Visualization of SVM Model"""

from sklearn.metrics import confusion_matrix
mat = confusion_matrix(Y_SVM_test, y_SVM_pred)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=df11.iloc[:,0].unique(), yticklabels=df11.iloc[:,0].unique())
plt.xlabel('true label')
plt.ylabel('predicted label');

"""### Accuracy of SVM Classifier"""

from sklearn.metrics import classification_report, confusion_matrix

print("Accuracy:",metrics.accuracy_score(Y_SVM_test, y_SVM_pred))

print(classification_report(Y_SVM_test,y_SVM_pred))

"""## KNN (k-nearest neighbours) classifier """

from sklearn.neighbors import KNeighborsClassifier

X_SVM_train

Y_SVM_train

"""### Fitting KNN model"""

knn = KNeighborsClassifier(n_neighbors = 1).fit(X_SVM_train, Y_SVM_train)

knn_predictions = knn.predict(X_SVM_test)
knn_predictions

"""### Accuracy of KNN Model"""

accuracy = knn.score(X_SVM_test, Y_SVM_test) 
accuracy

print("Accuracy:",metrics.accuracy_score(Y_SVM_test, knn_predictions))

print(classification_report(Y_SVM_test,knn_predictions))

"""### Model Visualization of KNN"""

from sklearn.metrics import confusion_matrix
mat = confusion_matrix(Y_SVM_test, knn_predictions)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=df11.iloc[:,0].unique(), yticklabels=df11.iloc[:,0].unique())
plt.xlabel('true label')
plt.ylabel('predicted label');

"""## Naive Bayes classifier"""

from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB().fit(X_SVM_train, Y_SVM_train) 
gnb_predictions = gnb.predict(X_SVM_test)
gnb_predictions

"""### Accuracy of Naive Bayes Classifier"""

accuracy = gnb.score(X_SVM_test, Y_SVM_test)
accuracy

print(classification_report(Y_SVM_test,gnb_predictions))

"""### Naive Bayes Model Visualization"""

from sklearn.metrics import confusion_matrix
mat = confusion_matrix(Y_SVM_test, gnb_predictions)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=df11.iloc[:,0].unique(), yticklabels=df11.iloc[:,0].unique())
plt.xlabel('true label')
plt.ylabel('predicted label');

"""### Prediciting Allotted Elective"""

testnb = [54.0,	55.0,	19.0,	14.0,	47.0,	48.0,	15.0,	55.0,	45.0,	43.0, 2]
testnb2 = [testnb]

test_pred = gnb.predict(testnb2)
test_pred[0]

naivebase=[0]*7
for i in range(1,8):
  if i == test_pred[0]:
    naivebase[i-1] = naivebase[i-1]+100
naivebase

"""

---

<br />

## Rank 3 Calculation"""

#Calculating the count of the all Electives
SVV_count = df2.loc[df['Preference Of Elective']== 'SVV' ]

CS_count = df2.loc[df['Preference Of Elective']== 'CS']

CC_count = df2.loc[df['Preference Of Elective']== 'CC']

AR_VR_count = df2.loc[df['Preference Of Elective']== 'AR_VR']

ML_count = df2.loc[df['Preference Of Elective']== 'ML']

NLP_count = df2.loc[df['Preference Of Elective']== 'NLP']

IOT_count = df2.loc[df['Preference Of Elective']== 'IOT']
SVV_count2 = SVV_count.loc[SVV_count['Marks In Alloted Elective'] >= 90]
CS_count2 = CS_count.loc[CS_count['Marks In Alloted Elective'] >= 90]
CC_count2 = CC_count.loc[CC_count['Marks In Alloted Elective'] >= 90]
AR_VR_count2 = AR_VR_count.loc[AR_VR_count['Marks In Alloted Elective'] >= 90]
ML_count2 = ML_count.loc[ML_count['Marks In Alloted Elective'] >= 90]
NLP_count2 = NLP_count.loc[NLP_count['Marks In Alloted Elective'] >= 90]
IOT_count2 = IOT_count.loc[IOT_count['Marks In Alloted Elective'] >= 90]

rank3= [AR_VR_count2['Student_ID'].count()/AR_VR_count['Student_ID'].count(),
         CC_count2['Student_ID'].count()/CC_count['Student_ID'].count(),
CS_count2['Student_ID'].count()/CS_count['Student_ID'].count(),
IOT_count2['Student_ID'].count()/IOT_count['Student_ID'].count(),
ML_count2['Student_ID'].count()/ML_count['Student_ID'].count(),
NLP_count2['Student_ID'].count()/NLP_count['Student_ID'].count(),
SVV_count2['Student_ID'].count()/SVV_count['Student_ID'].count()]

rank3

"""

---

<br />


## Weighted Rank Calculation"""

rank1f = [x * 0.7 for x in rank1]
rank1f

rank2 = [x * 0.05 for x in naivebase]
rank2

rank3f = [x * 25 for x in rank3]
rank3f

WR = [] 
for i in range(0, len(rank1f)): 
    WR.append(rank1f[i] + rank2[i]+ rank3f[i]) 
WR

dict = {'Electives':['AR_VR', 'CC', 'CS', 'IOT','ML','NLP','SVV'],  
       } 
df9 = pd.DataFrame(WR)
df7 = pd.DataFrame(dict)
df8 = pd.concat([df7,df9],ignore_index=False,axis=1,verify_integrity=False)
df8

"""## Final Order of Electives for Student"""

df10=df8.sort_values(by=0, ascending=False)
df10