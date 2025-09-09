import pandas as pd
import matplotlib.pyplot as plt

# Load results from CSV
file_name = "wifi_results.csv"
df = pd.read_csv(file_name)

print("📊 Data loaded:")
print(df.head())

# Plot throughput over time
plt.figure(figsize=(8,5))
plt.plot(df["timestamp"], df["throughput_mbps"], marker="o", linestyle="-", color="blue", label="Throughput (Mbps)")

# Make it pretty
plt.xticks(rotation=45, ha="right")
plt.xlabel("Time")
plt.ylabel("Throughput (Mbps)")
plt.title("Wi-Fi Performance Test Results")
plt.legend()
plt.tight_layout()

# Show graph
plt.show()
