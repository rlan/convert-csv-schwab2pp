# A Charles Schwab CSV Converter for Portfolio Performance

[![Python CI](https://github.com/rlan/convert-csv-schwab2pp/actions/workflows/python-app.yml/badge.svg)](https://github.com/rlan/convert-csv-schwab2pp/actions)
![Last commit date](https://img.shields.io/github/last-commit/rlan/convert-csv-schwab2pp)
![Eclipse Public License - v 2.0](https://img.shields.io/github/license/rlan/convert-csv-schwab2pp)

Converts a [Charles Schwab](https://www.schwab.com/) transaction CSV file to a ready-to-import CSV file for [Portfolio Performance](https://www.portfolio-performance.info/en/) (PP).

After conversion, this [step-by-step guide](./guide/README.md) creates a new portfolio file in PP and imports the converted example CSV.

## Usage

There are two ways to run this tool: [Google Colab](https://colab.research.google.com/) or via command-line. The former is for end-users. The later is for python-savvy users and developers.

### Usage via Google Colab

Although Google Colab is free, one will need a [Google account](https://www.google.com/account/about/).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rlan/convert-csv-schwab2pp/blob/main/convert-csv-schwab2pp.ipynb)

### Usage via command-line

Runtime Requirements:

* Python 3.7, 3.8, 3.9 or 3.10[^1]
* Pandas

Install this tool in a Python virtual environment:

1. [pyenv](https://github.com/pyenv/pyenv)
2. [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

Install runtime libraries:

```sh
pip install -r requirements.txt
```

Command-line options:

```sh
python convert.py --help
```

```
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

Example:

An example Schwab CSV: [example.csv](example.csv).
The converted ready-to-import CSV file: [example_out.csv](example_out.csv).

To replicate this conversion:

```sh
python convert.py example.csv -p example_out.csv
```

## Details

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

Not-yet-supported transactions:

* ACH deposit and withdrawal
* Wire withdrawal

I have actual transactions for the supported transactions. "Sell" is an educated guess; I don't have an actual sale. If you could share actual transactions for not-yet-supported ones, please let me know. Thank you.

Duplicate transactions:

As far as I can test, PP will detect and skip duplicate transactions. So it is safe to import overlapping transactions in the future.

## License

MIT

[^1]: Python 3.11 not yet officially supported by Pandas, as of 2022-11-15.
