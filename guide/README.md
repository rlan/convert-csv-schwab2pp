# A step-by-step guide

This guide will create a new portfolio file in Portfolio Performance (PP) and import a converted CSV file. Screen capturse are from PP 0.71.2 (October 2024).

1. Download a transcations CSV file from your Charles Schwab account, say, ```example.csv```.
2. Convert the CSV. [README](../README.md) for convert.py.

```sh
python3 convert.py example.csv -p example_out.csv
```

3. Open Portfolio Performance and click on "Create a new file".

![Create a new file](img/010.png "Click on Create a new file")

4. Select "USD (United States Dollar)" for currency.

![USD (United States Dollar)](img/020.png "Select 'USD (United States Dollar)' for currency.")

5. Type "Securities" for Securities Account and "Deposit" for Reference Account. Then click on "Add" button.

![Securities and Deposit accounts](img/030.png)

6. Click on "Finish" button.

![Clikd on Finish](img/040.png)

7. Import the converted CSV. Go to File menu, Import, CSV files (comma-seperated values) and select ```example_out.csv```.

![File menu, Import, CSV files](img/050.png)

8. Click on "Next" button.

![Click on "Next" button](img/060.png)

9. Note that "Deposit" is chosen as the Cash Account and "Securities" as the Securities Account. These two names where entered in a previous step. Click on "Finish" button.

![Click on "Finish" button](img/070.png)

10.  Click on "OK" button.

![Click on "OK" button](img/080.png)

11. Now we are going to retrieve historial quotes for securities that exist in the account.

    1. Select "All Securities" from the tree menu on the left panel.

    ![Select "All Securities"](img/090.png)

    2. Right click on "VANGUARD TOTAL INTERNATIONAL BND ETF" and choose "Edit".

    ![Right click and choose Edit](img/091.png)

    3. Select "Historical Quotes" tab.

    ![Select Historical Quotes tab](img/092.png)

    4. Choose "Yahoo" from the Provider dropdown list.

    ![Choose Yahoo from the Provider dropdown list](img/093.png)

    5. Historical quotes will be retrieved. Then click on "OK" button.

    ![Historical quotes retrieved](img/094.png)
    ![Chart of historical quotes](img/095.png)

    6. Repeat this for other securities in the account. Note that this only needs to be done once for each new securities in the account. For example, repeat this when a new security is purchased. PP will retrieve historical quotes automatically or you can manually do so via Online menu, Update Quotes.

12. Verify. Select "All transcations" from the tree menu on the left panel. Import complete.

![Select All transactions](img/100.png)
