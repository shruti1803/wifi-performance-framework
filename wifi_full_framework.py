import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import time
from datetime import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import joblib

# ----------------- Configuration ----------------- #
TEST_INTERVAL = 5  # seconds
CSV_FILE = "wifi_results.csv"
PDF_FOLDER = "."
ML_MODEL_FILE = "wifi_rf_model.pkl"

# Load trained ML model
clf = joblib.load(ML_MODEL_FILE)

# Initialize CSV
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["timestamp","throughput_mbps","latency_ms","jitter_ms","lost_percent","predicted_degraded"])
    df.to_csv(CSV_FILE,index=False)

# ----------------- Utility Functions ----------------- #
def run_iperf_test():
    """Run iperf3 test and return metrics as dictionary"""
    result = subprocess.run(["iperf3", "-c", "127.0.0.1", "-J"], capture_output=True, text=True)
    import json
    data = json.loads(result.stdout)
    try:
        throughput = data['end']['sum_received']['bits_per_second'] / 1e6
        latency = data.get('end', {}).get('streams', [{}])[0].get('sender', {}).get('mean_rtt', 0)
        jitter = data.get('end', {}).get('streams', [{}])[0].get('jitter_ms', 0)
        lost_percent = data.get('end', {}).get('streams', [{}])[0].get('lost_percent', 0)
    except:
        throughput = latency = jitter = lost_percent = 0
    return {
        "timestamp": datetime.now(),
        "throughput_mbps": throughput,
        "latency_ms": latency,
        "jitter_ms": jitter,
        "lost_percent": lost_percent
    }

def detect_anomalies(series):
    """Detect anomalies using 2-sigma rule"""
    if len(series) < 2:
        return []
    mean = series.mean()
    std = series.std()
    return series[(series - mean).abs() > 2 * std]

def save_metrics(metrics):
    global df
    # Save timestamp as ISO format
    metrics["timestamp"] = metrics["timestamp"].isoformat()
    df = pd.concat([df, pd.DataFrame([metrics])], ignore_index=True)
    df.to_csv(CSV_FILE,index=False)

# ----------------- PDF Report ----------------- #
def generate_pdf_report():
    metrics_list = ["throughput_mbps","latency_ms","jitter_ms","lost_percent"]
    pdf_name = f"{PDF_FOLDER}/wifi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(pdf_name,pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold",18)
    c.drawCentredString(width/2,height-50,"Wi-Fi Performance Report")

    # Summary table
    c.setFont("Helvetica",12)
    y = height-100
    c.drawString(50,y,"Summary of Tests:")
    y -= 20

    for metric in metrics_list:
        if metric in df.columns:
            mean_val = df[metric].mean()
            max_val = df[metric].max()
            min_val = df[metric].min()
            anomaly_count = len(detect_anomalies(df[metric]))
            predicted_count = df["predicted_degraded"].sum()
            line = f"{metric}: mean={mean_val:.2f}, min={min_val:.2f}, max={max_val:.2f}, anomalies={anomaly_count}, predicted_degraded={predicted_count}"
            c.drawString(60,y,line)
            y -= 15

    # Plots
    plot_images = []
    for metric in metrics_list:
        if metric in df.columns:
            plt.figure(figsize=(8,4))
            timestamps = pd.to_datetime(df["timestamp"], errors='coerce', infer_datetime_format=True)
            plt.plot(timestamps, df[metric], marker="o", label=metric)
            anomalies = detect_anomalies(df[metric])
            if len(anomalies) > 0:
                anomaly_points = df.loc[df[metric].isin(anomalies)]
                plt.scatter(pd.to_datetime(anomaly_points["timestamp"], errors='coerce', infer_datetime_format=True),
                            anomaly_points[metric],
                            color="red", s=80, label="Anomaly")
            pred_points = df[df["predicted_degraded"]==1]
            if len(pred_points)>0:
                plt.scatter(pd.to_datetime(pred_points["timestamp"], errors='coerce', infer_datetime_format=True),
                            pred_points[metric],
                            color="orange", s=80, label="Predicted Degradation")
            plt.title(f"Wi-Fi Performance: {metric}")
            plt.xlabel("Time")
            plt.ylabel(metric)
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf,format="png")
            plt.close()
            buf.seek(0)
            plot_images.append(buf)

    for img in plot_images:
        c.showPage()
        c.drawImage(ImageReader(img),50,150,width-100,height-300)

    c.save()
    print(f"✅ PDF report generated: {pdf_name}")

# ----------------- Live Dashboard ----------------- #
plt.ion()
fig, axs = plt.subplots(2,2,figsize=(12,8))
axs = axs.flatten()

def update_dashboard():
    for i, metric in enumerate(["throughput_mbps","latency_ms","jitter_ms","lost_percent"]):
        axs[i].clear()
        axs[i].set_title(f"Real-Time Wi-Fi Performance: {metric}")
        axs[i].set_xlabel("Time")
        axs[i].set_ylabel(metric)
        if metric in df.columns:
            timestamps = pd.to_datetime(df["timestamp"], errors='coerce', infer_datetime_format=True)
            axs[i].plot(timestamps, df[metric], marker="o", label=metric)

            anomalies = detect_anomalies(df[metric])
            if len(anomalies) > 0:
                anomaly_points = df.loc[df[metric].isin(anomalies)]
                axs[i].scatter(pd.to_datetime(anomaly_points["timestamp"], errors='coerce', infer_datetime_format=True),
                               anomaly_points[metric],
                               color="red", s=80, label="Anomaly", zorder=5)

            pred_points = df[df["predicted_degraded"]==1]
            if len(pred_points)>0:
                axs[i].scatter(pd.to_datetime(pred_points["timestamp"], errors='coerce', infer_datetime_format=True),
                               pred_points[metric],
                               color="orange", s=80, label="Predicted Degradation", zorder=4)
            axs[i].legend()
    plt.pause(0.01)

# ----------------- Main Test Loop ----------------- #
def run_tests():
    while True:
        metrics = run_iperf_test()
        # Predict degradation
        features = [[metrics["throughput_mbps"], metrics["latency_ms"], metrics["jitter_ms"], metrics["lost_percent"]]]
        metrics["predicted_degraded"] = int(clf.predict(features)[0])

        save_metrics(metrics)
        update_dashboard()
        time.sleep(TEST_INTERVAL)

# Run in main thread
try:
    run_tests()
except KeyboardInterrupt:
    print("Stopping tests...")
    generate_pdf_report()
