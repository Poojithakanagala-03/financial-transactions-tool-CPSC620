import pandas as pd

# Default path to the CSV file (same folder as this .py file)
FILE_PATH = "financial_transactions.csv"


# US-1: Load and clean data
def load_data(path: str = FILE_PATH) -> pd.DataFrame:
    """
    Load the financial_transactions.csv file,
    convert the 'date' column to datetime, and drop rows with invalid dates.
    """
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    return df


# US-2: Total income and expenses
def get_income_expense_summary(df: pd.DataFrame):
    """
    Return total income, total expenses, and net balance over all transactions.
    Assumes 'type' column has 'credit' (income) and 'debit' (expense).
    """
    income = df[df["type"] == "credit"]["amount"].sum()
    expenses = df[df["type"] == "debit"]["amount"].sum()
    net = income - expenses
    return income, expenses, net


# US-3: Summary by transaction type
def get_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary table with total amount and count of transactions by type.
    """
    type_totals = df.groupby("type")["amount"].sum()
    type_counts = df["type"].value_counts()

    result = pd.DataFrame(
        {
            "total_amount": type_totals,
            "count": type_counts,
        }
    )
    return result


# --- Task 18: year_month column helper ---------------------------------
def add_year_month_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a 'year_month' column in YYYY-MM format based on the 'date' column.
    """
    df = df.copy()
    if "year_month" not in df.columns:
        df["year_month"] = df["date"].dt.strftime("%Y-%m")
    return df


# --- Task 19: get_monthly_summary(df) -----------------------------------
def get_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a monthly summary showing:
      - total_income   (sum of credits)
      - total_expenses (sum of debits, as positive values)
      - net_amount     (income - expenses)

    Grouped by the 'year_month' column.
    """
    # Ensure year_month exists (Task 18)
    df = add_year_month_column(df)

    # Build helper columns for income and expenses
    income_mask = df["type"] == "credit"
    expense_mask = df["type"] == "debit"

    df = df.copy()
    df["income"] = df["amount"].where(income_mask, 0)
    df["expenses"] = df["amount"].where(expense_mask, 0).abs()

    # Group by month and calculate totals
    monthly = (
        df.groupby("year_month")
        .agg(
            total_income=("income", "sum"),
            total_expenses=("expenses", "sum"),
            net_amount=("amount", "sum"),  # credits positive, debits negative
        )
        .reset_index()
    )

    return monthly


# ---- Quick tests for your tasks (18 + 19) ------------------------------
if __name__ == "__main__":
    df = load_data()

    # Task 18 test: show dates with year_month
    df_with_month = add_year_month_column(df)
    print("Sample dates with year_month (Task 18):")
    print(df_with_month[["date", "year_month"]].head())

    # Task 19 test: monthly summary
    print("\nMonthly summary (Task 19):")
    monthly_summary = get_monthly_summary(df)
    print(monthly_summary.head())
