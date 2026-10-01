import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, datetime
import os

# ── Constants ────────────────────────────────────────────────────────────────
CSV_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Health", "Other"]
COLUMNS = ["date", "category", "amount", "note"]

# ── Data helpers ─────────────────────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    """Load expenses from CSV, returning an empty DataFrame if file is missing."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, parse_dates=["date"])
        # Ensure correct dtypes even if file was partially written
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = "" if col in ("category", "note") else 0.0
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        df["note"] = df["note"].fillna("")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        return df[COLUMNS].reset_index(drop=True)
    return pd.DataFrame(
        {"date": pd.Series(dtype="datetime64[ns]"),
         "category": pd.Series(dtype="str"),
         "amount": pd.Series(dtype="float64"),
         "note": pd.Series(dtype="str")}
    )


def save_data(df: pd.DataFrame) -> None:
    """Persist the DataFrame to CSV."""
    df.to_csv(CSV_FILE, index=False)


def format_inr(amount: float) -> str:
    """Format a number as Indian Rupees: ₹ 1,234.50"""
    return f"₹ {amount:,.2f}"


def current_month_label() -> str:
    now = datetime.now()
    return f"{now.year}-{now.month:02d}"


def filter_current_month(df: pd.DataFrame) -> pd.DataFrame:
    now = datetime.now()
    return df[(df["date"].dt.year == now.year) & (df["date"].dt.month == now.month)]


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="💸",
    layout="wide",
)

st.title("💸 Student Expense Tracker")
st.caption("Track your daily expenses, set a monthly budget, and analyse your spending habits.")

# ── Session state defaults ────────────────────────────────────────────────────
if "budget" not in st.session_state:
    st.session_state["budget"] = 0.0

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_add, tab_dash, tab_budget, tab_analysis, tab_manage = st.tabs(
    ["➕ Add Expense", "📊 Dashboard", "💰 Monthly Budget", "📈 Analysis", "🗑️ Manage Data"]
)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — ADD EXPENSE
# ═════════════════════════════════════════════════════════════════════════════
with tab_add:
    st.subheader("Add a New Expense")
    st.markdown("Fill in the details below and click **Save Expense**.")

    col1, col2 = st.columns(2)
    with col1:
        expense_date = st.date_input("Date", value=date.today())
        expense_category = st.selectbox("Category", CATEGORIES)
    with col2:
        expense_amount = st.number_input(
            "Amount (₹)", min_value=0.0, value=0.0, step=1.0, format="%.2f"
        )
        expense_note = st.text_input("Note (optional)", placeholder="e.g. Lunch at canteen")

    if st.button("💾 Save Expense", use_container_width=True):
        if expense_amount <= 0:
            st.error("⚠️ Amount must be greater than ₹ 0.00. Please enter a valid amount.")
        else:
            df = load_data()
            new_row = pd.DataFrame(
                [[pd.Timestamp(expense_date), expense_category, expense_amount, expense_note]],
                columns=COLUMNS,
            )
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success(
                f"✅ Expense saved! {expense_category} — {format_inr(expense_amount)} on {expense_date.strftime('%d %b %Y')}"
            )
            st.balloons()

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
with tab_dash:
    st.subheader("Dashboard")
    df = load_data()

    if df.empty:
        st.info("No expenses recorded yet. Go to **➕ Add Expense** to get started!")
    else:
        month_df = filter_current_month(df)

        total_spent = df["amount"].sum()
        num_expenses = len(df)
        top_category = (
            df.groupby("category")["amount"].sum().idxmax() if not df.empty else "—"
        )
        month_spent = month_df["amount"].sum()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("💰 Total Spent (All Time)", format_inr(total_spent))
        m2.metric("🧾 Total Expenses", str(num_expenses))
        m3.metric("🏆 Top Category", top_category)
        m4.metric(f"📅 This Month ({current_month_label()})", format_inr(month_spent))

        st.markdown("---")
        st.markdown("### All Expenses")

        display_df = df.copy().sort_values("date", ascending=False)
        display_df["date"] = display_df["date"].dt.strftime("%d %b %Y")
        display_df["amount"] = display_df["amount"].apply(format_inr)
        display_df.columns = ["Date", "Category", "Amount", "Note"]

        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — MONTHLY BUDGET
# ═════════════════════════════════════════════════════════════════════════════
with tab_budget:
    st.subheader("Monthly Budget Tracker")
    st.markdown(
        f"Set your budget for **{datetime.now().strftime('%B %Y')}** and monitor your spending."
    )

    budget_input = st.number_input(
        "Set Monthly Budget (₹)",
        min_value=0.0,
        value=float(st.session_state["budget"]),
        step=500.0,
        format="%.2f",
        key="budget_input_field",
    )
    if st.button("✅ Apply Budget"):
        st.session_state["budget"] = budget_input
        st.success(f"Budget set to {format_inr(budget_input)}.")

    budget = st.session_state["budget"]
    df = load_data()
    month_df = filter_current_month(df)
    month_spent = month_df["amount"].sum()

    st.markdown("---")

    b1, b2, b3 = st.columns(3)
    b1.metric("📊 Monthly Budget", format_inr(budget))
    b2.metric("💸 Spent This Month", format_inr(month_spent))
    remaining = budget - month_spent
    b3.metric(
        "🏦 Remaining",
        format_inr(max(remaining, 0)),
        delta=None,
    )

    if budget > 0:
        progress = min(month_spent / budget, 1.0)
        st.progress(progress)
        pct = (month_spent / budget) * 100

        if month_spent > budget:
            overspent = month_spent - budget
            st.error(
                f"🚨 Over Budget! You have exceeded your budget by **{format_inr(overspent)}** "
                f"({pct:.1f}% of budget used)."
            )
        elif pct >= 80:
            st.warning(
                f"⚠️ You have used {pct:.1f}% of your monthly budget. Spend carefully!"
            )
        else:
            st.success(f"✅ You have used {pct:.1f}% of your monthly budget. Looking good!")
    else:
        st.info("Enter a budget above and click **Apply Budget** to start tracking.")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
with tab_analysis:
    st.subheader("Spending Analysis")
    df = load_data()

    if df.empty:
        st.info("No expenses to analyse yet. Add some expenses first!")
    else:
        # ── Category filter ──────────────────────────────────────────────────
        selected_cats = st.multiselect(
            "Filter by Category (leave empty to show all)",
            options=CATEGORIES,
            default=[],
        )
        filtered_df = df[df["category"].isin(selected_cats)] if selected_cats else df.copy()

        if filtered_df.empty:
            st.warning("No expenses match the selected categories.")
        else:
            # ── Spending totals table ────────────────────────────────────────
            st.markdown("### Spending by Category")
            cat_totals = (
                filtered_df.groupby("category")["amount"]
                .sum()
                .reset_index()
                .sort_values("amount", ascending=False)
            )
            cat_totals.columns = ["Category", "Total (₹)"]
            cat_totals["Total (₹)"] = cat_totals["Total (₹)"].apply(format_inr)
            st.dataframe(cat_totals, use_container_width=True, hide_index=True)

            # ── Charts ───────────────────────────────────────────────────────
            cat_chart_data = (
                filtered_df.groupby("category")["amount"]
                .sum()
                .reset_index()
                .rename(columns={"category": "Category", "amount": "Amount"})
            )

            col_bar, col_donut = st.columns(2)

            with col_bar:
                st.markdown("### Category Bar Chart")
                bar_chart = (
                    alt.Chart(cat_chart_data)
                    .mark_bar()
                    .encode(
                        x=alt.X("Amount:Q", title="Total Spent (₹)"),
                        y=alt.Y("Category:N", sort="-x", title=""),
                        color=alt.Color("Category:N", legend=None),
                        tooltip=["Category:N", alt.Tooltip("Amount:Q", format=",.2f")],
                    )
                    .properties(height=300)
                )
                st.altair_chart(bar_chart, use_container_width=True)

            with col_donut:
                st.markdown("### Spending Share (Donut)")
                donut_chart = (
                    alt.Chart(cat_chart_data)
                    .mark_arc(innerRadius=60)
                    .encode(
                        theta=alt.Theta("Amount:Q"),
                        color=alt.Color("Category:N"),
                        tooltip=["Category:N", alt.Tooltip("Amount:Q", format=",.2f")],
                    )
                    .properties(height=300)
                )
                st.altair_chart(donut_chart, use_container_width=True)

            # ── Monthly trend ─────────────────────────────────────────────────
            st.markdown("### Monthly Spending Trend")
            trend_df = filtered_df.copy()
            trend_df["month"] = trend_df["date"].dt.to_period("M").astype(str)
            monthly = (
                trend_df.groupby("month")["amount"]
                .sum()
                .reset_index()
                .rename(columns={"month": "Month", "amount": "Amount"})
                .sort_values("Month")
            )

            trend_chart = (
                alt.Chart(monthly)
                .mark_line(point=True, color="#3b82d4")
                .encode(
                    x=alt.X("Month:O", title="Month"),
                    y=alt.Y("Amount:Q", title="Total Spent (₹)"),
                    tooltip=["Month:O", alt.Tooltip("Amount:Q", format=",.2f")],
                )
                .properties(height=300)
            )
            st.altair_chart(trend_chart, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — MANAGE DATA
# ═════════════════════════════════════════════════════════════════════════════
with tab_manage:
    st.subheader("Manage Data")
    df = load_data()

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("### 📥 Download Expenses")
    if df.empty:
        st.info("No data to download yet.")
    else:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download expenses.csv",
            data=csv_bytes,
            file_name="expenses.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")

    # ── Delete ────────────────────────────────────────────────────────────────
    st.markdown("### 🗑️ Delete an Expense")
    if df.empty:
        st.info("No expenses to delete.")
    else:
        df_display = df.copy()
        df_display["label"] = (
            df_display["date"].dt.strftime("%d %b %Y")
            + " | "
            + df_display["category"]
            + " | "
            + df_display["amount"].apply(format_inr)
            + (
                df_display["note"].apply(
                    lambda n: f" | {n}" if str(n).strip() else ""
                )
            )
        )
        labels = df_display["label"].tolist()
        selected_label = st.selectbox("Select expense to delete", labels)
        selected_index = labels.index(selected_label)

        st.markdown(
            f"**Selected:** {labels[selected_index]}"
        )

        if st.button("🗑️ Delete Selected Expense", type="primary", use_container_width=True):
            df = df.drop(index=selected_index).reset_index(drop=True)
            save_data(df)
            st.success("✅ Expense deleted successfully.")
            st.rerun()
