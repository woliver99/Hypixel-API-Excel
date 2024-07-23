import requests
import json
import file_utils

auctionCacheFile = "auction_cache.json"
bazaarCacheFile = "bazaar_cache.json"

def fetchAuctionPage(page: int):
    url = "https://api.hypixel.net/v2/skyblock/auctions"

    params = {
        "page": page
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        page_data = response.json()
        total_pages = int(page_data["totalPages"]) - 1
        print(f"Successfully fetched page {page}/{total_pages} of the auction house.")
        return page_data
    else:
        raise Exception(f"Failed to fetch page {page} of the auction house. Status code: {response.status_code}, response: {response.text}")
    

def fetchAllAuctionPages(useCache: bool = True):
    if useCache:
        try:
            with open(auctionCacheFile, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Cache file not found, fetching all auction pages.")

    page = 0
    total_pages = 0
    all_auctions = []
    while page <= total_pages:
        auctions = fetchAuctionPage(page)
        total_pages = int(auctions["totalPages"]) - 1
        all_auctions += auctions["auctions"]
        page += 1
    print("Writing auction pages to cache.")
    file_utils.writeJsonToFile(all_auctions, auctionCacheFile)
    return all_auctions

def fetchLowestBin(items: set[str]) -> dict[str, int]:
    prices = {}
    auctions = fetchAllAuctionPages(True)

    for item in auctions:
        if item["item_name"] in items:
            if item["bin"] == False:
                continue

            if item["item_name"] not in prices:
                prices[item["item_name"]] = item["starting_bid"]
            else:
                prices[item["item_name"]] = min(prices[item["item_name"]], item["starting_bid"])

    return prices

def fetchBazaarData(useCache: bool = True):
    if useCache:
        try:
            with open(bazaarCacheFile, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Cache file not found, fetching bazaar data.")
    
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)

    if response.status_code == 200:
        bazaar_data = response.json()
        print("Writing bazaar data to cache.")
        file_utils.writeJsonToFile(bazaar_data, bazaarCacheFile)
        return bazaar_data
    else:
        raise Exception(f"Failed to fetch bazaar data. Status code: {response.status_code}, response: {response.text}")
    
def fetchBazaarSellPrices(items: set[str]) -> dict[int]:
    bazaar_data = fetchBazaarData(True)
    sell_prices = {}

    for item in items:
        if item in bazaar_data["products"]:
            sell_prices[item] = round(float(bazaar_data["products"][item]["quick_status"]["sellPrice"]))

    return sell_prices