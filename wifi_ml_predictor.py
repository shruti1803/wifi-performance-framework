import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load data
df = pd.read_csv("wifi_results.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Define target: degraded = 1 if metrics exceed thresholds
df["degraded"] = ((df["latency_ms"] > 50) | 
                  (df["lost_percent"] > 5) | 
                  (df["throughput_mbps"] < df["throughput_mbps"].mean() * 0.5)).astype(int)

# Features
X = df[["throughput_mbps", "latency_ms", "jitter_ms", "lost_percent"]]
y = df["degraded"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
