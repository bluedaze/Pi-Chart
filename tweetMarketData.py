#!/usr/bin/python3
import time
import requests
import json
from pprint import pprint

count = 0
while True:
    count = count + 1
    page = requests.get('https://www.predictit.org/api/marketdata/all/')
    all_markets = json.loads(page.text)
    markets = all_markets['markets']
    #pprint(markets)
    for i in markets:
        marketName = i['name']
        timeStamp = i['timeStamp']
        marketID = i['id']
        marketURL = i['url']
        marketURL = "See further details here: " + marketURL
        contracts = i['contracts']
        if (marketName.find('tweets') != -1):
            #pprint(contracts)
            print("\n\n")
            divider = "[~~~~~~~~~~~~~~~~~~~~~~~~~~~]"
            print(divider.center(120))
            header = "Market ID: " + str(marketID)
            print(header.center(120))
            print()
            print(marketName.center(120))
            for i in contracts:
                betName = i['name']
                bestBuyNo = i['bestBuyNoCost']
                bestBuyYes = i['bestBuyYesCost']
                bestSellNo = i['bestSellNoCost']
                bestSellYes = i['bestSellYesCost']
                print()
                print("-------")
                print(betName)
                print("-------")

                if bestBuyNo == None:
                    print("Buy no: N/A")
                else:
                    print("Buy no:", bestBuyNo)

                if bestBuyYes == None:
                    print("Buy yes: N/A")
                else:
                    print("Buy yes:", bestBuyYes)

                if bestSellNo == None:
                    print("Sell no: N/A")
                else:
                    print("Sell no:", bestSellNo)

                if bestSellYes == None:
                    print("Sell yes: N/A")
                else:
                    print("Sell yes:", bestSellYes)
            print("\n")
            print(marketURL.center(100))
            print()
    print("Iteration:", count, "\n")
    print(timeStamp)
    time.sleep(60)
