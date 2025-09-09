import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
from datetime import datetime
import numpy as np

# -------- Load Data -------- #
file_name = "wifi_results.csv"
df = pd.read_csv(file_name)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# -------- Anomaly Detection -------- #
def detect_anomalies(series):
    if len(series) < 2:
        return []
    mean = series.mean()
    std = series.std()
    return series[(series - mean).abs() > 2 * std]

metrics = ["throughput_mbps", "latency_ms", "jitter_ms", "lost_percent"]

# -------- Generate Plots as Images -------- #
plot_images = []
for metric in metrics:
    if metric in df.columns:
        plt.figure(figsize=(8,4))
        plt.plot(df["timestamp"], df[metric], marker="o", label=metric)

        anomalies = detect_anomalies(df[metric].dropna())
        if len(anomalies) > 0:
            anomaly_points = df.loc[df[metric].isin(anomalies)]
            plt.scatter(anomaly_points["timestamp"], anomaly_points[metric],
                color="red", s=80, label="Anomaly")


        plt.title(f"Wi-Fi Performance: {metric}")
        plt.xlabel("Time")
        plt.ylabel(metric)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        plot_images.append(buf)

# -------- Create PDF -------- #
pdf_name = f"wifi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
c = canvas.Canvas(pdf_name, pagesize=A4)
width, height = A4

# Title
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(width/2, height-50, "Wi-Fi Performance Report")

# Summary Table
c.setFont("Helvetica", 12)
y = height - 100
c.drawString(50, y, "Summary of Tests:")
y -= 20

for metric in metrics:
    if metric in df.columns:
        mean_val = df[metric].mean()
        max_val = df[metric].max()
        min_val = df[metric].min()
        anomaly_count = len(detect_anomalies(df[metric]))
        line = f"{metric}: mean={mean_val:.2f}, min={min_val:.2f}, max={max_val:.2f}, anomalies={anomaly_count}"
        c.drawString(60, y, line)
        y -= 15

# Insert Plots
for img in plot_images:
    c.showPage()
    c.drawImage(ImageReader(img), 50, 150, width-100, height-300)

c.save()
print(f"✅ PDF report generated: {pdf_name}")
