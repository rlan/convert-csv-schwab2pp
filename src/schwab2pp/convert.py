#!/usr/bin/env python3

import sys
from pathlib import Path

import pandas as pd


def remove_currency(text: str) -> str:
    """Removes currency symbol from string. Works for negative values."""
    import locale
    import re

    decimal_point_char = locale.localeconv()["decimal_point"]
    clean = re.sub(r"[^0-9" + decimal_point_char + "-" + r"]+", "", text)
    return clean


def convert(schwab_csv: Path, pp_csv: Path) -> int:
    """Converts transactions from Charles Schwab to Portfolio Performance.

    Converts a transactions CSV file from Charles Schwab to an equivalent and
    ready-to-import CSV file for Portfolio Performance.
    """

    # A Charles Scwab CSV starts with a prefix and a suffix row
    # Prefix: "Transactions  for account..."
    # Suffix: "Transactions Total"
    # They are ignored.
    dtype = {
        "Date": str,
        "Symbol": str,
        "Fees & Comm": str,  # must keep as string, in case of floating-point rounding errors.
        "Amount": str,  # must keep as string, in case of floating-point rounding errors.
    }
    df = pd.read_csv(schwab_csv, skiprows=1, skipfooter=1, dtype=dtype, engine="python")
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
    new_value = df["Value"].apply(remove_currency)
    df["Value"] = new_value

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
