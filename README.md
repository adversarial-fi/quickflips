![pepe](https://github.com/adversarial-fi/quickflips/assets/168155085/de008f96-f1e2-418d-8730-3e490a04c4fd)
# Quick Flips: Motion tracker for Base addresses.

Does that wallet have motion or are they a brokie? Now you can know by making sense of blockchain data.

### How does it work

It analyzes a single-column spreadsheet with Base (On Ethereum) addresses and offers the following information for the most consistent traders based on data of the past 31 days:

1. Average trade volume.
2. Total trades over the period.
3. Most profitable trade with a BaseScan txid link.
4. Address trade history with a Zerion history link.

### Are your wallets winners?

Quickflips only shows you the top 5 most motion having addresses. Meaning, most trades made and largest cashout per address.

### Coming soon (Maybe)

- Average profit and loss per address.
- Other stuff found interesting.

### How to install and use

You need Python 3, a terminal, and the following `pip` modules:

1. `termcolor`
2. `requests`
3. `pandas`

You also need a [BaseScan account](https://basescan.org/register) to get an API, and a [CryptoCompare](https://www.cryptocompare.com/) account for the same purpose. Both offer free APIs.

Once you get them, swap out the placeholder values in the Python script for your keys and run it on the terminal.

You'll be asked for a single-column `.csv`  file with Base addresses, one address per row. Input the path and it will output the information on your screen and also as an export `.csv` file with more details.

### Last updated

April 25th, 2024, Q2
