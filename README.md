# 📊 LedgerLens – AI-Powered Financial Dashboard

## 🚀 Overview

LedgerLens is a financial analytics dashboard that processes financial reports (CSV) and generates meaningful insights such as spending patterns, category breakdowns, and risk detection.

The system follows a **Layered + MVC architecture**, ensuring modularity, scalability, and clean separation of concerns. 

---

## ✨ Features

* 📤 Upload financial reports (CSV)
* 📊 Interactive dashboard with charts
* 🧠 Smart insights (rule-based AI)
* ⚠️ Risk detection (anomaly-based transactions)
* 📈 Category-wise expense visualization
* 📉 Spending trend analysis

---

## 🏗️ Tech Stack

### Frontend

* React (Create React App)
* Axios (API calls)
* Recharts (data visualization)

### Backend

* FastAPI
* Pandas (data processing)

### Architecture

* Layered Architecture
* MVC Pattern

---

## ⚙️ Project Structure

```
ledgerlens/
├── backend/
│   ├── app.py
│   └── venv/
│
└── frontend/
    └── ledgerlens-ui/
        ├── src/
        │   └── App.js
        ├── public/
        └── package.json
```

---

## 🔄 System Workflow

1. User uploads a financial report (CSV)
2. Backend processes and analyzes data
3. Transactions are categorized
4. Insights and risk alerts are generated
5. Results are displayed on dashboard

---

## 📥 Installation & Setup

### 🔧 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Mac/Linux
pip install fastapi uvicorn pandas python-multipart
uvicorn app:app --reload
```

---

### 🎨 Frontend Setup

```bash
cd frontend/ledgerlens-ui
npm install
npm install axios recharts
npm start
```

---

## 📊 Sample Data Format

```csv
date,description,amount,category
2024-01-01,Amazon,1200,Shopping
2024-01-02,Swiggy,300,Food
2024-01-03,Uber,250,Transport
2024-01-04,Salary,50000,Income
```

---

## 🧠 Risk Detection Logic

* Transactions exceeding **2× average spending** are flagged as risky
* Helps identify anomalies and unusual spending behavior

---

## 🖥️ Dashboard Components

* 💰 Total Spending
* 📉 Average Transaction Value
* ⚠️ Risk Alerts Panel
* 🥧 Category-wise Pie Chart
* 📈 Spending Trend Line Chart

---

## 🎯 Use Cases

* Personal finance tracking
* Expense analysis
* Fraud detection (basic)
* Financial insights for decision making

---

## 🚧 Future Enhancements

* PDF report processing (OCR)
* Machine Learning-based categorization
* Real-time analytics
* User authentication system
* Cloud deployment

---

## 🤝 Contributing

Feel free to fork this project and enhance it with more advanced analytics and UI improvements.

---

## 📌 Conclusion

LedgerLens provides a simple yet powerful way to analyze financial data through an intuitive dashboard. Its modular architecture and real-time insights make it a scalable solution for financial analytics.

---
