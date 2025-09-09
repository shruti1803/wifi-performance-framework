import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
df = pd.read_csv("wifi_results.csv")

# Define degraded: latency>50ms OR lost_percent>5 OR throughput < 50% mean
df["degraded"] = ((df["latency_ms"] > 50) | 
                  (df["lost_percent"] > 5) | 
                  (df["throughput_mbps"] < df["throughput_mbps"].mean() * 0.5)).astype(int)

X = df[["throughput_mbps","latency_ms","jitter_ms","lost_percent"]]
y = df["degraded"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model
joblib.dump(clf, "wifi_rf_model.pkl")
print("✅ ML model trained and saved as wifi_rf_model.pkl")
