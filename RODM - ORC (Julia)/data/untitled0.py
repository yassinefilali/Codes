from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import numpy as np
df = pd.read_csv(r"C:\Users\Yassine\Desktop\Zach\data\adult_test.csv")

OE = OrdinalEncoder()

ref = df.income[0]
target = (df.income == ref).astype(int)
data = df.iloc[:,:df.shape[1]-1]
x = OE.fit_transform(data[['workclass']])
data['workclass'] = x
native_OHE = pd.get_dummies(np.asarray(data.native_country))
X_tr, X_ts, y_tr, y_ts = train_test_split(data, target, test_size=0.25)
model = RandomForestClassifier()
model.fit(X_tr,y_tr)
y_pred = model.predict(X_ts)
print(accuracy_score(y_pred,y_ts))
