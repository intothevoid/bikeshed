import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Read the data
data = pd.read_csv("data.csv")


# point of interest
y = data["price"]

# features
X = data[["area", "bedrooms", "age"]]

# Define model. Specify a number for random_state to ensure same results each run
model = DecisionTreeClassifier(random_state=1)

# Fit model
model.fit(X, y)

# Make a prediction for a house with 3000 sqr ft area, 3 bedrooms, 40 year old
print(model.predict([[3000, 3, 40]]))

# Make a prediction for a house with 2500 sqr ft area, 4 bedrooms, 5 year old
print(model.predict([[2500, 4, 5]]))
