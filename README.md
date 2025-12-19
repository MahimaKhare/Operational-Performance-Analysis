# 🛒 Vendor Performance Analysis  

This project is a **real-world Data Analyst portfolio project** where we analyze vendor performance using **SQL, Python, and Power BI**. The goal is to simulate an end-to-end data workflow — from data ingestion into a database, through exploratory analysis and reporting, to building a business-ready dashboard.  

---

## 📂 Project Workflow  

1. **Data Ingestion**  
   - Notebook: `ingestion_db.ipynb`  
   - Loads multiple CSV datasets into a **Postgres database** (`inventory`).  
   - Sets up structured tables for analysis.  

2. **Exploratory Data Analysis (EDA)**  
   - Notebook: `eda.ipynb`  
   - Performs data cleaning, transformation, and exploratory analysis on tables in `inventory`.  
   - Creates a **summary table** by joining data from multiple sources.  
   - Pushes the summary table back into Postgres for downstream use.  

3. **Scheduled Processing**  
   - Script: `vendor_summary.py`  
   - Automates the creation of vendor summary tables.  
   - Designed for **repetitive scheduled tasks** to ensure fresh data for analysis.  

4. **Vendor Performance Analysis**  
   - Notebook: `Vendor Performance Analysis.ipynb`  
   - Works on the final `vendor_sales_summary` table.  
   - Includes **visualizations, statistical analysis, and answering business questions** about vendor performance using Python.  

5. **Business Intelligence Dashboard**  
   - File: `VendorPerformance.pbix`  
   - Power BI dashboard built on top of the processed datasets.  
   - Provides **interactive insights** for stakeholders.  

---

## 📊 Tech Stack  

- **Database**: PostgreSQL  
- **Languages**: Python (Pandas, Matplotlib, Seaborn, SQLAlchemy)  
- **Visualization**: Power BI, Python plotting libraries  
- **Workflow Automation**: Python scripting  
- **Version Control**: Git & GitHub  

---

## 📁 Repository Structure  
├── ingestion_db.ipynb # Load CSVs into Postgres
├── eda.ipynb # Data cleaning & exploratory analysis
├── Vendor Performance Analysis.ipynb # Vendor-level analysis & visualizations
├── vendor_summary.py # Script for scheduled summary table creation
├── VendorPerformance.pbix # Power BI dashboard
├── logs/ # Log files for ingestion & vendor summary
├── begin_inventory.csv # Dataset (sample inventory start)
├── end_inventory.csv # Dataset (sample inventory end)
├── purchase_prices.csv # Dataset (purchase prices)
├── vendor_invoice.csv # Dataset (vendor invoices)
├── vendor_sales_summary.csv # Final summarized dataset
└── README.md # Project documentation


---

## 📂 Large Files  

The following files were excluded from GitHub due to size limits:  

- `sales.csv` (~1.5 GB)  
- `purchases.csv` (~345 MB)  

👉 These files are essential for running the project. You can download them here:  
- [sales.csv][(https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_1)](https://drive.google.com/file/d/1nNrb2NDydrIEvkwplzkv7RVpzHSrmPa3/view?usp=drive_link)  
- [purchases.csv][(https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_2)](https://drive.google.com/file/d/1NeLmTwc7MG2HIG5s4BLsuWixVM7pdlG9/view?usp=drive_link)

---

## 🚀 How to Run  

1. Clone this repo:  

   ```bash
   git clone https://github.com/MahimaKhare/Operational-Performance-Analysis.git
   cd VendorPerformance

2. Set up a PostgreSQL database named inventory.

3. Run ingestion_db.ipynb to load all datasets.

4. Execute eda.ipynb to perform EDA and create the summary table.

5. Use vendor_summary.py to automate summary table updates (can be scheduled with cron/Task Scheduler).

6. Open and run Vendor Performance Analysis.ipynb for insights.

7. Explore the Power BI dashboard (VendorPerformance.pbix) for interactive visualizations.

📌 Key Insights

- Built an end-to-end ETL pipeline with PostgreSQL + Python.

- Designed automated scripts to refresh vendor summary tables.

- Answered business-driven questions using Python analysis.

- Created an interactive Power BI dashboard for stakeholders.
