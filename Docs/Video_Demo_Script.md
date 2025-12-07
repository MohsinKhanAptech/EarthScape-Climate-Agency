# Video Demonstration Script & Checklist

**Project:** EarthScape Climate Monitoring System
**Target Duration:** ~90 Seconds

---

## 1. Pre-Recording Checklist
Before you start recording, ensure the following setup is complete:

- [ ] **Server Running:** Ensure `python run.py` is running in the terminal without errors.
- [ ] **Clean State:** If you want to show the "Sign Up" flow, ensure the username you plan to use doesn't already exist in the database.
- [ ] **Dataset Ready:** Place a copy of `GlobalLandTemperaturesByMajorCity.csv` (or a smaller dummy CSV) on your Desktop for quick access during the ingestion step.
- [ ] **Zoom Level:** Set your browser zoom to **100% or 110%** so the text and charts are clearly visible in the video.
- [ ] **Audio Check:** Test your microphone if you plan to narrate live.

---

## 2. Video Script

### **0:00 - 0:15 | Introduction & Home Page**
* **Action:** Start on the Home Page (`/`). Scroll down slowly to reveal the content.
* **Visual:** Show the "Global Warming Trend" red graph and the "Real-Time Data Analysis" statistics.
* **Narration:**
    > "This is the EarthScape Climate Monitoring System. It leverages Big Data and Machine Learning to track global temperature trends. As you can see, the home page visualizes historical data processed from our HDFS cluster to show global warming trends over the last century."

### **0:15 - 0:35 | User Authentication**
* **Action:** Click **"Sign Up"**.
* **Action:** Fill in a username (e.g., `Analyst_Demo`) and a password. Select "Climate Analyst" as the role. Click **"Create Account"**.
* **Action:** You will be redirected to the Sign In page. Enter the credentials you just created and log in.
* **Narration:**
    > "The system features a secure, role-based authentication system. I am registering a new Climate Analyst account to access the private prediction dashboard."

### **0:35 - 1:00 | The Analyst Dashboard (Core Feature)**
* **Action:** Land on the Dashboard. Mouse over the green **"HDFS Status: Online (Active)"** indicator at the top right.
* **Action:**
    1.  Select **"New York"** (or any city) from the "Select Region" dropdown.
    2.  Use the **Date Picker** to select a future date (e.g., **July 2030**).
    3.  Click the **"Run Prediction"** button.
* **Visual:** Point out the result card showing the specific temperature and the "Annual Trend Analysis" graph that appears below it.
* **Narration:**
    > "Here is the Analyst Dashboard, connected to our HDFS backend. Using the Random Forest engine, I can predict the average temperature for New York in July 2030. The system also dynamically generates a visualization of the yearly trend for that specific region."

### **1:00 - 1:15 | Data Ingestion**
* **Action:** Click **"Ingestion"** in the navigation bar.
* **Action:** Click the file input, select your CSV file from the Desktop, and click **"Start Ingestion"**.
* **Narration:**
    > "Admins can ingest raw satellite or sensor data directly into the Hadoop Distributed File System using this interface. The system handles data partitioning automatically."

### **1:15 - 1:30 | Support & Conclusion**
* **Action:** Click **"Support"** in the navigation bar. Briefly scroll through the form.
* **Action:** Click **"Logout"** in the top right.
* **Narration:**
    > "Finally, we have a dedicated support channel for reporting data anomalies or system issues. This concludes the demo of the EarthScape Big Data solution."

---

## 3. Final Technical Check
* Ensure `app/models/climate_model.pkl` is present in the `app/models/` folder.
* Ensure your internet connection is active (for Bootstrap/Fonts to load).
