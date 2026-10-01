# 💸 Student Expense Tracker

A simple, clean, and professional web application built with **Python** and **Streamlit** that helps students record, monitor, and analyse their daily expenses.

---

## 📌 Problem Statement

Students often struggle to keep track of daily spending across multiple categories like food, transport, and books. Without a clear picture of where money goes, it is easy to overspend and fall short before the end of the month. This application gives students a lightweight, easy-to-use tool to log expenses, set a monthly budget, and spot spending patterns — all without needing any database or internet connection.

---

## ✨ Features

| Feature | Details |
|---|---|
| ➕ Add Expense | Log date, category, amount, and an optional note |
| ✅ Validation | Rejects expenses with amount ≤ ₹ 0 |
| 📊 Dashboard | Metric cards for total spent, expense count, top category, this month's spending |
| 💰 Monthly Budget | Set a budget, track progress with a visual bar, get over-budget alerts |
| 📈 Analysis | Bar chart, donut chart, and monthly trend line powered by Altair |
| 🔍 Category Filter | Filter all charts and tables to one or more categories |
| 🗑️ Delete Expense | Remove any expense from the list |
| ⬇️ Download CSV | Export expense data at any time |
| 💾 Local Storage | All data saved to `expenses.csv` — no server, no database |

---

## 🛠️ Technologies Used

| Technology | Version | Role |
|---|---|---|
| Python | 3.10+ | Core language |
| Streamlit | ≥ 1.57 | Web UI framework |
| Pandas | ≥ 2.0 | Data loading, filtering, aggregation |
| Altair | ≥ 5.0 | Interactive charts (bar, donut, line) |

---

## 📁 Project Structure

```
student-expense-tracker/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── sample_expenses.csv     # Sample data for testing (copy to expenses.csv)
├── README.md               # Project documentation
├── .gitignore              # Files excluded from version control
└── expenses.csv            # Live data file (auto-created on first save)
```

---

## ⚙️ Installation

### 1. Clone or download the project

```bash
git clone https://github.com/vanamsurajsagar/Student-Expense-Tracker.git
cd Student-Expense-Tracker
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Load sample data

Copy the sample file to use as your starting dataset:

```bash
# Windows
copy sample_expenses.csv expenses.csv
# macOS / Linux
cp sample_expenses.csv expenses.csv
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Streamlit will open the app automatically in your default browser at **http://localhost:8501**.

---

## 🤖 How IBM Bob Was Used

IBM Bob (an AI-powered coding assistant) was used throughout this project to accelerate development:

1. **Project planning** — Bob generated a detailed implementation plan covering file structure, tab layout, data model, and chart design before a single line of code was written.
2. **Code generation** — The complete `app.py` was scaffolded by Bob, including the data helpers (`load_data`, `save_data`, `format_inr`), all five tabs, Altair chart specifications, and session state handling for the budget feature.
3. **Sample data** — Bob created `sample_expenses.csv` with 30 realistic rows spanning three months and all seven categories.
4. **Error detection and fixing** — Bob ran syntax checks, import validation, and a live Streamlit startup test, then resolved any issues found before delivery.
5. **Documentation** — This README was written by Bob following the project requirements.

Using IBM Bob reduced development time from several hours to under 30 minutes while producing clean, maintainable code that follows Streamlit best practices.

---

## 🚀 Future Improvements

- **Multiple users / profiles** — Allow each student to maintain a separate expense log.
- **Recurring expenses** — Mark expenses like rent as recurring so they auto-populate each month.
- **Export to PDF** — Generate a monthly expense report as a PDF.
- **Currency selector** — Support currencies beyond INR for international students.
- **Dark mode theme** — Add a toggle for a dark Streamlit theme.
- **Notifications / reminders** — Email or browser alerts when the budget is 80 % used.
- **Cloud sync** — Optional sync to Google Sheets or a cloud database for multi-device access.
- **Authentication** — Simple PIN or password protection for privacy.

---

## 📄 License

This project is open-source and free to use for educational purposes.
