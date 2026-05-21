import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("attack_dataset_1000.csv")

X = data[['attempts','time_gap','ip_change','energy']]
y = data['attack']

model = RandomForestClassifier()
model.fit(X,y)

joblib.dump(model,"attack_model.pkl")