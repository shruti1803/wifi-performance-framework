import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_name = "wifi_results.csv"

# -------- Load Data Function -------- #
def load_data():
    try:
        df = pd.read_csv(file_name)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception:
        return pd.DataFrame()

# -------- Anomaly Detection -------- #
def detect_anomalies(series):
    if len(series) < 2:
        return []
    mean = series.mean()
    std = series.std()
    return series[(series - mean).abs() > 2 * std]

# -------- Plot Setup -------- #
metrics = ["throughput_mbps", "latency_ms", "jitter_ms", "lost_percent"]
fig, axs = plt.subplots(len(metrics), 1, figsize=(10, 12))
plt.subplots_adjust(hspace=0.5)

# -------- Animation Function -------- #
def update(frame):
    df = load_data()
    if df.empty:
        return
    
    for i, metric in enumerate(metrics):
        axs[i].clear()
        axs[i].set_title(f"Real-Time Wi-Fi Performance: {metric}")
        axs[i].set_xlabel("Time")
        axs[i].set_ylabel(metric)

        if metric in df.columns:
            axs[i].plot(df["timestamp"], df[metric], marker="o", label=metric)

            # highlight anomalies
            anomalies = detect_anomalies(df[metric].dropna())
            if not anomalies.empty:
                anomaly_points = df.loc[df[metric].isin(anomalies)]
                axs[i].scatter(anomaly_points["timestamp"], anomaly_points[metric], 
                               color="red", s=80, label="Anomaly", zorder=5)

            axs[i].legend()

# -------- Start Animation -------- #
ani = FuncAnimation(fig, update, interval=2000)  # refresh every 2 sec
plt.show()
