#!/usr/bin/python3
import requests
import json
import time
import sqlite3
from datetime import datetime

print("Starting Script...")

def sanityCheck(*argv):
    '''
    None values are converted to 0.00
    '''

    for arg in argv:
        if arg == None:
            arg = 0.00
        else:
            arg = arg
        return arg

def currency(*argv):
    '''
    All values converted to currency.
    '''

    for arg in argv:
        currency = "${:,.2f}".format(arg) 
        return currency

def ping():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    count = 0
    '''
    Fetches twitter data markets from predictit API and adds it to a sqlite database.
    '''
    # create variable database in order to use this function with another market. Polls, maybe?

    page = requests.get('http://www.predictit.org/api/marketdata/all')
    print("PredictIt API:", page)
    print("Current Time: ", current_time)
    pidata = json.loads(page.text)
    markets = pidata['markets']
    for i in markets:
        marketName = i['name']
        shortMarketName = i['shortName']
        shortMarketName = shortMarketName.rsplit(" ")[0][1::]
        origin_url = i['url']
        url = origin_url.rsplit("detail")[1]
        url_prefix = origin_url.rsplit("detail")[0]
        marketID = i['id']
        contracts = i['contracts']
        timeStamp = i['timeStamp']
        status = i['status']

        if (marketName.find('tweets') != -1):
            conn = sqlite3.connect('pidb.db')
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS tweets (bracket TEXT, timeStamp TEXT, marketName TEXT, contractName TEXT, buyYes TEXT, \
             buyNo TEXT, sellYes TEXT, sellNo TEXT, url TEXT)")
            for i in contracts:
                
                # This bit generates the bracket number. 
                # I would create a generator function for this but Python globals are annoying.
                # Brackets are numbed 1-9. So the count should never be higher than 9.
                count = count + 1
                if count > 9:
                    count = 1

                bracket = "B" + str(count)
                contractID = i['id']
                dateEnd = i['dateEnd']
                image = i['image']
                contractName = i['name']
                shortContractName = i['shortName']
                status = i['status']
                lastTradePrice = i['lastTradePrice']
                buyYes = i['bestBuyYesCost']
                buyNo = i['bestBuyNoCost']
                sellYes = i['bestSellYesCost']
                sellNo = i['bestSellNoCost']
                lastClosePrice = i['lastClosePrice']
                # DisplayOrder is absolutely worthless, contrary to the name it does not display anything in order.
                # I included in case the api is updated to make it not worthless.
                # This comment has more value than displayOrder.
                displayOrder = i['displayOrder']

                # Ensures that values are not None.
                # Then converts to currency.
                buyYes = currency(sanityCheck(buyYes))
                buyNo = currency(sanityCheck(buyNo))
                sellYes = currency(sanityCheck(sellYes))
                sellNo = currency(sanityCheck(sellNo))
                c.execute("INSERT INTO tweets (bracket, timeStamp, marketName, contractName, buyYes, buyNo, sellYes, \
                    sellNo, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (bracket, timeStamp, shortMarketName, contractName, buyYes, buyNo, sellYes, sellNo, url))

            conn.commit()
            c.close()
            conn.close()

if __name__ == "__main__":
    while True:
        ping()
        time.sleep(60)