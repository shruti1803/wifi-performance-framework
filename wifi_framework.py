import subprocess, json, os, time
import pandas as pd
from datetime import datetime
from ping3 import ping
import numpy as np

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
        raise RuntimeError(proc.stderr)
    return json.loads(proc.stdout)

# -------- Extract Metrics -------- #
def extract_metrics(iperf_json, server_ip="127.0.0.1"):
    end = iperf_json.get("end", {})
    summary = end.get("sum_received") or end.get("sum_sent") or {}

    # Ping latency test
    latency_ms = ping(server_ip, unit="ms")
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "throughput_mbps": summary.get("bits_per_second", 0) / 1e6,
        "retransmits": summary.get("retransmits"),
        "lost_percent": summary.get("lost_percent"),
        "jitter_ms": summary.get("jitter_ms"),
        "latency_ms": latency_ms,
    }

# -------- Anomaly Detection -------- #
def detect_anomalies(df):
    anomalies = []
    for metric in ["throughput_mbps", "latency_ms", "jitter_ms", "lost_percent"]:
        if metric in df.columns:
            values = df[metric].dropna()
            if len(values) > 1:
                mean = values.mean()
                std = values.std()
                # Mark anomalies if > 2 standard deviations away
                anomalies += list(df.loc[(df[metric] - mean).abs() > 2*std, "timestamp"])
    return anomalies

# -------- Save to CSV -------- #
def save_results(metrics, file_name="wifi_results.csv"):
    df = pd.DataFrame([metrics])
    if os.path.exists(file_name):
        df.to_csv(file_name, mode="a", header=False, index=False)
    else:
        df.to_csv(file_name, index=False)

# -------- Automation Loop -------- #
if __name__ == "__main__":
    server_ip = "127.0.0.1"
    num_tests = 8       # more runs to catch anomalies
    duration = 5        # each test length (seconds)

    print(f"🚀 Running {num_tests} Wi-Fi performance tests...\n")
    
    for i in range(num_tests):
        print(f"▶ Test {i+1}/{num_tests}...")
        j = run_iperf_test(server_ip, duration=duration, parallel=1, udp=False)
        metrics = extract_metrics(j, server_ip)
        print(metrics)
        save_results(metrics)
        time.sleep(2)   # wait before next test
    
    # Load results for anomaly detection
    df = pd.read_csv("wifi_results.csv")
    anomalies = detect_anomalies(df)

    if anomalies:
        print("\n⚠️ Anomalies detected at timestamps:")
        for a in anomalies:
            print(" -", a)
    else:
        print("\n✅ No anomalies detected")
