#!/usr/bin/python3
import requests
import json
from pprint import pprint

def get_json():
    '''Calls json object from PredictIt to be parsed'''
    page = requests.get('https://www.predictit.org/api/marketdata/all/')
    all_markets = json.loads(page.text)
    markets = all_markets['markets']
    #pprint(markets)
    return markets

def CreateDataFrame():
    '''Generator to create a data structure for PredictIt.com twitter markets.
    This Data can be more easily parsed for data analysis.'''
    markets = get_json()
    for i in markets:
        marketName = i['name']
        marketID = i['id']
        marketURL = i['url']
        contracts = i['contracts']
        timeStamp = i['timeStamp']
        if (marketName.find('tweets') != -1):
            #pprint(i)
            brackets = {}
            count = 0
            for i in contracts:
                count = count + 1
                betName = i['name']
                betName = "B" + str(count) + ": " + betName
                bestBuyNo = i['bestBuyNoCost']
                bestBuyYes = i['bestBuyYesCost']
                bestSellNo = i['bestSellNoCost']
                bestSellYes = i['bestSellYesCost']
                bets = {"MarketHeader": [
                "Market Name: " + str(marketName),
                "Market ID: " + str(marketID),
                "Time: " + str(timeStamp)],

                betName:
                ["Buy-no: "  + str(bestBuyNo),
                "Buy-yes: "  + str(bestBuyYes),
                "Sell-no: "  + str(bestSellNo),
                "Sell-yes: " + str(bestSellYes)]}
                brackets.update(bets)
            yield brackets


if __name__ == "__main__":
    data = CreateDataFrame()
    for i in data:
        print(i)
        print()
