import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Read the data
data = pd.read_csv("melb_data.csv")

# Filter rows with missing values
data.dropna(axis=0, subset=["Price"], inplace=True)

# Choose target and features
y = data.Price
X = data.drop(["Price"], axis=1)

# Break off validation set from training data
train_X, train_y, val_X, val_y = train_test_split(X, y, random_state=0)

# Define model
model = RandomForestRegressor(random_state=1)

# Fit model
model.fit(train_X, train_y)

# Get predicted prices on validation data
val_predictions = model.predict(val_X)

# Calculate mean absolute error
mae = mean_absolute_error(val_y, val_predictions)

print("Mean Absolute Error: " + str(int(mae)))
