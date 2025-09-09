import pandas as pd
import matplotlib.pyplot as plt

# -------- Load Results -------- #
file_name = "wifi_results.csv"
df = pd.read_csv(file_name)

# -------- Convert timestamp to datetime -------- #
df["timestamp"] = pd.to_datetime(df["timestamp"])

# -------- Detect anomalies (same logic as framework) -------- #
def detect_anomalies(df, metric):
    values = df[metric].dropna()
    if len(values) < 2:
        return []
    mean = values.mean()
    std = values.std()
    return df.loc[(df[metric] - mean).abs() > 2 * std]

# -------- Plot Metrics with Anomalies -------- #
metrics = ["throughput_mbps", "latency_ms", "jitter_ms", "lost_percent"]

for metric in metrics:
    if metric in df.columns:
        plt.figure(figsize=(10,5))
        plt.plot(df["timestamp"], df[metric], marker="o", label=metric)

        # Highlight anomalies
        anomalies = detect_anomalies(df, metric)
        if not anomalies.empty:
            plt.scatter(anomalies["timestamp"], anomalies[metric], 
                        color="red", s=100, label="Anomaly", zorder=5)

        plt.title(f"Wi-Fi Performance: {metric}")
        plt.xlabel("Time")
        plt.ylabel(metric)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
