#!/usr/bin/python
# First step in creating a predictit database which tracks prices of markets for you.
# TODO:
# Add database
# Track notable changes per contract.
# Notifications based on price fluctionations.
# Allow user to input url. Extract page id, and then run script against this URL.

import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

m1 = requests.get('https://www.predictit.org/api/marketdata/markets/6117')
market = json.loads(m1.text)
m1name = market['name']
whitehouse = market['contracts']

m2 = requests.get('https://www.predictit.org/api/marketdata/markets/6105')
market = json.loads(m2.text)
m2name = market['name']
vp = market['contracts']

m3 = requests.get('https://www.predictit.org/api/marketdata/markets/6106')
market = json.loads(m3.text)
m3name = market['name']
potus = market['contracts']

m4 = requests.get('https://www.predictit.org/api/marketdata/markets/6109')
market = json.loads(m4.text)
m4name = market['name']
aoc = market['contracts']

m5 = requests.get('https://www.predictit.org/api/marketdata/markets/6110')
market = json.loads(m5.text)
m5name = market['name']
yang = market['contracts']

m6 = requests.get('https://www.predictit.org/api/marketdata/markets/6114')
market = json.loads(m6.text)
m6name = market['name']
rdt = market['contracts']


def brackets(page, market, marketName):
    ##pprint(contracts)
    print()
    print(marketName.center(80))
    print()
    count = 0
    market_list = []
    for item in market:
        name = item['name']
        buyno = item['bestBuyNoCost']
        buyyes = item['bestBuyYesCost']
        if buyno == None:
            buyno = "N/A"
        if buyyes == None:
            buyyes = "N/A"
        market = str(name) + "\nNo: " + str(buyno) + " Yes: " + str(buyyes)
        market_list.append(market)
        market_list.sort()
    print()
    for i in market_list:
        count = count + 1
        print("B" + str(count) + ":" + i)
    print()

keep_going="y"
while (keep_going=="y"):
    print("  1. White House")
    print("  2. VP")
    print("  3. Potus")
    print("  4. AOC")
    print("  5. Yang")
    print("  6. RDT")
    print("  7. All")
    print("  Q. QUIT")
    choice = input("\nPlease enter your choice: ")
    if choice == "1":
        brackets(m1, whitehouse, m1name)
    elif choice == "2":
        brackets(m2, vp, m2name)
    elif choice == "3":
        brackets(m3, potus, m3name)
    elif choice == "4":
        brackets(m4, aoc, m4name)
    elif choice == "5":
        brackets(m5, yang, m5name)
    elif choice == "6":
        brackets(m6, rdt, m6name)
    elif choice == "7":
        brackets(m1, whitehouse, m1name)
        brackets(m2, vp, m2name)
        brackets(m3, potus, m3name)
        brackets(m4, aoc, m4name)
        brackets(m5, yang, m5name)
        brackets(m6, rdt, m6name)       
    elif choice == "Q":
        print("Choice was 2.  Exiting program")
        keep_going = "n"

    else:
        print("Choice was not valid.  Please choose a valid option.")
        input("Press any key to continue.")



##brackets(m1, whitehouse)
# Example of how to get information from a json object for my future reference.
        
##print(market['contracts'][0]['name'])
##print("No:", market['contracts'][0]['bestBuyNoCost'])
##print("Yes:", market['contracts'][0]['bestBuyYesCost'])
##print()
##print(market['contracts'][1]['name'])
##print("No:", market['contracts'][1]['bestBuyNoCost'])
##print("Yes:", market['contracts'][1]['bestBuyYesCost'])
