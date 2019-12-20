#!/usr/bin/python3
import requests
import json
from pprint import pprint
import csv
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
        marketURL = i['url']
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

def buildCSV(data):
    bets = []
    for i in data:
        header = i["MarketHeader"]
        name = header[0]
        name = name[35::]
        name = name.rsplit("post")[0]
        name = name.strip()
        b1 = i["B1"][1:5]
        b2 = i["B2"][1:5]
        b3 = i["B3"][1:5]
        b4 = i["B4"][1:5]
        b5 = i["B5"][1:5]
        b6 = i["B6"][1:5]
        for item in b1:
                row = name+","+"b1,"+item+"\n"
                with open('bracketinfo.txt', "a") as pilog:
                    pilog.write(row)
                print(row)
        for item in b2:
                row = name+","+"b2,"+item+"\n"
                with open('bracketinfo.txt', "a") as pilog:
                    pilog.write(row)
                print(row)
        for item in b3:
                row = name+","+"b3,"+item+"\n"
                with open('bracketinfo.txt', "a") as pilog:
                    pilog.write(row)
                print(row)
        for item in b4:
                row = name+","+"b4,"+item+"\n"
                with open('bracketinfo.txt', "a") as pilog:
                    pilog.write(row)
                print(row)
        for item in b5:
                row = name+","+"b5,"+item+"\n"
                with open('bracketinfo.txt', "a") as pilog:
                    pilog.write(row)
                print(row)
        for item in b6:
                row = name+","+"b6,"+item+"\n"
                with open('bracketinfo.txt', "a") as pilog:
                    pilog.write(row)
                print(row)

def main():
    data = createDataFrame()
    b1 = buildCSV(data)

if __name__ == "__main__":
    count = 0
    while True:
        count = count + 1
        main()
        print()
        print(str(count))
        time.sleep(60)
