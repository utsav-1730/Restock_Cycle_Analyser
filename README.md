


# 📦 Walmart Logistics & Stockout Dashboard

This project visualizes and analyzes truck delivery delays and stockout behaviors across key Walmart departments using realistic, scenario-based mock data. Built with **Python**, **Pandas**, **Matplotlib**, **Seaborn**, and **Streamlit**, this interactive dashboard provides a real-world simulation of how operations, delays, and inefficiencies manifest inside Walmart stores.

---

## 🎯 Objectives

- Understand how **delivery timing** impacts **shelf availability**
- Track **top delay reasons** affecting restocking workflows
- Identify **departments most prone to stockouts**
- Simulate **real-world decision-making** with data-backed insights

---

## 📊 Features

- Filter by **Department** and **Date Range**
- View:
  - **Delay Reason Frequency**
  - **Average Stocking Delay (minutes)**
  - **Stockouts by Department**
  - **Truck Volume per Day**
- KPI summaries and full interactive data table
- Built for use by:
  - Store operations managers
  - Transportation teams
  - Inventory analysts

---

## 🧠 Key Findings

| Metric                  | Insight                                                                 |
|-------------------------|-------------------------------------------------------------------------|
| Top Delay Reason        | `Late Truck` and `Staff Shortage` lead in delay causes                 |
| Most Affected Depts     | `Garden Centre`, `Produce`, and `Dairy` show recurring stockouts       |
| Avg Delay by Dept       | `Frozen`, `Grocery`, and `General Merchandise` show longest delays     |
| Daily Volume Trends     | Delivery surges occur mid-week (Tue–Thu), matching stocking pressure   |

---

## 💡 Operational Recommendations

1. **Late Truck Arrival**:
   - Improve supplier/truck dispatch coordination
   - Introduce real-time GPS alerting + predictive ETA tools

2. **Staff Shortage**:
   - Schedule peak-hour labor with delay forecasts
   - Cross-train unloaders and sales floor staff for dynamic handoffs

3. **Stockouts in Key Depts**:
   - Use ML to forecast high-demand SKUs (e.g., soil in Garden Centre)
   - Auto-alert replenishment if shelf lag > 2 hours from delivery

4. **Overall Logistics Optimization**:
   - Link truck data to CRM tools like Salesforce for unified visibility
   - Embed delay dashboards in store-level decision rooms

---

## 🧰 Tech Stack

- Python, Pandas, Matplotlib, Seaborn
- Streamlit (interactive dashboard)
- GitHub (version control & publishing)

---

## 🚀 Getting Started

```bash
pip install streamlit pandas matplotlib seaborn
streamlit run app.py
```

Ensure `Walmart_Logistics_Dataset.csv` is in the same directory.

---

## 📬 Contact

Made by [Utsav Changani](https://linkedin.com/in/utsav-changani-287589225/)  
GitHub: [@utsav-1730](https://github.com/utsav-1730)  
Portfolio: [utsavchangani.netlify.app](https://utsavchangani.netlify.app)

---
