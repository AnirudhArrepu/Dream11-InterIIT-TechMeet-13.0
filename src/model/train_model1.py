import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
import logging
from lime.lime_tabular import LimeTabularExplainer

# Setup logging to log to a file
log_file = "training_log.log"  # Log file name
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # To log messages to both file and console
    ]
)
logger = logging.getLogger()

# Parameters
dataset_dir = "../data/raw/cricksheet/final/combined_output.csv"  # Replace with the actual dataset path
target_column = "Fantasy Points"  # Target column to predict

# Load dataset
if not os.path.exists(dataset_dir):
    logger.error(f"Dataset not found at {dataset_dir}")
    raise FileNotFoundError(f"Dataset not found at {dataset_dir}")

logger.info(f"Loading dataset from {dataset_dir}")
data = pd.read_csv(dataset_dir)
logger.info(f"Dataset loaded successfully with shape: {data.shape}")
logger.info(f"Dataset preview:\n{data.head()}")

# Exclude 'Match Date' and 'City' columns
exclude_columns = ['Match Date', 'City']
data.drop(columns=exclude_columns, inplace=True, errors='ignore')
logger.info(f"Excluding columns: {exclude_columns}. Dataset shape is now: {data.shape}")

# Preprocessing
# Encode categorical features
categorical_columns = ['Player', 'Team', 'Match Type']
label_encoders = {col: LabelEncoder() for col in categorical_columns}

for col in categorical_columns:
    data[col] = label_encoders[col].fit_transform(data[col])

# Separate features and target
X = data.drop(columns=[target_column])
y = data[target_column]

# Split data into train, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Initialize model with optimal parameters
model = XGBRegressor(
    objective='reg:squarederror',
    random_state=42,
    learning_rate=0.2,
    max_depth=7,
    n_estimators=150,
    subsample=1.0
)

# Train the model
logger.info("Training the model with optimal parameters.")
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
logger.info(f"Mean Absolute Error (MAE) on test data: {mae:.4f}")

# Integrate LIME for model interpretation
logger.info("Initializing LIME for model interpretation.")
explainer = LimeTabularExplainer(
    X_train.values,
    training_labels=y_train.values,
    feature_names=X.columns,
    mode='regression'
)

# Explain a single prediction
sample_index = 0  # Change index to analyze different samples
sample = X_test.iloc[sample_index].values.reshape(1, -1)
explanation = explainer.explain_instance(
    sample.flatten(),
    model.predict,
    num_features=5
)

# Log LIME explanation
logger.info("LIME explanation for a single test sample:")
logger.info(explanation.as_list())

# Display explanation
explanation.show_in_notebook()