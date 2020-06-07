#!/usr/bin/python3
import requests
import json
import time
import sqlite3
from datetime import datetime
from pisql import insert_data, create_database
num = 0
print("\n\n----------------------\
\nRestarting Script...\n\
----------------------\n\n")


def sanityCheck(*args):
    '''
    None values are converted to 0.00
    '''

    for arg in args:
        if arg == None:
            arg = 0.00
        else:
            arg = arg
        return arg

def currency(*args):
    '''
    All values converted to currency.
    '''

    for arg in args:
        currency = "${:,.2f}".format(arg) 
        return currency

def ping():
    '''
    Fetches twitter data markets from predictit API and adds it to a sqlite database.
    '''
    # create variable database in order to use this function with another market. Polls, maybe?

    page = requests.get('http://www.predictit.org/api/marketdata/all')
    pidata = json.loads(page.text)
    markets = pidata['markets']
    for i in markets:
        marketName = i['name']
        shortName = i['shortName']
        url = i['url'].rsplit("detail")[1]
        contracts = i['contracts']
        timeStamp = i['timeStamp']

        if (marketName.find('538') != -1 or marketName.find('RCP') != -1):
            pi_api_query(shortName, timeStamp, url, contracts)


def pi_api_query(marketName, timeStamp, url, contracts):

    count = 0
    create_database()

    for i in contracts:
        
        # This bit generates the bracket number. 
        count = count + 1
        bracket = "B" + str(count)
        
        contractName = i['name']
        buyYes = i['bestBuyYesCost']
        buyNo = i['bestBuyNoCost']
        sellYes = i['bestSellYesCost']
        sellNo = i['bestSellNoCost']

        # Ensures that values are not None.
        # Then converts to currency.
        buyYes = currency(sanityCheck(buyYes))
        buyNo = currency(sanityCheck(buyNo))
        sellYes = currency(sanityCheck(sellYes))
        sellNo = currency(sanityCheck(sellNo))

        try:
            insert_data(bracket, timeStamp, marketName, contractName, buyYes, buyNo, sellYes, sellNo, url)
        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    while True:
        ping()
        print("committed")
        time.sleep(59)