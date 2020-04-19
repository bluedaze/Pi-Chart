#!/usr/bin/python3
import requests
import json
import time
import sqlite3

print("Starting Script...")

def sanityCheck(*argv):
    '''
    This function exists to ensure that all None values are converted to 0.00
    '''

    for arg in argv:
        if arg == None:
            arg = 0.00
        else:
            arg = arg
        return arg

def currency(*argv):
    '''
    This function exists to convert all values to currency.
    '''

    for arg in argv:
        currency = "${:,.2f}".format(arg) 
        return currency

def main():
    '''
    Fetches twitter data markets from predictit API and adds it to a sqlite database.
    '''

    page = requests.get('http://www.predictit.org/api/marketdata/all')
    print(page)
    pidata = json.loads(page.text)
    markets = pidata['markets']
    for i in markets:
        marketName = i['name']
        shortMarketName = i['shortName']
        shortMarketName = shortMarketName.rsplit(" ")[0]
        origin_url = i['url']
        url = origin_url.rsplit("detail")[1]
        url_prefix = origin_url.rsplit("detail")[0]
        marketID = i['id']
        contracts = i['contracts']
        timeStamp = i['timeStamp']
        timeStamp = timeStamp[11:16]
        status = i['status']
        print(timeStamp)


        if (marketName.find('tweets') != -1):
            conn = sqlite3.connect('testcase1.db')
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(\"Market Name\" TEXT, \"Contract Name\" TEXT, \"Buy Yes\" TEXT, \
             \"Buy No\" TEXT, \"Sell Yes\" TEXT, \"Sell No\" TEXT, \"CurrentTime Stamp\" TEXT, url TEXT)")
            for i in contracts:
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
                # I included in case the api is updated to make it not worthless. This comment has more value than displayOrder.
                displayOrder = i['displayOrder']

                #Ensures that values are not None.
                #Then converts to currency.
                buyYes = currency(sanityCheck(buyYes))
                buyNo = currency(sanityCheck(buyNo))
                sellYes = currency(sanityCheck(sellYes))
                sellNo = currency(sanityCheck(sellNo))

                c.execute("INSERT INTO stuffToPlot (\"Market Name\", \"Contract Name\", \"Buy Yes\", \"Buy No\", \"Sell Yes\", \
                    \"Sell No\", \"CurrentTime Stamp\", url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (shortMarketName, contractName, buyYes, buyNo, sellYes, sellNo, timeStamp, url))
                print(marketName+":", contractName, buyYes, buyNo, sellYes, sellNo, timeStamp, url)

            conn.commit()
            c.close()
            conn.close()

if __name__ == "__main__":
    main()
