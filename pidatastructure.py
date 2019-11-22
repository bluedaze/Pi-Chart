import requests
import json
from pprint import pprint


class predictitCall():
    dataFrame = []
    page = requests.get('https://www.predictit.org/api/marketdata/all/')
    all_markets = json.loads(page.text)
    markets = all_markets['markets']
    for i in markets:
        marketName = i['name']
        marketID = i['id']
        marketURL = i['url']
        contracts = i['contracts']
        if (marketName.find('tweets') != -1):
            brackets = {}
            for i in contracts:
                betName = i['name']
                bestBuyNo = i['bestBuyNoCost']
                bestBuyYes = i['bestBuyYesCost']
                bestSellNo = i['bestSellNoCost']
                bestSellYes = i['bestSellYesCost']
                bets = {betName:
                ["Buy no: "  + str(bestBuyNo),
                "Buy yes: "  + str(bestBuyYes),
                "Sell no: "  + str(bestSellNo),
                "Sell yes: " + str(bestSellYes)]}
                brackets.update(bets)
            uid = (str(marketID) + ": " + str(marketName))
            verticles = {uid: brackets}
            dataFrame.append(verticles)

    for i in dataFrame:
        print(i, "\n")
