#!/usr/bin/python3
import requests
import json
import time
import sqlite3

def get_json():
    '''Calls json object from PredictIt to be parsed'''
    page = requests.get('https://www.predictit.org/api/marketdata/all/')
    all_markets = json.loads(page.text)
    markets = all_markets['markets']
    return markets

def parse_json():
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
                bracket_name = "B" + str(count)
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
                bracket_name: [betName,
                "BN"  + str(bestBuyNo),
                "BY"  + str(bestBuyYes),
                "SN"  + str(bestSellNo),
                "SY" + str(bestSellYes)]}

                brackets.update(bets)
            # Yields an object from the dictionary brackets{}. This is a new one to me!
            # Much faster than returning a list object, which was what I was doing before.
            yield brackets

def data_frame():
    ''' Build a CSV which can be easily parsed to iterated upon for further analysis.'''

    # Much of this work may look duplicated, but creating a new function for the CSV
    # Allows the above data structure to be reused in the future, if needed.
    data = parse_json()
    bets = []
    for i in data:
        time = i["MarketHeader"][2][17:25]
        date= i["MarketHeader"][2][6:16]
        name = i["MarketHeader"][0][35::].rsplit("post")[0].strip()
        # Create tuple objects which can then be iterated over to write a csv.
        # Create a name based upon the market header object by string splitting, and then stripping white space.
        b1 = (name, "b1", i["B1"][1:5], time, date)
        b2 = (name, "b2", i["B2"][1:5], time, date)
        b3 = (name, "b3", i["B3"][1:5], time, date)
        b4 = (name, "b4", i["B4"][1:5], time, date)
        b5 = (name, "b5", i["B5"][1:5], time, date)
        b6 = (name, "b6", i["B6"][1:5], time, date)
        b7 = (name, "b7", i["B7"][1:5], time, date)
        b8 = (name, "b8", i["B8"][1:5], time, date)
        b9 = (name, "b9", i["B9"][1:5], time, date)
        bets.extend((b1, b2, b3, b4, b5, b6, b7, b8, b9))

    yield bets

def data_entry():
    conn = sqlite3.connect('testcase1.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(name TEXT, bracket TEXT, bet_name TEXT, bet_value REAL, tstamp, dstamp)")
    betGenerator = data_frame()
    for listyield in betGenerator:
        for i in listyield:
            for bet in i[2]:
                name = i[0]
                bracket = i[1]
                bet_name = bet[0:2]
                if bet[2::] == "None":
                    bet_value = 0.00
                else:
                    bet_value = bet[2::]
                #bet_value = bet[2::]
                time = i[3]
                date = i[4]
                c.execute("INSERT INTO stuffToPlot (name, bracket, bet_name, bet_value, tstamp, dstamp) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, bracket, bet_name, bet_value, time, date))
                print(name, bracket, bet_name, bet_value, time, date)
    conn.commit()
    c.close()
    conn.close()

def main():
    data_entry()

if __name__ == "__main__":
    count = 0
    while True:
        count = count + 1
        main()
        print("\n" + str(count))
        time.sleep(60)
