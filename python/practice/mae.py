# Overfitting: capturing spurious patterns that won't recur in the future, leading to less accurate predictions, or
# Underfitting: failing to capture relevant patterns, again leading to less accurate predictions.

# Compute the mean absolute error (MAE) based on number of max_leaf_nodes
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error


def get_mae(max_leaf_nodes, train_X, train_y, val_X, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return mae


# compare MAE with differing values of max_leaf_nodes
def compare_mae(train_X, train_y, val_X, val_y):
    for x in [5, 50, 500, 5000]:
        my_mae = get_mae(x, train_X, train_y, val_X, val_y)
        print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" % (x, my_mae))
