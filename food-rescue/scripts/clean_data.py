import pandas as pd
from datetime import datetime
from pathlib import Path

# Folder where your CSV files are stored
DATA = Path("data")

# File paths mapping
files = {
    "providers": DATA / "providers_data.csv",
    "receivers": DATA / "receivers_data.csv",
    "food_listings": DATA / "food_listings_data.csv",
    "claims": DATA / "claims_data.csv"
}

def clean_dataframe(df):
    """
    Cleans a DataFrame:
    - Trims whitespace
    - Converts date/timestamp columns
    - Removes rows where 'name' column is missing or empty
    - Drops duplicates
    - Resets index
    """
    # Remove leading/trailing spaces from strings
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Convert date/timestamp columns to datetime
    for col in df.columns:
        if "date" in col.lower() or "timestamp" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Remove rows where 'name' column is missing or empty
    if "name" in df.columns:
        df = df[df["name"].notna() & (df["name"].str.strip() != "")]

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df

def main():
    for name, path in files.items():
        if path.exists():
            print(f"Cleaning {name}...")
            df = pd.read_csv(path)
            df = clean_dataframe(df)
            cleaned_path = path.with_name(path.stem + ".cleaned.csv")
            df.to_csv(cleaned_path, index=False)
            print(f"✅ Saved cleaned {name} to {cleaned_path}")
        else:
            print(f"⚠️ File not found: {path}")

if __name__ == "__main__":
    main()
