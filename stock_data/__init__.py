from filter import StockFilterByPrice
from listing_obtainers import TSXObtainer
from listing_obtainers.NASDAQObtainer import NASDAQObtainer
from stock_data.CurrentStockDataObtainer import CurrentStockDataObtainer
from stock_data.StockDatabase import StockDatabase
import time

if __name__ == "__main__":
    tsx_obtainer = NASDAQObtainer(20)
    filter = StockFilterByPrice(10, CurrentStockDataObtainer())
    filter.addListings(tsx_obtainer)\
        .getPricesForListings()\
        .filterStocks()

    # Recommended for setSecondsBetweenStockUpdates: 60 (which is the default)
    database = StockDatabase.getInstance()
    database.setPricesToKeepTrackOf(7)\
            .setSecondsBetweenStockUpdates(30)\
            .useObtainer(CurrentStockDataObtainer())\
            .trackStocksInFilter(filter)\
            .startSelfUpdating()

    time.sleep(75)
    database.stopSelfUpdating()
    # print(database.getCurrentStock("AAB.TO"))

