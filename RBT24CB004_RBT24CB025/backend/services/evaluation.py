import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

def evaluate_model(y_train, y_train_pred, y_test, y_test_pred) -> dict:
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_r2 = r2_score(y_train, y_train_pred)
    
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_r2 = r2_score(y_test, y_test_pred)
    
    overfitting = bool(train_r2 - test_r2 > 0.15)
    
    return {
        "train_rmse": float(train_rmse),
        "test_rmse": float(test_rmse),
        "train_r2": float(train_r2),
        "test_r2": float(test_r2),
        "overfitting_warning": overfitting
    }
