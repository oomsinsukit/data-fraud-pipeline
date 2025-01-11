from sklearn.model_selection import train_test_split
import pandas as pd

df = pd.read_csv("./creditcard.csv")

# seperate feature and target into x and y
x_data = df.drop("Class",axis='columns')
y_data = df[["Class"]]

# split data into train, test and validation data
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

# combined data
train_data = pd.concat([x_train,y_train], axis='columns')
test_data = pd.concat([x_test,y_test], axis='columns')

# export data to csv file
train_data.to_csv("./train.csv")
test_data.to_csv('./test.csv')