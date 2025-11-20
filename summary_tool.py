import pandas as pd

# Path to your CSV file
CSV_FILE = "financial_transactions.csv"


def load_transactions(csv_path: str = CSV_FILE) -> pd.DataFrame:
    """
    Load the financial_transactions.csv file and convert the 'date' column to datetime.
    """
    df = pd.read_csv(csv_path)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows where date failed to convert
    df = df.dropna(subset=["date"])

    return df


def add_year_month_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a new column 'year_month' in YYYY-MM format based on the 'date' column.
    """
    df = df.copy()
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    return df


def get_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a monthly summary showing:
    - total income
    - total expenses
    - net amount (income - expenses)
    """

    # Ensure 'year_month' exists
    if "year_month" not in df.columns:
        df["year_month"] = df["date"].dt.strftime("%Y-%m")

    # Income = positive values
    df["income"] = df["amount"].apply(lambda x: x if x > 0 else 0)

    # Expenses = absolute value of negative numbers
    df["expenses"] = df["amount"].apply(lambda x: abs(x) if x < 0 else 0)

    # Group by month and calculate totals
    monthly_summary = df.groupby("year_month").agg(
        total_income=("income", "sum"),
        total_expenses=("expenses", "sum"),
        net_amount=("amount", "sum")  # sum of original amount column
    ).reset_index()

    return monthly_summary


if __name__ == "__main__":
    # Load dataset
    df = load_transactions()

    # Task 18
    df = add_year_month_column(df)
    print("\nSample dates with year_month (Task 18):")
    print(df[["date", "year_month"]].head())

    # Task 19
    print("\nMonthly summary (Task 19):")
    monthly = get_monthly_summary(df)
    print(monthly.head())
