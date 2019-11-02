# First step in creating a predictit database which tracks prices of markets for you.
# TODO:
# Add database
# Notifications based on price fluctionations.
# Allow user to input url. Extract page id, and then run script against this URL.

import requests
from bs4 import BeautifulSoup
import json


##user_page = input("Which market would you like to see? Please provide a URL: ")


page = requests.get('https://www.predictit.org/api/marketdata/markets/3698')
market = json.loads(page.text)
contracts = market['contracts']
count = 0
for item in contracts:
    name = item['name']
    buyno = item['bestBuyNoCost']
    buyyes = item['bestBuyNoCost']
    if buyyes and buyno == None:
        print("")
    if buyno == None:
        buyno = "0.00"        
    if buyyes == None:
        buyyes = "0.00"
    else:
        count = count + 1
        print(str(count),": ", name,"\n", "No: ", buyno, " Yes: ", buyyes, sep="")


# Example of how to get information from a json object for my future reference.
        
##print(market['contracts'][0]['name'])
##print("No:", market['contracts'][0]['bestBuyNoCost'])
##print("Yes:", market['contracts'][0]['bestBuyYesCost'])
##print()
##print(market['contracts'][1]['name'])
##print("No:", market['contracts'][1]['bestBuyNoCost'])
##print("Yes:", market['contracts'][1]['bestBuyYesCost'])
