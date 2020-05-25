# Name: BinanceDataSetCreator
# Author: Robert Ciborowski
# Date: 19/04/2020
# Description: Creates a data set for Binance Pump & Dumps.
import math
from math import pi
from typing import List

from stock_data import HistoricalBinanceDataObtainer
import pandas as pd
from datetime import datetime
#plotting
from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svgs
from bokeh.io import output_notebook
from bokeh.models import Axis, ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from matplotlib import pyplot as plt
import csv

class BinanceDataSetCreator:
    dataObtainer: HistoricalBinanceDataObtainer
    numberOfSamples: int
    samplesBeforePumpPeak: int

    def __init__(self, dataObtainer: HistoricalBinanceDataObtainer):
        self.dataObtainer = dataObtainer
        self.numberOfSamples = 25
        self.samplesBeforePumpPeak = 7

    def exportPumpsToCSV(self, symbol: str, rightBeforePumps: List,
                         areTheyPumps=True, pathPrefix=""):
        if len(rightBeforePumps) == 0:
            return

        if areTheyPumps:
            path = pathPrefix + symbol + "-pumps.csv"
        else:
            path = pathPrefix + symbol + "-non-pumps.csv"

        try:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                numberOfRAs = self.numberOfSamples
                volumeList = ["Volume-RA-" + str(i) for i in range(numberOfRAs)]
                priceList = ["Price-RA-" + str(i) for i in range(numberOfRAs)]
                writer.writerow(volumeList + priceList + ["Pump"])

                for df in rightBeforePumps:
                    mean = df["24m Volume RA"].mean()
                    std = df["24m Volume RA"].std()
                    volumes = (df["24m Volume RA"] - mean) / std
                    mean = df["24m Close Price RA"].mean()
                    std = df["24m Close Price RA"].std()
                    prices = (df["24m Close Price RA"] - mean) / std
                    csvRow = []

                    # Becomes true if a value is nan so that we can skip this
                    # pump.
                    cancel = False

                    for value in volumes:
                        if math.isnan(value):
                            cancel = True
                            break

                        csvRow.append(value)

                    if cancel:
                        continue

                    for value in prices:
                        if math.isnan(value):
                            cancel = True
                            break
                        csvRow.append(value)

                    if cancel:
                        continue

                    if areTheyPumps:
                        csvRow.append(1)
                    else:
                        csvRow.append(0)

                    writer.writerow(csvRow)

        except IOError as e:
            print("Error writing to csv file! " + str(e))

    def createFinalPumpsDataSet(self, pumps: List, rightBeforePumps: List):
        # lst = []
        lst2 = []
        length = len(pumps)

        for i in range(0, length):
            print("Is this a pump? " + str(i + 1) + "/" + str(length))
            df = pumps[i]
            df2 = rightBeforePumps[i]
            self._plotWithPyPlot(df, df2)
            input1 = input()

            if input1 == "y":
                # lst.append(df)
                lst2.append(df2)
            elif input1 == "n":
                continue
            else:
                print("Invalid input.")
                i -= 1

        return lst2

    def createFinalNonPumpsDataSet(self, pumps: List, rightBeforePumps: List):
        # We don't need to do anything anymore.
        return rightBeforePumps

    def findPumpsForSymbols(self, symbols: List[str], amountToIncrement: int):
        """
        Returns random non-pumps for a list of symbols.
        Precondition: symbols is not empty!!!

        :param symbols: the symbols
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframe lists where df contains pumps,
                 df2 contains the moment before the pumps.
        """
        lst1, lst2 = self.findPumpsForSymbol(symbols[0], amountToIncrement)

        for i in range(1, len(symbols)):
            lst3, lst4 = self.findPumpsForSymbol(symbols[i], amountToIncrement)
            lst1 += lst3
            lst2 += lst4

        return lst1, lst2

    def findNonPumpsForSymbols(self, symbols: List[str], amountToIncrement: int):
        """
        Returns random non-pumps for a list of symbols.
        Precondition: symbols is not empty!!!

        :param symbols: the symbols
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframe lists where df contains
                 non-pumps, df2 contains non-pumps of size self.numberOfSamples
        """
        lst1, lst2 = self.findNonPumpsForSymbol(symbols[0], amountToIncrement)

        for i in range(1, len(symbols)):
            lst3, lst4 = self.findNonPumpsForSymbol(symbols[i], amountToIncrement)
            lst1 += lst3
            lst2 += lst4

        return lst1, lst2

    def findPumpsForSymbol(self, symbol: str, amountToIncrement: int):
        """
        Returns pumps for a symbol.
        Precondition: symbol is not empty!!!

        :param symbol: the symbols
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframes where df contains pump & dumps,
                 df2 contains the moment before the pump.
        """
        df = self.dataObtainer.data[symbol]
        dfs = []
        dfs2 = []

        for i in range(0, int((self._getNumberOfRows(df) - amountToIncrement) /
                              (amountToIncrement + 1))):
            rowEntry, df2 = self.findPumpAndDumps(symbol, i * amountToIncrement,
                                                  amountToIncrement + (i + 1) *
                                                  amountToIncrement)

            if rowEntry["Pump and Dumps"] > 0:
                dfs.append(df2)
                dfs2.append(rowEntry["Right Before DF"])

        return dfs, dfs2

    def findNonPumpsForSymbol(self, symbol: str, amountToIncrement: int):
        """
        Returns random non-pumps for a symbol.
        Precondition: symbols is not empty!!!

        :param symbol: the symbol
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframes where df contains non-pumps,
                 df2 contains non-pumps of size self.numberOfSamples
        """
        df = self.dataObtainer.data[symbol]
        dfs = []
        dfs2 = []

        for i in range(0, int((self._getNumberOfRows(df) - amountToIncrement) /
                              (amountToIncrement + 1))):
            rowEntry, df2 = self.findPumpAndDumps(symbol, i * amountToIncrement,
                                                  amountToIncrement + (i + 1) *
                                                  amountToIncrement)

            if rowEntry["Pump and Dumps"] == 0:
                dfs.append(df2)
                dfs2.append(df2.iloc[0:self.numberOfSamples])

        return dfs, dfs2


    def findPumpAndDumps(self, symbol: str, startIndex: int, endIndex: int,
                         plot=False):
        df = self.dataObtainer.data[symbol].iloc[startIndex:endIndex]
        # return self._analyseSymbolForPumps(symbol, df, 3, 1.05), df
        return self._analyseSymbolForPumps(symbol, df, 2.5, 1.05), df

    # returns final dataframe
    def _analyseSymbolForPumps(self, symbol: str, df: pd.DataFrame, volumeThreshold: float,
                               priceThreshold: float, windowSize=24):
        """
        :param symbol: symbol code (e.g. OAXBTC)
        :param df: pandas dataframe with the data
        :param volumeThreshold: volume threshold, e.g. 5 (500%)
        :param priceThreshold: price threshold, e.g. 1.05 (5%)
        :param windowSize: size of the window to use for computing rolling
               average, in hours
        :return: a dict with all the computed data (see end of this function)
        """
        exchangeName = "binance"

        # This finds spikes for volume and price.
        volumeMask, vdf = self._findVolumeSpikes(df, volumeThreshold, windowSize)
        volumeSpikeAmount = self._getNumberOfRows(vdf)

        pmask, pdf = self._findPriceSpikes(df, priceThreshold, windowSize)
        priceSpikeAmount = self._getNumberOfRows(pdf)

        # pdmask, pddf = self._findPriceDumps(df, windowSize)
        # vdmask, vddf = self._findVolumeDumps(df, windowSize)

        # This finds coinciding price and volume spikes.
        volumePriceMask = (volumeMask) & (pmask)
        volumePriceDF = df[volumePriceMask]
        volumePriceCombinedRowsAmount = self._getNumberOfRows(volumePriceDF)

        # These are coinciding price and volume spikes for alleged P&D (more
        # than 1x per given time removed).
        volumePriceFinalDF = self._removeSameDayPumps(volumePriceDF)
        allegedAmount = self._getNumberOfRows(volumePriceFinalDF)

        # This finds coinciding price and volume spikes (with dumps afterwards).
        # finalMask = (volumeMask) & (pmask) & (pdmask)
        finalMask = (volumeMask) & (pmask)
        finalDF = df[finalMask]

        # This removes indicators which occur on the same day.
        finalCombined = self._removeSameDayPumps(finalDF)
        finalCombinedAmount = self._getNumberOfRows(finalCombined)

        if finalCombinedAmount == 0:
            rightBeforeDF = finalCombined
        else:
            timeIndex = finalCombined.index[0]
            endIndex = self.dataObtainer.data[symbol].index.get_loc(timeIndex)\
                       - self.samplesBeforePumpPeak
            startIndex = endIndex - self.numberOfSamples

            if startIndex < 0:
                rightBeforeDF = finalCombined
            else:
                rightBeforeDF = self.dataObtainer.data[symbol].iloc[startIndex:endIndex]

        rowEntry = {'Exchange': exchangeName,
                    'Symbol': symbol,
                    'Price Spikes': priceSpikeAmount,
                    'Volume Spikes': volumeSpikeAmount,
                    'Alleged Pump and Dumps': allegedAmount,
                    'Pump and Dumps': finalCombinedAmount,
                    "Right Before DF": rightBeforeDF
                    }

        return rowEntry

    def _getNumberOfRows(self, df: pd.DataFrame):
        return df.shape[0]

    def _removeSameDayPumps(self, df: pd.DataFrame):
        """
        Removes spikes that occur on the same day.
        """
        df = df.copy()
        df['Timestamp_DAYS'] = df['Timestamp'].apply(
            lambda x: x.replace(hour=0, minute=0, second=0))
        df = df.drop_duplicates(subset='Timestamp_DAYS', keep='last')
        return df

    def _findVolumeSpikes(self, df: pd.DataFrame, volumeThreshold: float,
                          windowSize: int):
        """
        Finds volume spikes in a given dataframe, with a certain threshold
        and window size.

        :return: a (boolean_mask,dataframe) tuple
        """
        # -- add rolling average column to df --
        vRA = str(windowSize) + 'm Volume RA'
        self._addRA(df, windowSize, 'Volume', vRA)

        # -- find spikes --
        volumeThreshold = volumeThreshold * df[vRA]
        # This is where the volume is at least v_thresh greater than the x-hr RA
        volumeSpikeMask = df["Volume"] > volumeThreshold
        volumeSpikeDF = df[volumeSpikeMask]
        return (volumeSpikeMask, volumeSpikeDF)

    def _findPriceSpikes(self, df: pd.DataFrame, priceThreshold: float,
                         windowSize: int):
        """
        Finds price spikes in a given df, with a certain threshold and window
        size.

        :return: a (boolean_mask,dataframe) tuple
        """
        # -- add rolling average column to df --
        pRA = str(windowSize) + 'm Close Price RA'
        self._addRA(df, windowSize, 'Close', pRA)

        # -- find spikes --
        newThreshold = priceThreshold * df[pRA]
        # This is where the high is at least p_thresh greater than the x-hr RA.
        priceSpikeMask = df["Close"] > newThreshold
        priceSpikeDF = df[priceSpikeMask]
        return (priceSpikeMask, priceSpikeDF)

    def _findPriceDumps(self, df: pd.DataFrame, windowSize: int):
        """
        Finds price dumps in a given dataframe, with a certain threshold and
        window size. Requires a price rolling average column of the proper
        window size and naming convention

        :return: a (boolean_mask,dataframe) tuple
        """
        pRA = str(windowSize) + "m Close Price RA"
        pRA_plus = pRA + "+" + str(windowSize)
        df[pRA_plus] = df[pRA].shift(-windowSize)
        priceDumpMask = df[pRA_plus] <= (df[pRA] + df[pRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _findVolumeDumps(self, df: pd.DataFrame, windowSize: int):
        vRA = str(windowSize) + "m Volume RA"
        vRA_plus = vRA + "+" + str(windowSize)
        df[vRA_plus] = df[vRA].shift(-windowSize)
        priceDumpMask = df[vRA_plus] <= (df[vRA] + df[vRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _findNonVolumeSpikes(self, df: pd.DataFrame, volumeThreshold: float,
                             windowSize: int):
        # -- add rolling average column to df --
        vRA = str(windowSize) + 'm Volume RA'
        self._addRA(df, windowSize, 'Volume', vRA)

        # -- find spikes --
        volumeThreshold = volumeThreshold * df[vRA]
        # This is where the volume is at least v_thresh greater than the x-hr RA
        volumeSpikeMask = df["Volume"] <= volumeThreshold
        volumeSpikeDF = df[volumeSpikeMask]
        return (volumeSpikeMask, volumeSpikeDF)

    def _findNonPriceSpikes(self, df: pd.DataFrame, priceThreshold: float,
                            windowSize: int):
        """
        Finds price spikes in a given dataframe, with a certain threshold and
        window size.

        :return: a (boolean_mask,dataframe) tuple
        """
        # -- add rolling average column to df --
        pRA = str(windowSize) + 'm Close Price RA'
        self._addRA(df, windowSize, 'Close', pRA)

        # -- find spikes --
        newThreshold = priceThreshold * df[pRA]
        # This is where the high is at least priceThreshold greater than the
        # x-hr RA.
        priceSpikeMask = df["Close"] <= newThreshold
        priceSpikeDF = df[priceSpikeMask]
        return (priceSpikeMask, priceSpikeDF)

    def _findNonPriceDumps(self, df: pd.DataFrame, windowSize: int):
        """
        Finds price dumps in a given dataframe, with a certain threshold and
        window size. Requires a price rolling average column of the proper
        window size and naming convention :return: a (boolean_mask,
        dataframe) tuple
        """
        pRA = str(windowSize) + "m Close Price RA"
        pRA_plus = pRA + "+" + str(windowSize)
        df[pRA_plus] = df[pRA].shift(-windowSize)
        priceDumpMask = df[pRA_plus] > (df[pRA] + df[pRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _findNonVolumeDumps(self, df: pd.DataFrame, windowSize: int):
        vRA = str(windowSize) + "m Volume RA"
        vRA_plus = vRA + "+" + str(windowSize)
        df[vRA_plus] = df[vRA].shift(-windowSize)
        priceDumpMask = df[vRA_plus] > (df[vRA] + df[vRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _addRA(self, df, windowSize, col, name):
        """
        Adds a rolling average column with specified window size to a given
        dataframe and column.
        """
        df[name] = df[col].rolling(window=windowSize, min_periods=1,
                                     center=False).mean()

    def _plotWithPyPlot(self, df, df2):
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))
        fig.tight_layout()

        # plt.figure()
        # axes[0].xlabel("Timestamp")
        # axes[0].ylabel("Value")
        axes[0][0].plot(df[["Timestamp"]], df[["High"]], label="High")
        axes[0][0].plot(df2.iloc[0]["Timestamp"], df2.iloc[0]["High"],
                        marker='o', markersize=3, color="red")
        axes[0][0].plot(df2.iloc[-1]["Timestamp"], df2.iloc[-1]["High"],
                        marker='o', markersize=3, color="red")
        axes[0][0].set_title("Zoomed Out - Price High")
        # axes[0].legend()
        # plt.show()

        # plt.figure()
        # axes[1].xlabel("Timestamp")
        # axes[1].ylabel("Value")
        axes[1][0].plot(df[["Timestamp"]], df[["Volume"]], label="Volume")
        axes[1][0].plot(df2.iloc[0]["Timestamp"], df2.iloc[0]["Volume"],
                        marker='o', markersize=3, color="red")
        axes[1][0].plot(df2.iloc[-1]["Timestamp"], df2.iloc[-1]["Volume"],
                        marker='o', markersize=3, color="red")
        axes[1][0].set_title("Zoomed Out - Volume")
        # axes[1].legend()
        # plt.show()

        axes[0][1].plot(df2[["Timestamp"]], df2[["High"]], label="High")
        axes[0][1].set_title("Zoomed In - Price High")
        axes[1][1].plot(df2[["Timestamp"]], df2[["Volume"]], label="Volume")
        axes[1][1].set_title("Zoomed In - Volume")

        fig.show()