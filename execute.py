import json
import pandas as pd

def main():
    """
    Reads data.csv (converted from data.xlsx), performs a simple sanity check,
    and writes the dataframe to result.json in JSON records orientation.

    This script is compatible with Python 3.11+ and pandas 2.3+.
    """
    # Read the CSV converted from the provided Excel file.
    # Using dtype=str to preserve original formatting where appropriate.
    try:
        df = pd.read_csv("data.csv", dtype=str)
    except FileNotFoundError:
        # Fallback: if data.csv isn't present but data.xlsx exists in the same directory,
        # try to read it and save as CSV for local convenience.
        try:
            df = pd.read_excel("data.xlsx", dtype=str)
            df.to_csv("data.csv", index=False)
        except FileNotFoundError:
            raise SystemExit("Neither data.csv nor data.xlsx were found in the repository root.")

    # Basic validation: ensure dataframe is not empty
    if df.empty:
        raise SystemExit("Input data is empty. Aborting.")

    # Example transformation: strip whitespace from string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(lambda v: v.strip() if isinstance(v, str) else v)

    # Output to JSON file in records orientation
    result = df.to_dict(orient="records")

    # Write to stdout-compatible JSON file
    with open("result.json", "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()