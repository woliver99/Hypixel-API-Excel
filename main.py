import hypixel_api
import excel_utils

fetch_latest_auction = input("Do you want to fetch the latest auction data? This may take a while. Type 'yes' to continue: ")
fetch_latest_bazaar = input("Do you want to fetch the latest bazaar data? Type 'yes' to continue: ")

if fetch_latest_auction.lower() == "yes":
    hypixel_api.fetchAllAuctionPages(False)

if fetch_latest_bazaar.lower() == "yes":
    hypixel_api.fetchBazaarData(False)

print("Updating auction house prices.")
auctionItemsToUpdate = excel_utils.getItemNames("Auction")
prices = hypixel_api.fetchLowestBin(auctionItemsToUpdate)
excel_utils.updateItemPrices("Auction", prices)

print("Updating bazaar prices.")
bazaarItemsToUpdate = excel_utils.getItemNames("Bazaar")
bazaarPrices = hypixel_api.fetchBazaarSellPrices(bazaarItemsToUpdate)
excel_utils.updateItemPrices("Bazaar", bazaarPrices)