# Wi-Fi Performance Testing & Automation Framework
<img width="932" height="383" alt="Screenshot 2025-09-09 220013" src="https://github.com/user-attachments/assets/65626417-d1cf-4dcb-8d7b-b76ee0cff059" />
<img width="1490" height="1030" alt="Screenshot 2025-09-09 211615" src="https://github.com/user-attachments/assets/ee289e01-4f86-4870-be09-983fe15f485f" />


## Project Overview
This is a **Python-based framework** to **test, monitor, and predict Wi-Fi network performance**.  
It automates latency, throughput, jitter, and packet loss tests, provides a **live dashboard**, and includes a **machine learning model** to predict network degradation.

---

## Key Features
##Automated Wi-Fi Performance Testing

- Runs latency, throughput, jitter, and packet loss tests.

- Supports different load conditions (e.g., multiple clients, bandwidth limits).

- Logs results in structured CSV files for later analysis.

##Real-Time Dashboard

- Live plotting of key metrics (latency, jitter, throughput, packet loss).

- Updates dynamically as tests run.

- Clear visualization for performance monitoring.

##Machine Learning Integration

- Random Forest Classifier trained on historical data.

- Predicts when Wi-Fi performance might degrade.

- Flags anomalies such as latency spikes, bandwidth drops, or packet loss.

- Integrated seamlessly with the live dashboard and test runs.

##Automated Reporting

- Generates professional PDF reports summarizing results.

- Includes graphs, test metrics, and ML predictions.

- Reports saved automatically in a reports/ folder.

##Anomaly Detection

- AI-based detection of unusual behavior (e.g., sudden jitter or packet loss).

- Highlights anomalies directly in reports.

##Extensible Framework

- Easy to add new metrics or test cases.

- Modular design for plugging in different ML models.

- Can scale from single laptop simulation to multi-client real tests.

##Scalability

- Uses iperf for traffic simulation (server & client modes).

- Supports multiple clients under different bandwidth/load conditions.

##Data Visualization

- CSV → Graphs (Matplotlib).

- Real-time and static plotting.

- Easy to extend with advanced dashboards (e.g., Plotly/Streamlit in future).

##Automation & Scripting

- Python scripts handle test execution, logging, analysis, and visualization.

- Can be scheduled or run repeatedly without manual effort.

##Version Control & Collaboration

- Structured repository on GitHub.

- .gitignore configured to exclude large/generated files (CSV, cache, pickle).

##Why it matters for managers:

- In large-scale networks, Wi-Fi performance directly impacts user experience, productivity, and customer satisfaction. Manual testing is time-consuming, inconsistent, and difficult to scale.

- This framework addresses those challenges by:

- Automating Wi-Fi testing → reduces time, human error, and cost of validation

- Providing repeatable, data-driven benchmarks → enables faster release cycles and higher confidence in deployments

- Supporting scalability → adaptable for enterprise, IoT, and multi-device test environments

- Leveraging ML insights → helps anticipate performance degradation before it impacts end users

For managers, this means faster go-to-market, improved reliability, and measurable performance assurance, all while aligning with Cisco’s mission of delivering secure, high-quality connectivity at scale.
  

---

## Usage

- **Run the framework:**  <br>
Live Dashboard: Automatically shows performance metrics in real-time.<br>
ML Predictions: Alerts when network performance might degrade.<br>
PDF Reports: Saved in the reports/ folder after each test run.<br>
Why This Matters (For Hiring Managers):<br>
Demonstrates automated network testing and monitoring.<br>
Integrates ML for proactive performance alerts.<br>
Showcases Python automation, Wi-Fi networking, and data visualization skills.<br>
Highlights skills directly relevant to enterprise IT, cloud, and network infrastructure roles.<br>

📊 Sample Output <br>
Live Dashboard: Shows throughput, latency, jitter, packet loss with red anomaly markers<br>
PDF Report: Summary table + plots with anomalies<br>
<img width="1490" height="1030" alt="Screenshot 2025-09-09 211615" src="https://github.com/user-attachments/assets/3c19d1b6-2bfb-4d9f-ada2-84924f2f6a8d" />
<img width="1919" height="1079" alt="Screenshot 2025-09-09 195353" src="https://github.com/user-attachments/assets/3ecf6a54-65b8-4d36-984b-0766b12e328f" />
<img width="1252" height="707" alt="Screenshot 2025-09-09 194556" src="https://github.com/user-attachments/assets/e3b425e7-9916-4222-b4bc-788173fd05d2" />
<img width="1683" height="1068" alt="Screenshot 2025-09-09 193803" src="https://github.com/user-attachments/assets/765bc34d-c47f-4c44-8abe-9c84df3c1896" />


🎯 Impact<br>
Provides a scalable, automated Wi-Fi performance testing solution, showcasing skills in networking, Python automation, real-time monitoring, data visualization, and reporting.<br>
Live Dashboard: Shows throughput, latency, jitter, packet loss with red anomaly markers
PDF Report: Summary table + plots with anomalies
