import pandas as pd

# Default path to the CSV file (same folder as this .py file)
CSV_FILE = "financial_transactions.csv"


def load_transactions(csv_path: str = CSV_FILE) -> pd.DataFrame:
    """
    Load the financial_transactions.csv file and convert the 'date' column to datetime.
    """
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def add_year_month_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a new column 'year_month' in YYYY-MM format based on the 'date' column.
    """
    df = df.copy()
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    return df


if __name__ == "__main__":
    # Small test to verify Task #18
    df = load_transactions()
    df = add_year_month_column(df)
    print(df[["date", "year_month"]].head())
