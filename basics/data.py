import pandas as pd
df = pd.read_csv('task.csv')
# print(df.isnull().sum())
df["Experience"] = df["Experience"].fillna(df["Experience"].mean())
df["Salary"] = df["Salary"].fillna(df["Salary"].mean())
df["PerformanceScore"] = df["PerformanceScore"].fillna(df["PerformanceScore"].mean())
department_avearges = df.groupby("Department")[["Experience", "Salary", "PerformanceScore"]].mean()
print(df)
print(department_avearges)