import requests
import json
from pprint import pprint

page = requests.get('https://www.predictit.org/api/marketdata/all/')
all_markets = json.loads(page.text)
markets = all_markets['markets']
#pprint(markets)
for i in markets:
    marketName = i['name']
    marketID = i['id']
    marketURL = i['url']
    contracts = i['contracts']
    if (marketName.find('tweets') != -1):
        #pprint(contracts)
        print("Market ID:", marketID)
        print(marketName)
        print(marketURL)
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
            print("Buy no:", bestBuyNo)
            print("Buy yes:", bestBuyYes)
            print("Sell no:", bestSellNo)
            print("Sell yes:", bestSellYes)
        print()
