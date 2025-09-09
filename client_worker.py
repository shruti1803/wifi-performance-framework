import subprocess, json
import pandas as pd
from datetime import datetime
import os

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

def extract_metrics(iperf_json):
    end = iperf_json.get("end", {})
    summary = end.get("sum_received") or end.get("sum_sent") or {}
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "throughput_mbps": summary.get("bits_per_second", 0) / 1e6,
        "retransmits": summary.get("retransmits"),
        "lost_percent": summary.get("lost_percent"),
        "jitter_ms": summary.get("jitter_ms"),
    }

if __name__ == "__main__":
    # Run test
    j = run_iperf_test("127.0.0.1", duration=5, parallel=1, udp=False)
    metrics = extract_metrics(j)
    print(metrics)

    # Save to CSV
    file_name = "wifi_results.csv"
    df = pd.DataFrame([metrics])

    # Append if file exists, else create new
    if os.path.exists(file_name):
        df.to_csv(file_name, mode="a", header=False, index=False)
    else:
        df.to_csv(file_name, index=False)

    print(f"✅ Results saved to {file_name}")
