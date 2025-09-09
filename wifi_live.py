import subprocess, json, os, time, threading
import pandas as pd
from datetime import datetime
from ping3 import ping
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_name = "wifi_results.csv"

# -------- Run iperf3 Test -------- #
def run_iperf_test(server_ip="127.0.0.1", duration=5, parallel=1, udp=False, bandwidth=None):
    cmd = ["iperf3", "-c", server_ip, "-t", str(duration), "-J", "-p", "5201"]
    if parallel > 1:
        cmd += ["-P", str(parallel)]
    if udp:
        cmd += ["-u"]
        if bandwidth:
            cmd += ["-b", str(bandwidth)]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("❌ iperf3 error:", proc.stderr)
        return None
    try:
        return json.loads(proc.stdout)
    except:
        return None

# -------- Extract Metrics -------- #
def extract_metrics(iperf_json, server_ip="127.0.0.1"):
    end = iperf_json.get("end", {})
    summary = end.get("sum_received") or end.get("sum_sent") or {}

    latency_ms = ping(server_ip, unit="ms")

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "throughput_mbps": summary.get("bits_per_second", 0) / 1e6,
        "retransmits": summary.get("retransmits"),
        "lost_percent": summary.get("lost_percent"),
        "jitter_ms": summary.get("jitter_ms"),
        "latency_ms": latency_ms,
    }

# -------- Save to CSV -------- #
def save_results(metrics):
    df = pd.DataFrame([metrics])
    if os.path.exists(file_name):
        df.to_csv(file_name, mode="a", header=False, index=False)
    else:
        df.to_csv(file_name, index=False)

# -------- Anomaly Detection -------- #
def detect_anomalies(series):
    if len(series) < 2:
        return []
    mean = series.mean()
    std = series.std()
    return series[(series - mean).abs() > 2 * std]

# -------- Background Test Runner -------- #
def run_tests(server_ip="127.0.0.1", num_tests=20, duration=5):
    print(f"🚀 Running {num_tests} Wi-Fi tests...\n")
    for i in range(num_tests):
        print(f"▶ Test {i+1}/{num_tests}")
        j = run_iperf_test(server_ip, duration=duration)
        if j:
            metrics = extract_metrics(j, server_ip)
            print(metrics)
            save_results(metrics)
        time.sleep(2)
    print("\n✅ All tests finished!")

# -------- Real-Time Plotting -------- #
metrics = ["throughput_mbps", "latency_ms", "jitter_ms", "lost_percent"]
fig, axs = plt.subplots(len(metrics), 1, figsize=(10, 12))
plt.subplots_adjust(hspace=0.5)

def load_data():
    try:
        df = pd.read_csv(file_name)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except:
        return pd.DataFrame()

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

            anomalies = detect_anomalies(df[metric].dropna())
            if not anomalies.empty:
                anomaly_points = df.loc[df[metric].isin(anomalies)]
                axs[i].scatter(anomaly_points["timestamp"], anomaly_points[metric],
                               color="red", s=80, label="Anomaly", zorder=5)

            axs[i].legend()

# -------- Main -------- #
if __name__ == "__main__":
    # Start test runner in background thread
    t = threading.Thread(target=run_tests, args=("127.0.0.1", 20, 5))
    t.start()

    # Start real-time dashboard
    ani = FuncAnimation(fig, update, interval=2000)
    plt.show()
