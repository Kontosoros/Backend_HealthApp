import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn import  svm
import pickle

df  = pd.read_csv("heart.csv")
df.drop(columns=['cp', 'restecg','caa', 'oldpeak','slp'])
X = df[['age', 'sex',  'trtbps', 'chol', 'fbs',  'thalachh',
       'exng',    'thall',]]

y = df['output']
X_train, X_test, y_train, y_test = train_test_split(X.to_numpy(), y.to_numpy(), test_size=0.20, random_state=42)
model = svm.SVC(kernel='linear')
model.fit(X_train,y_train)
filename = 'heart_attack_classifier_model.sav'
#pickle.dump(model, open(filename, 'wb'))
accuracy = model.score(X_test,y_test)
print("ACCURACY :",accuracy)