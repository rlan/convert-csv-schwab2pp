# A Charles Schwab CSV Converter for Portfolio Performance

[![Testing badge](https://github.com/rlan/convert-csv-schwab2pp/actions/workflows/python-app.yml/badge.svg)](https://github.com/rlan/convert-csv-schwab2pp/actions)
![Python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![MIT license](https://img.shields.io/github/license/rlan/convert-csv-schwab2pp)

Converts a [Charles Schwab](https://www.schwab.com/) transaction CSV file to a ready-to-import CSV file for [Portfolio Performance](https://www.portfolio-performance.info/en/) (PP).

After conversion, this [step-by-step guide](./guide/README.md) creates a new portfolio file in PP and imports the converted example CSV.

<figure>
  <img
  src="https://github.com/rlan/convert-csv-schwab2pp/raw/main/guide/img/100.png"
  alt="Guide step 100">
  <figcaption>After importing the converted example CSV</figcaption>
</figure>

## Usage

There are two ways to run this tool: [Google Colab](https://colab.research.google.com/) or via command-line. The former is for end-users. The later is for python-savvy users and developers.

### Usage via Google Colab

Although Google Colab is free, one will need a [Google account](https://www.google.com/account/about/).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rlan/convert-csv-schwab2pp/blob/main/convert-csv-schwab2pp.ipynb)

### Usage via command-line

Runtime Requirements:

* Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12.
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

```txt
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
* "Wire Sent" (Thank you, @ipaulo)
* "Sell" (Not verified)

Not-yet-supported transactions:

* ACH deposit and withdrawal

I have actual transactions for the supported transactions. "Sell" is an educated guess; I don't have an actual sale. If you could share actual transactions for not-yet-supported ones, please let me know. Thank you.

Duplicate transactions:

As far as I can test, PP will detect and skip duplicate transactions. So it is safe to import overlapping transactions in the future.

## License

MIT
