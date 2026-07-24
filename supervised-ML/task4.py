import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
data = {
    "Study Hours": [1,2,3,4,5,6,7,8,9,10],
    "Pass": [0,0,0,0,1,1,1,1,1,1]

}
df = pd.DataFrame(data)
print(df)
X = df[["Study Hours"]]
y = df['Pass']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred= model.predict(X_test)
print("Predicted Values:", y_pred)
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)