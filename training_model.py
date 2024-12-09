import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load the dataset
file_path = r"C:\Users\HP\Downloads\archive (1)\Bengaluru_House_Data.csv"
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure of the dataset
print("Initial Data Preview:")
print(data.head())

# Function to preprocess 'total_sqft' column
def convert_sqft_to_num(value):
    try:
        # If it's a range (e.g., "2580 - 2591"), take the average
        if "-" in str(value):
            parts = value.split("-")
            return (float(parts[0]) + float(parts[1])) / 2
        # If it's already a number, return it as float
        return float(value)
    except ValueError:
        # For invalid or unexpected values, return NaN
        return None

# Apply preprocessing to 'total_sqft' column
data["total_sqft"] = data["total_sqft"].apply(convert_sqft_to_num)

# Drop rows with NaN values in critical columns
data = data.dropna(subset=["total_sqft", "bath", "price"])

# Select relevant features and target variable
# Adjust based on your dataset's column names
data = data[["total_sqft", "bath", "balcony", "location", "price"]]

# Handle missing values in less critical columns (e.g., 'balcony')
data["balcony"] = data["balcony"].fillna(0)  # Replace NaN with 0

# Encode 'location' as numeric (Label Encoding)
data["location"] = data["location"].astype("category").cat.codes

# Features (X) and Target (y)
X = data[["total_sqft", "bath", "balcony", "location"]]
y = data["price"]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model to a file
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

# Load the model (to confirm it's saved correctly)
with open("model.pkl", "rb") as file:
    loaded_model = pickle.load(file)

# Test prediction
# Provide an example test case (square_feet, bath, balcony, encoded location)
sample_input = [[2000, 2, 1, 10]]  # Replace with meaningful test values
predicted_price = loaded_model.predict(sample_input)

print(f"Predicted Price for input {sample_input}: ₹{predicted_price[0]:,.2f}")
