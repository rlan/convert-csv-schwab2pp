# A Charles Schwab CSV Converter for Portfolio Performance

Converts a [Charles Schwab](https://www.schwab.com/) transaction CSV file to a ready-to-import CSV file for [Portfolio Performance](https://www.portfolio-performance.info/en/) (PP).

[ ![workflow badge](https://github.com/rlan/convert-csv-schwab2pp/actions/workflows/python-app.yml/badge.svg) ](https://github.com/rlan/convert-csv-schwab2pp/actions)

Usage:

```sh
python convert.py --help
usage: convert.py [-h] [-p PP_CSV] schwab_csv

Converts a Charles Schwab transaction CSV file to a ready-to-import CSV file for Portfolio
Performance.

positional arguments:
  schwab_csv            Input Charles Schwab CSV file

optional arguments:
  -h, --help            show this help message and exit
  -p PP_CSV, --pp_csv PP_CSV
                        Resulting CSV file for Portfolio Performance (default: pp.csv)
```

Runtime Requirements:

* Python 3
* Pandas

Install runtime libraries:

```sh
pip install -r requirements.txt
```

Example:

There is an example Schwab CSV included: [example.csv](example.csv).
The converted ready-to-import CSV file: [example_out.csv](example_out.csv).

To replicate this conversion:

```sh
python3 convert.py example.csv -p example_out.csv
```

Here is a complete [step-by-step guide](./guide/README.md) for creating a new portfolio file in PP and importing the converted example CSV. As far as I can test, PP will detect and skip duplicate transactions. So it is safe to import overlapping transactions in the future.

Supported transactions:

* "NRA Tax Adj"
* "Credit Interest"
* "NRA Withholding"
* "Short Term Cap Gain"
* "Long Term Cap Gain"
* "Cash Dividend"
* "Buy"
* "Wire Received"
* "Sell" (Not verified)

I have actual transactions for only above types of transactions. "Sell" is an educated guess; I don't have an actual sale.

License:

Eclipse Public License - v 2.0
