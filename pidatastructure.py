#!/usr/bin/python3
import requests
import json
import time

def get_json():
    '''Calls json object from PredictIt to be parsed'''
    page = requests.get('https://www.predictit.org/api/marketdata/all/')
    all_markets = json.loads(page.text)
    markets = all_markets['markets']
    #pprint(markets)
    return markets

def createDataFrame():
    '''Generator to create a data structure for PredictIt.com twitter markets.
    This Data can be more easily parsed for data analysis.'''
    markets = get_json()
    for i in markets:
        brackets = {}
        count = 0
        marketName = i['name']
        marketID = i['id']
        contracts = i['contracts']
        timeStamp = i['timeStamp']

        if (marketName.find('tweets') != -1):
            for i in contracts:
                # Accumulator created to be appended to bracket name.
                count = count + 1

                betName = i['name']
                bracket = "B" + str(count)
                bracket_name = bracket
                bestBuyNo = i['bestBuyNoCost']
                bestBuyYes = i['bestBuyYesCost']
                bestSellNo = i['bestSellNoCost']
                bestSellYes = i['bestSellYesCost']

                # Creating an object to be yieled.
                bets = {"MarketHeader": [
                "Market Name: " + str(marketName),
                "Market ID: " + str(marketID),
                "Time: " + str(timeStamp)],

                # Brackets are labeled so that you know what the values belong to. Labeling follows the following pattern:
                # BN = Buy No
                # BY = Buy Yes
                # SN = Sell No
                # SY = Sell Yes
                bracket: [betName,
                "BN,"  + str(bestBuyNo),
                "BY,"  + str(bestBuyYes),
                "SN,"  + str(bestSellNo),
                "SY," + str(bestSellYes)]}

                brackets.update(bets)
            # Yields an object from the dictionary brackets{}. This is a new one to me!
            # Much faster than returning a list object, which was what I was doing before.
            yield brackets

def buildCSV():
    ''' Build a CSV which can be easily parsed to iterated upon for further analysis.'''

    # Much of this work may look duplicated, but creating a new function for the CSV
    # Allows the above data structure to be reused in the future, if needed.
    data = createDataFrame()
    bets = []
    for i in data:
        # Create a name based upon the market header object by string splitting, and then stripping white space.
        name = i["MarketHeader"][0][35::].rsplit("post")[0].strip()
        # Create tuple objects which can then be iterated over to write a csv.
        b1 = (name, "b1", i["B1"][1:5])
        b2 = (name, "b2", i["B2"][1:5])
        b3 = (name, "b3", i["B3"][1:5])
        b4 = (name, "b4", i["B4"][1:5])
        b5 = (name, "b5", i["B5"][1:5])
        b6 = (name, "b6", i["B6"][1:5])
        bets.extend((b1, b2, b3, b4, b5, b6))
    for i in bets:
        for item in i[2]:
            row = (i[0] + "," + i[1] + "," + item+"\n")
            print(row, end="")
            with open('bracketinfo.txt', "a") as pilog:
                pilog.write(row)

def main():
    buildCSV()

if __name__ == "__main__":
    count = 0
    while True:
        count = count + 1
        main()
        print("\n" + str(count))
        time.sleep(60)
