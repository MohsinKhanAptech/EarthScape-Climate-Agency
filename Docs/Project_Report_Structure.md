# Project Report: EarthScape Climate Agency Big Data Solution

## 1. Title Page
* **Project Name:** EarthScape Climate Monitoring System
* **Student Name:** [Your Name]
* **Centre/Batch:** [Your Batch Code]
* **Date:** December 2025

---

## 2. Table of Contents
1. Introduction
2. Problem Definition
3. Objectives
4. System Requirements (Hardware/Software)
5. System Analysis & Design
   * Data Flow Diagrams (DFD)
   * System Architecture
6. Implementation Details
7. Testing & Screenshots
8. Future Enhancements
9. Conclusion

---

## 3. Introduction
* [cite_start]**Overview:** Introduce the EarthScape Climate Agency and its mission to monitor climate change issues[cite: 39].
* [cite_start]**Context:** Discuss how greenhouse emissions and deforestation are leading to severe weather shifts[cite: 37].
* [cite_start]**Technology:** Explain that the project uses **Big Data (Hadoop)** for processing vast datasets and **Machine Learning** for predictive analysis[cite: 38].

## 4. Problem Definition
* [cite_start]**Current Challenge:** The agency collects massive amounts of data from satellites and weather stations but lacks a robust solution to process it efficiently[cite: 40].
* [cite_start]**The Need:** There is a critical need for a system that can ingest historical and real-time data, detect anomalies, and visualize trends for decision-making[cite: 41].

## 5. Objectives
* [cite_start]To implement a **secure authentication system** for administrators and analysts[cite: 44].
* [cite_start]To utilize **HDFS (Hadoop Distributed File System)** for scalable storage of climate datasets[cite: 51].
* [cite_start]To develop **MapReduce jobs** for parallel processing of weather records[cite: 54].
* [cite_start]To create **Machine Learning models** (Random Forest) to predict temperature trends and identify anomalies[cite: 61, 62].
* [cite_start]To provide an **interactive web dashboard** for data visualization[cite: 64].

---

## 6. System Requirements

### [cite_start]Hardware Requirements [cite: 98]
* **Processor:** Intel Core i5 (minimum) / i7 (recommended)
* **RAM:** 16 GB
* **Storage:** 500 GB SSD
* **OS:** Windows 10 (64-bit) or higher

### [cite_start]Software Requirements [cite: 104]
* **Languages:** Python (Flask, Pandas, Scikit-Learn), HTML/CSS/JS
* **Big Data Tools:** Apache Hadoop, HDFS, Impala Server
* **Database:** MongoDB (Compass/Shell)
* **IDE:** VS Code / PyCharm / Jupyter Notebook
* **Visualization:** Tableau / Matplotlib

---

## 7. System Analysis & Design

### A. System Architecture
*(Insert a diagram here showing: Data Sources (Satellites) -> Ingestion (Python) -> Storage (HDFS/MongoDB) -> Processing (MapReduce/ML) -> Frontend (Flask Web App))*

### [cite_start]B. Data Flow Diagrams (DFD) 
* **Level 0 (Context Diagram):** Show the "User" interacting with the "EarthScape System" (Input: Login/Data; Output: Visualizations/Alerts).
* **Level 1 (Process Flow):**
    1. User Logs in (Auth Module).
    2. Admin uploads CSV -> Script sends to HDFS.
    3. Analyst requests prediction -> ML Engine processes data -> Returns Graph.
    4. System detects high temp -> Notifications Module sends Email.

### C. Flowcharts
*(Draw a simple flowchart for the Login Logic and the Prediction Logic)*

---

## 8. Implementation Details

### Key Modules Developed:
1.  **Authentication:** Uses `flask_login` and `werkzeug.security` for password hashing.
2.  **Big Data Processing:**
    * **Ingestion:** Python script using `hdfs` subprocess commands.
    * **MapReduce:** `mrjob` script to calculate average temperatures per year.
3.  **Machine Learning:**
    * **Algorithm:** Random Forest Regressor.
    * **Accuracy:** (Mention the R2 score you got in Colab).
4.  **Web Interface:** Flask-based dashboard with Jinja2 templates.

### Code Snippets
*(Copy specific interesting functions here, e.g., the `predict_temperature` function from `ml_engine.py` or the `mapper` function from `map_reduce_jobs.py`)*

---

## 9. Testing & Screenshots
* **Unit Testing:** Mention testing the Login function (valid vs. invalid credentials).
* **Integration Testing:** Testing the flow from Dashboard -> Prediction -> Result Display.
* **Screenshots:**
    * [Paste Screenshot of Login Page]
    * [Paste Screenshot of Dashboard with a Graph]
    * [Paste Screenshot of "System Alerts" Email]

---

## 10. Conclusion
The EarthScape Climate Monitoring System successfully integrates Big Data technologies with a user-friendly web interface. It meets the core requirements of storage, processing, and visualization, providing the agency with actionable insights to mitigate climate change impacts.

---


