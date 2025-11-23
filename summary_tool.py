import pandas as pd

file_path = "financial_transactions.csv"

# ---------- DATA CLEANING ----------
def load_data(path):
    df = pd.read_csv(path)
    
    # Convert date safely
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    
    # Remove rows with invalid dates
    df = df.dropna(subset=["date"])
    
    return df


# ---------- TASK 18 ----------
def add_year_month_column(df):
    df = df.copy()
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    return df


# ---------- TASK 19 + 20 ----------
def get_monthly_summary(df):
    df = add_year_month_column(df)

    income = df[df["type"] == "credit"].groupby("year_month")["amount"].sum()
    expenses = df[df["type"] == "debit"].groupby("year_month")["amount"].sum()

    monthly_summary = pd.DataFrame({
        "total_income": income,
        "total_expenses": expenses
    }).fillna(0)

    monthly_summary["net_amount"] = (
        monthly_summary["total_income"] - monthly_summary["total_expenses"]
    )

    monthly_summary.reset_index(inplace=True)
    return monthly_summary


# ---------- TASK 21 : TEST OUTPUT ----------
if __name__ == "__main__":
    df = load_data(file_path)
    monthly_report = get_monthly_summary(df)

    print("✅ Monthly Summary Output:")
    print(monthly_report.head())

