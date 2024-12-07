import os
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
import logging
from lime.lime_tabular import LimeTabularExplainer
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import learning_curve
from lime.lime_tabular import LimeTabularExplainer
import joblib
from sklearn.preprocessing import StandardScaler

def target_encode_with_smoothing(data, column, target, n_splits=5, smoothing=1):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    encoded_values = np.zeros(len(data))
    global_mean = data[target].mean()  
    category_mapping = {}  
    for train_idx, val_idx in kf.split(data):
        train_data, val_data = data.iloc[train_idx], data.iloc[val_idx]
        category_stats = train_data.groupby(column)[target].agg(['mean', 'count'])
        category_stats['smoothed_mean'] = (
            (category_stats['count'] * category_stats['mean'] + smoothing * global_mean) /
            (category_stats['count'] + smoothing)
        )
        for category, smoothed_mean in category_stats['smoothed_mean'].items():
            category_mapping[category] = smoothed_mean
        val_encoded = val_data[column].map(category_stats['smoothed_mean'])
        encoded_values[val_idx] = val_encoded.fillna(global_mean)  
    for category in data[column].unique():
        if category not in category_mapping:
            category_mapping[category] = global_mean  
    return encoded_values, category_mapping
file_path = '../data/processed/final.csv'
df = pd.read_csv(file_path)
# print(df.head())
# print(df.columns)
X = df.iloc[:, [0, 3, 4, 5, 6]]  
y = df.iloc[:, 1]           
X_original = df.iloc[:, [0, 3, 4, 5, 6]]  
# print("Input (X):")
# print(X.head())
# print("\nOutput (y):")
# print(y.head())
# X['Player'] = target_encode_with_smoothing(df, column='Player', target='Fantasy Points')
# X['Team'] = target_encode_with_smoothing(df, column='Team', target='Fantasy Points')
# X['Match Date'] = target_encode_with_smoothing(df, column='Match Date', target='Fantasy Points')
# X['Opponent'] = target_encode_with_smoothing(df, column='Opponent', target='Fantasy Points')
# X['Match Type'] = target_encode_with_smoothing(df, column='Match Type', target='Fantasy Points')
X['Player'], player_mapping = target_encode_with_smoothing(df, column='Player', target='Fantasy Points')
X['Team'], team_mapping = target_encode_with_smoothing(df, column='Team', target='Fantasy Points')
X['Match Date'], match_date_mapping = target_encode_with_smoothing(df, column='Match Date', target='Fantasy Points')
X['Opponent'], opponent_mapping = target_encode_with_smoothing(df, column='Opponent', target='Fantasy Points')
X['Match Type'], match_type_mapping = target_encode_with_smoothing(df, column='Match Type', target='Fantasy Points')
joblib.dump((player_mapping,team_mapping,match_date_mapping,opponent_mapping,match_type_mapping), 'encodings.pkl')
X = X.values
y = y.values
print(X)
print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=92)
X_train_orginal, X_test_original, y_train_original, y_test_original = train_test_split(X_original, y, test_size=0.2, random_state=92)
xgb_model = xgb.XGBRegressor(objective='reg:squarederror')
param_grid = {
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 400],
    'colsample_bytree': [0.3, 0.7],
    'alpha': [0, 10, 100]
}
grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error', 
    cv=5, 
    verbose=1,  
    n_jobs=-1   
)
grid_search.fit(X_train, y_train)
# print("Best Parameters:", grid_search.best_params_)
# print("Best Score:", grid_search.best_score_)
y_pred = grid_search.best_estimator_.predict(X_test)
x = X_test[:, 0] 
# plt.figure(figsize=(8, 6))
# plt.plot(x, y_test, 'b-o', label="Original (True Values)", alpha=0.7)
# plt.xlabel("X (Independent Variable)")
# plt.ylabel("Y (Dependent Variable)")
# plt.title("X vs Original Values")
# plt.legend()
# plt.grid(True)
# plt.show()
# plt.figure(figsize=(8, 6))
# plt.plot(x, y_pred, 'r--o', label="Predicted Values", alpha=0.7)
# plt.xlabel("X (Independent Variable)")
# plt.ylabel("Y (Dependent Variable)")
# plt.title("X vs Predicted Values")
# plt.legend()
# plt.grid(True)
# plt.show()
plt.figure(figsize=(8, 6))
plt.plot(x, y_test, 'b-o', label="Original (True Values)", alpha=0.7)
plt.plot(x, y_pred, 'r--o', label="Predicted Values", alpha=0.7)
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("X vs True vs Predicted Values")
plt.legend()
plt.grid(True)
plt.show()
importances = grid_search.best_estimator_.feature_importances_
features = X_train.columns if hasattr(X_train, 'columns') else range(X_train.shape[1])
print(X_train)
print(features)
plt.figure(figsize=(10, 6))
plt.barh(features, importances, color='skyblue')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.title('Feature Importance')
plt.show()
model = grid_search.best_estimator_
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error (MAE) on test data: {mae:.4f}")
model_filename = 'xgb_model_best.pkl'
joblib.dump(grid_search.best_estimator_, model_filename)
print(f"Model saved to {model_filename}")