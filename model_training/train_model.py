from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score,precision_score , recall_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joblib

# Import data from csv file
train = pd.read_csv("./train.csv")
test = pd.read_csv("./test.csv")

# Split data
x_train = train.drop(["Class","Unnamed: 0"],axis=1)
y_train = train[["Class"]]

x_test = test.drop(["Class","Unnamed: 0"],axis=1)
y_test = test[["Class"]]

# Train model
model = XGBClassifier()
model.fit(x_train,y_train)

# Prediction
y_pred = model.predict(x_test)

# Evaluation model with any metric
acc_test = accuracy_score(y_test, y_pred)
roc_auc_test = roc_auc_score(y_test, y_pred)
f1_test= f1_score(y_test, y_pred)
precision_test = precision_score(y_test, y_pred)
recall_test = recall_score(y_test, y_pred)

print("Accuracy = ", acc_test)
print("ROC and AUC = ", roc_auc_test)
print("F1 scorre = ", f1_test)
print("Precision score = ", precision_test)
print("Recall score = ", recall_test)


# Feature important
df_feature = pd.DataFrame({'Feature': x_train.columns, 'Feature importance': model.feature_importances_})
df_feature = df_feature.sort_values(by='Feature importance', ascending=False)

s = sns.barplot(x='Feature',y='Feature importance',data=df_feature)
s.set_xticklabels(s.get_xticklabels(),rotation=90)
plt.show()

# Export model
joblib.dump(model, './dags/fraud_detection.pkl')