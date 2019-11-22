import requests
import json
from pprint import pprint


class predictitCall():
    dataFrame = []
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
            marketHeader = {}
            marketHeader[str(marketID)] = [str(marketName), str(marketURL)]
            brackets = {}
            for i in contracts:
                betName = i['name']
                bestBuyNo = i['bestBuyNoCost']
                bestBuyYes = i['bestBuyYesCost']
                bestSellNo = i['bestSellNoCost']
                bestSellYes = i['bestSellYesCost']
                #print("\n" + "-------" + "\n" + betName + "\n" + "-------")
                bets = {betName:
                ["Buy no: "  + str(bestBuyNo),
                "Buy yes: "  + str(bestBuyYes),
                "Sell no: "  + str(bestSellNo),
                "Sell yes: " + str(bestSellYes)]}
                brackets.update(bets)
                #data.append(bets)
                # print("Buy no:", bestBuyNo)
                # print("Buy yes:", bestBuyYes)
                # print("Sell no:", bestSellNo)
                # print("Sell yes:", bestSellYes)
            #markets.update(brackets)
            # markets = {marketHeader: brackets}
            uid = (str(marketID) + ": " + str(marketName))
            verticles = {uid: brackets}
            dataFrame.append(verticles)

    for i in dataFrame:
        print(i, "\n")
