#!/usr/bin/env python3
"""Conversion of transactions.

This module converts Schwab transactions to Portfolio Performance ones.
"""

import sys
import re
from pathlib import Path

import pandas as pd


def remove_currency(text: str) -> str:
    """Remove currency symbol from string. Work for negative values."""
    import locale
    import re
    
    # Handle NaN values
    if pd.isna(text):
        return ""
    
    decimal_point_char = locale.localeconv()["decimal_point"]
    clean = re.sub(r"[^0-9" + decimal_point_char + "-" + r"]+", "", text)
    return clean


def convert(schwab_csv: Path, pp_csv: Path) -> int:
    """Convert transactions from Charles Schwab for Portfolio Performance.

    Convert a transactions CSV file from Charles Schwab to an equivalent and
    ready-to-import CSV file for Portfolio Performance.
    """
    # Check if CSV has prefix and suffix rows that need to be skipped
    # Prefix: "Transactions  for account..."
    # Suffix: "Transactions Total"
    # Expected header: "Date","Action","Symbol","Description","Quantity","Price","Fees & Comm","Amount"
    expected_header = 'Date","Action","Symbol","Description","Quantity","Price","Fees & Comm","Amount'
    prefix_pattern = re.compile(r'^"Transactions\s+for account', re.IGNORECASE)
    suffix_pattern = re.compile(r'^"Transactions Total"', re.IGNORECASE)
    
    # Read first few lines to check for prefix
    with open(schwab_csv, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        second_line = f.readline().strip()
        
        # Check if first line is prefix
        skip_first_row = bool(prefix_pattern.match(first_line))
        
        # If skipping first row, header should be in second line
        # Otherwise, header should be in first line
        if skip_first_row:
            header_line = second_line
        else:
            header_line = first_line
        
        # Verify header matches expected format
        if expected_header not in header_line:
            # If we were planning to skip first row but header doesn't match,
            # maybe we shouldn't skip it
            if skip_first_row and expected_header in first_line:
                skip_first_row = False
                header_line = first_line
            else:
                raise ValueError(f"Unexpected CSV header format. Expected header containing: {expected_header}")
    
    # Read last line to check for suffix
    with open(schwab_csv, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            skip_last_row = bool(suffix_pattern.match(last_line))
        else:
            skip_last_row = False
    
    # A Charles Scwab CSV may start with a prefix and end with a suffix row
    # Prefix: "Transactions  for account..."
    # Suffix: "Transactions Total"
    # They are ignored if present.
    dtype = {
        "Date": str,
        "Symbol": str,
        "Fees & Comm": str,  # must keep as string, in case of floating-point rounding errors.
        "Amount": str,  # must keep as string, in case of floating-point rounding errors.
    }
    
    skiprows = 1 if skip_first_row else 0
    skipfooter = 1 if skip_last_row else 0
    
    df = pd.read_csv(
        schwab_csv, 
        skiprows=skiprows, 
        skipfooter=skipfooter, 
        dtype=dtype, 
        engine="python"
    )
    df["Symbol"] = df["Symbol"].fillna("")

    # Rename column names
    column_new_names = {
        "Action": "Note",
        "Symbol": "Ticker Symbol",
        "Description": "Security Name",
        "Quantity": "Shares",
        "Fees & Comm": "Fees",
        "Amount": "Value",
    }
    df.rename(columns=column_new_names, inplace=True)

    # Remove US dollar symbol
    new_value = df["Value"].fillna("").apply(remove_currency)
    df["Value"] = new_value
    
    # Remove US dollar symbol from Fees column if present
    new_fees = df["Fees"].fillna("").apply(remove_currency)
    df["Fees"] = new_fees

    # Hard-coding. Assume all transactions are in USD.
    # Add a new column: Transaction Currency
    df["Transaction Currency"] = ["USD"] * len(df.index)

    # Convert Action (Schwab) to Type (Portfolio Performance)
    """
    "Deposit/Removal (or withdrawal): Depositing or withdrawing funds will 
    respectively increase or decrease the value of a deposit account."
    Ref: https://help.portfolio-performance.info/en/reference/transaction/

    So a Schwab "Wire Sent" is a PP "Removal".

    Bank Interest as Dividend was introduced in commit 
    297f429979d4588f8871ad6d23d70f0557de9420 by @sdtom. After review, as Interest 
    is probably more appropriate.
    """
    action_to_type = {
        "NRA Tax Adj": "Taxes",
        "Credit Interest": "Interest",
        "NRA Withholding": "Taxes",
        "Short Term Cap Gain": "Dividend",
        "Long Term Cap Gain": "Dividend",
        "Cash Dividend": "Dividend",
        "Buy": "Buy",
        "Sell": "Sell",
        "Wire Received": "Deposit",
        "Wire Sent": "Removal",
        "Advisor Fee": "Fees",
        "Reinvest Dividend": "Dividend",
        "Reinvest Shares": "Buy",
        "Bank Interest": "Interest",
        "Funds Received": "Deposit",
        "MoneyLink Transfer": "Deposit",
        "Stock Plan Activity": "Buy",
        "Qualified Dividend": "Dividend",
        "Adjustment": "Taxes",
        "Misc Cash Entry": "Fees",
        "Service Fee": "Fees",
    }
    new_type = [action_to_type[x] for x in df["Note"]]
    df["Type"] = new_type

    # Delete Price column because PP seems not to have this column for a
    # transaction.
    df.drop(columns=["Price"], inplace=True)

    # If "Ticker Symbol" column is not empty, then "Security Name" column
    # contains the name of the security. Otherwise it's a description.
    # If latter, append to "Note" column.
    new_security_name: list[str] = []
    for k, v in df["Ticker Symbol"].items():
        if len(v) == 0:
            new_security_name.append("")
            df.at[k, "Note"] = df.at[k, "Note"] + " " + df.at[k, "Security Name"]
        else:
            new_security_name.append(df.at[k, "Security Name"])
    df["Security Name"] = new_security_name

    # Convert dates to datetime objects
    new_date: list[str] = []
    for k, v in df["Date"].items():
        multiple = v.split(" as of ", 1)
        new_date.append(multiple[0])
        if len(multiple) > 1:
            if len(df.at[k, "Note"]):
                df.at[k, "Note"] = df.at[k, "Note"] + " as of " + multiple[1]
            else:
                df.at[k, "Note"] = "as of " + multiple[1]

    df["Date"] = pd.to_datetime(new_date, format="%m/%d/%Y")

    # Write to CSV file
    df.to_csv(pp_csv, index=False, date_format="%Y-%m-%d")
    # print(pp_csv)

    return 0


# Allow the script to be run standalone (useful during development).
if __name__ == "__main__":
    sys.exit(convert(Path("in.csv"), Path("out.csv")))
