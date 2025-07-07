import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Step 1: Load data
df = pd.read_csv("crop_prices.csv")

# Step 2: Convert categorical variables
df = pd.get_dummies(df, columns=["crop", "state", "month"])

# Step 3: Split into input and target
X = df.drop("price", axis=1)
y = df["price"]

# Step 4: Train the model
model = LinearRegression()
model.fit(X, y)

# Step 5: Save the model
joblib.dump(model, "market_price_model.pkl")

# Optional: Save the feature columns (needed during prediction)
joblib.dump(X.columns.tolist(), "model_features.pkl")

print("✅ Model trained and saved as market_price_model.pkl")
