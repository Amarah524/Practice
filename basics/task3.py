import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# data = {
#     "Study Hours": [1,2,3,4,5],
#     "Test Scores": [45,60,58,80,70]
# }
data = {
    "Study Hours": [1,2,3],
    "Test Scores": [50,60,70]
}
df = pd.DataFrame(data)
corr_matrix = df.corr()
# print(corr_matrix)
sns.heatmap(corr_matrix, annot=True, cmap="Reds")
plt.title("Correlation Heatmap")
plt.show()