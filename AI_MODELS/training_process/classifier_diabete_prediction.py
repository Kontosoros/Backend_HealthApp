import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn import  svm
import pickle

df  = pd.read_csv("diabetes.csv")
X = df[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
       'BMI', 'DiabetesPedigreeFunction', 'Age']]
y = df['Outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
model = svm.SVC()
model.fit(X_train,y_train)
filename = 'diabetes_classifier_model.sav'
#pickle.dump(model, open(filename, 'wb'))
accuracy = model.score(X_test,y_test)
print("ACCURACY :",accuracy)