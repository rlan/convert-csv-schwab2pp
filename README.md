# A Charles Schwab CSV Converter for Portfolio Performance

Converts a [Charles Schwab](https://www.schwab.com/) transaction CSV file to a ready-to-import CSV file for [Portfolio Performance](https://www.portfolio-performance.info/en/) (PP).

[![workflow badge](https://github.com/rlan/convert-csv-schwab2pp/actions/workflows/python-app.yml/badge.svg)](https://github.com/rlan/convert-csv-schwab2pp/actions)

## Usage

There are two ways to run this tool: Google Colab or via command-line. The former is for end-users. The later is for python-savvy users and developers.

### Usage via Google Colab

Although [Google Colab](https://colab.research.google.com/) is free, one will need a [Google account](https://www.google.com/account/about/).
More instructions are in this [link](https://colab.research.google.com/drive/1uyuqQmZA8tg8XlHsVV2IKsVq4B-SiSMo?usp=sharing).

### Usage via command-line

Runtime Requirements:

* Python 3.8, 3.9 or 3.10[^1]
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

## After conversion

Here is a complete [step-by-step guide](./guide/README.md) for creating a new portfolio file in PP and importing the converted example CSV.

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

I have actual transactions for only above types of transactions. "Sell" is an educated guess; I don't have an actual sale.

Duplicate transactions:

As far as I can test, PP will detect and skip duplicate transactions. So it is safe to import overlapping transactions in the future.

## License

Eclipse Public License - v 2.0

[^1]: Python 3.8, 3.9 and 3.10 are supported. Only these versions are officially supported by Pandas, as of 2022-11-15.
