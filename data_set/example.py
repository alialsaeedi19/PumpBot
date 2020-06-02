from data_set.BinanceDataSetCreator import BinanceDataSetCreator

if __name__ == "__main__":
    from filter.PassThroughStockFilter import PassThroughStockFilter
    from listing_obtainers.TestListingObtainer import TestListingObtainer
    from datetime import datetime
    from stock_data.HistoricalBinanceDataObtainer import \
        HistoricalBinanceDataObtainer

    listOfStocks = ["BCCBTC", "BNBBTC", "GASBTC", "HSRBTC",
                    "LRCBTC", "LTCBTC", "MCOBTC", "NEOBTC", "OAXBTC",
                    "OMGBTC", "QTUMBTC", "STRATBTC", "WTCBTC",
                    "YOYOBTC", "ZRXBTC"]
    historicalObtainer = HistoricalBinanceDataObtainer(
        datetime(day=17, month=8, year=2018, hour=0, minute=1), datetime(day=27, month=12, year=2019, hour=0, minute=1),
        # datetime(day=17, month=8, year=2018, hour=0, minute=1), datetime(day=31, month=8, year=2018, hour=0, minute=1),
        # datetime(day=31, month=8, year=2018, hour=0, minute=1), datetime(day=30, month=9, year=2018, hour=0, minute=1),
        "../binance_historical_data/")
    print("Reading historical stock data...")
    historicalObtainer.trackStocks(listOfStocks)
    dataSetCreator = BinanceDataSetCreator(historicalObtainer)
    print("Analyzing historical stock data for pumps...")
    pumps, rightBeforePumps = dataSetCreator.findPumpsForSymbols(listOfStocks,
                                                                 1440)
    pumps2, rightBeforePumps2 = dataSetCreator.findNonPumpsForSymbols(
        listOfStocks, 1440)
    rightBeforePumps, extraNonPumpsToAdd = dataSetCreator.createFinalPumpsDataSet(pumps, rightBeforePumps)
    print(rightBeforePumps2[0].columns)
    dataSetCreator.exportPumpsToCSV("final-dataset", rightBeforePumps)
    rightBeforePumps2 = dataSetCreator.createFinalNonPumpsDataSet(pumps2, rightBeforePumps2)
    rightBeforePumps2.extend(extraNonPumpsToAdd)
    dataSetCreator.exportPumpsToCSV("final-dataset", rightBeforePumps2, areTheyPumps=False)
