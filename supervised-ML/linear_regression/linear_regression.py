import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error


columns = [
    "CRIM",      # Crime Rate
    "ZN",        # Residential Land
    "INDUS",     # Industrial Area
    "CHAS",      # Near River (0/1)
    "NOX",       # Nitric Oxide Level
    "RM",        # Average Rooms
    "AGE",       # Age of Houses
    "DIS",       # Distance to Employment Centers
    "RAD",       # Road Accessibility
    "TAX",       # Property Tax
    "PTRATIO",   # Pupil-Teacher Ratio
    "B",         # Population Factor
    "LSTAT",     # Lower Status Population %
    "MEDV"       # House Price (Target)
]


df = pd.read_csv(
    "housing.csv", names=columns, header=None,  delim_whitespace=True)



print("First 5 Rows:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

X = df.drop("MEDV", axis=1)
y = df["MEDV"]


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


#Calculate MSE
mse = mean_squared_error(y_test, y_pred)
print("\nMSE:", mse)

#Calculate MAE
mae = mean_absolute_error(y_test, y_pred)
print("MAE:", mae)

#Residual Plot
residuals = y_test - y_pred

plt.scatter(y_pred, residuals)
plt.axhline(y=0)
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()


#Ridge Regression
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
ridge_pred = ridge.predict(X_test)
ridge_mse = mean_squared_error(y_test, ridge_pred)
print("\nRidge MSE:", ridge_mse)


#Lasso Regression
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
lasso_pred = lasso.predict(X_test)
lasso_mse = mean_squared_error(y_test, lasso_pred)
print("Lasso MSE:", lasso_mse)


# Compare Coefficients
print("\nLinear Regression Coefficients:")
print(model.coef_)
print("\nRidge Coefficients:")
print(ridge.coef_)
print("\nLasso Coefficients:")
print(lasso.coef_)