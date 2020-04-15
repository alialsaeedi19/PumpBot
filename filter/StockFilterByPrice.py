# Name: Stock filter by price
# Author: Robert Ciborowski
# Date: 26/03/2020
# Description: Filters out stocks.

from __future__ import annotations

from typing import Dict
from datetime import datetime
import pandas as pd
import yfinance as yf


from listing_obtainers import ListingObtainer
from stock_data import StockDataObtainer


class StockFilterByPrice:
    priceThreshold: int
    template: Dict
    data: Dict
    filtered_stocks: pd.DataFrame
    dayThreshold: int
    timestampOfDownload: datetime
    dataObtainer: StockDataObtainer

    def __init__(self, priceThreshold: int, dataObtainer: StockDataObtainer, dayThreshold=5):
        self.priceThreshold = priceThreshold
        self.data = {
            "Ticker": [],
            "Price": []
        }
        self.dataObtainer = dataObtainer
        self.dayThreshold = dayThreshold

    """
    Changes the day threshold (default is 5), which stores how long ago the stock
    must have had a price update/change for it to be used.
    """
    def changeDayThreshold(self, dayThreshold: int) -> StockFilterByPrice:
        self.dayThreshold = dayThreshold
        return self

    def addListings(self, obtainer: ListingObtainer) -> StockFilterByPrice:
        dataframe = obtainer.obtain()

        for index, row in dataframe.iterrows():
            self.data["Ticker"].append(row["Ticker"])
            self.data["Price"].append(0)

        self.dataObtainer.trackStocks(self.data["Ticker"])
        return self

    def getPricesForListings(self) -> StockFilterByPrice:
        self.timestampOfDownload = datetime.now()
        data2 = {"Ticker": [], "Price": []}

        for ticker in self.data["Ticker"]:
            lst = self.dataObtainer.obtainPrices(ticker, 1)

            if len(lst) != 0:
                data2["Ticker"].append(ticker)
                data2["Price"].append(lst[0])

        self.data = data2
        return self


    """
    Filters out stocks above a threshold price.
    Preconditions: coloumn "Ticker" of df contains stock tickers as strings,
                   coloumn "Price" of df contains prices
    """
    def filterStocks(self) -> StockFilterByPrice:
        dictionary = {
            "Ticker": [],
            "Price": []
        }

        toRemove = []

        for i in range(len(self.data["Ticker"])):
            if self.data["Price"][i] <= self.priceThreshold:
                dictionary["Ticker"].append(self.data["Ticker"][i])
                dictionary["Price"].append(self.data["Price"][i])
            else:
                toRemove.append(self.data["Ticker"][i])

        self.filtered_stocks = pd.DataFrame(dictionary,
                                            columns=["Ticker", "Price"])
        self.dataObtainer.stopTrackingStocks(toRemove)
        return self
