# A Charles Schwab CSV Converter for Portfolio Performance

[![Testing badge](https://github.com/rlan/convert-csv-schwab2pp/actions/workflows/python-app.yml/badge.svg)](https://github.com/rlan/convert-csv-schwab2pp/actions)
![Python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![MIT license](https://img.shields.io/github/license/rlan/convert-csv-schwab2pp)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15024607.svg)](https://doi.org/10.5281/zenodo.15024607)

A command-line tool that converts a [Charles Schwab](https://www.schwab.com/) transaction CSV file to a ready-to-import CSV file for [Portfolio Performance](https://www.portfolio-performance.info/en/) (PP).

After conversion, this [step-by-step guide](./guide/README.md) creates a new portfolio file in PP and imports the converted example CSV.

<figure>
  <img
  src="https://github.com/rlan/convert-csv-schwab2pp/raw/main/guide/img/100.png"
  alt="Guide step 100">
  <figcaption>After importing the converted example CSV.</figcaption>
</figure>


## Installation

First, install [pipx](https://github.com/pypa/pipx) (not pip).

Then:

```sh
pipx install git+https://github.com/rlan/convert-csv-schwab2pp
```


### Try it out!

Let's see if installation was successful:

```sh
schwab2pp --help
```

```txt
usage: schwab2pp [-h] [-p PP_CSV] schwab_csv

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
schwab2pp example.csv -p example_out.csv
```


### Update to a new version

```sh
pipx upgrade schwab2pp
```


### Uninstallation

```sh
pipx uninstall schwab2pp
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
* "Wire Sent"[^1] (Thank you, [@ipaulo](https://github.com/ipaulo))
* "Sell" (Not verified)

Not-yet-supported transactions:

* ACH deposit and withdrawal

I have actual transactions for the supported transactions. "Sell" is an educated guess; I don't have an actual sale. If you could share actual transactions for not-yet-supported ones, please let me know. Thank you.

Duplicate transactions:

As far as I can test, PP will detect and skip duplicate transactions. So it is safe to import overlapping transactions in the future.

Dates:

If date is in "date1 as of date2" format, "date1" will be used and "as of date2" will be appended to the resulting "Note" column.


## Citation

If this project helps your research, don't hesitate to spread the word! Click on the badge below and find citation formats (e.g., BibTeX and etc) at the bottom of that page.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15024607.svg)](https://doi.org/10.5281/zenodo.15024607)


## License

[MIT](LICENSE)


[^1]: https://github.com/rlan/convert-csv-schwab2pp/issues/2
