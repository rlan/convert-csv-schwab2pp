#!/usr/bin/env python3

import argparse
import os.path
import sys

try:
    import pandas as pd
except ImportError:
    raise ImportError('Is Pandas installed?')


parser = argparse.ArgumentParser(
    description=('Converts a Charles Schwab transaction CSV file to a'
                 ' ready-to-import CSV file for Portfolio Performance.'))
parser.add_argument(
    'schwab_csv', type=str,
    help='Input Charles Schwab CSV file')
parser.add_argument(
    '-p', '--pp_csv', type=str,
    default='pp.csv',
    help='Resulting CSV file for Portfolio Performance (default: pp.csv)')
args = parser.parse_args()


if not os.path.isfile(args.schwab_csv):
    print(f'{args.schwab_csv} not found')
    sys.exit(1)


# A Charles Scwab CSV starts with a prefix and a suffix row
# Prefix: "Transactions  for account...
# Suffix: "Transactions Total"
df = pd.read_csv(args.schwab_csv,
                 skiprows=1,
                 skipfooter=1,
                 engine='python')

# Convert dates to datetime objects
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Rename column names
column_new_names = {
    'Action': 'Note',
    'Symbol': 'Ticker Symbol',
    'Description': 'Security Name',
    'Quantity': 'Shares',
    'Fees & Comm': 'Fees',
    'Amount': 'Value',
}
df.rename(columns=column_new_names, inplace=True)


# Remove US dollar sign from Value column
def remove_currency(text: str):
    import re
    import locale
    decimal_point_char = locale.localeconv()['decimal_point']
    clean = re.sub(r'[^0-9'+decimal_point_char+'-'+r']+', '', text)
    return clean


new_value = df['Value'].apply(remove_currency)
df['Value'] = new_value

# Add a new column with all USD: Transaction Currency
transaction_currency = ["USD" for x in df['Value']]
df['Transaction Currency'] = transaction_currency

# Convert Action to Type
action_to_type = {
    'NRA Tax Adj': 'Taxes',
    'Credit Interest': 'Interest',
    'NRA Withholding': 'Taxes',
    'Short Term Cap Gain': 'Dividend',
    'Long Term Cap Gain': 'Dividend',
    'Cash Dividend': 'Dividend',
    'Buy': 'Buy',
    'Sell': 'Sell',
    'Wire Received': 'Deposit',
}
new_type = [action_to_type[x] for x in df['Note']]
df['Type'] = new_type

# Delete Price column
df.drop(columns=['Price'], inplace=True)

# Add SCHWAB1 INT to Notes
for k, v in df['Security Name'].items():
    if v.startswith('SCHWAB1 INT'):
        df.at[k, 'Note'] = df.at[k, 'Note'] + ' ' + v


# Remove non-security names
def convert_security_name(data: str):
    if data.startswith('SCHWAB1 INT'):
        return ''
    elif data.startswith('WIRED FUNDS RECEIVED'):
        return ''
    else:
        return data


new_security_name = [convert_security_name(v) for v in df['Security Name']]
df['Security Name'] = new_security_name

# Write to CSV file
df.to_csv(args.pp_csv, index=False, date_format='%Y%m%d')
print(args.pp_csv)
