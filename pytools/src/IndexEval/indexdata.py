'''
Created on 03.09.2013

@author: selen00r
'''

import collections
import csv
import datetime
import string

class MeanSet:
    '''
    MeanSet defines a set of mean values used for index analysis.
    Currently there are mean values defined for
          5 days
         13 days
         38 days
         89 days and
        200 days
    '''
    class MeanData:
        '''
        MeanData is a helper class to calculate the mean value.
        '''
        def __init__(self, size):
            self.meanSize = size
            self.valueQueue = collections.deque()
            self.meanValue = 0

        def addValue(self, value):
            if len(self.valueQueue) < self.meanSize:
                self.valueQueue.append(value)
                self.meanValue = self.meanValue + value
            else:
                self.meanValue = self.meanValue - self.valueQueue.popleft()
                self.valueQueue.append(value)
                self.meanValue = self.meanValue + value

        def getMeanValue(self):
            if len(self.valueQueue) == self.meanSize:
                return self.meanValue / self.meanSize
            else:
                return 0

    def __init__(self):
        self.mean5 = self.MeanData(5)
        self.mean8 = self.MeanData(8)
        self.mean13 = self.MeanData(13)
        self.mean21 = self.MeanData(21)
        self.mean34 = self.MeanData(34)
        self.mean38 = self.MeanData(38)
        self.mean50 = self.MeanData(50)
        self.mean55 = self.MeanData(55)
        self.mean89 = self.MeanData(89)
        self.mean100 = self.MeanData(100)
        self.mean144 = self.MeanData(144)
        self.mean200 = self.MeanData(200)
        self.mean233 = self.MeanData(233)

    def setData(self, value):
        self.mean5.addValue( value )
        self.mean8.addValue( value )
        self.mean13.addValue( value )
        self.mean21.addValue( value )
        self.mean34.addValue( value )
        self.mean38.addValue( value )
        self.mean50.addValue( value )
        self.mean55.addValue( value )
        self.mean89.addValue( value )
        self.mean100.addValue( value )
        self.mean144.addValue( value )
        self.mean200.addValue( value )
        self.mean233.addValue( value )

class IndexData:
    '''
    IndexData defines the data of one day which is used to analyze an index.
    It holds the date, the values of the day and the corresponding mean values.
    '''
    def __init__(self):
        self.date = datetime.date.today()
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.mean5 = 0
        self.mean8 = 0
        self.mean13 = 0
        self.mean21 = 0
        self.mean34 = 0
        self.mean38 = 0
        self.mean50 = 0
        self.mean55 = 0
        self.mean89 = 0
        self.mean100 = 0
        self.mean144 = 0
        self.mean200 = 0
        self.mean233 = 0

    def _checkData(self):
        if self.low > self.high:
            temp = self.low
            self.low = self.high
            self.high = temp

    def set(self, idxDate, idxOpen, idxClose, idxHigh, idxLow ):
        self.date = idxDate
        self.open = idxOpen
        self.close = idxClose
        self.high = idxHigh
        self.low = idxLow
        self._checkData()

    def getMeanValue(self, mean):
        if mean == 5:
            return self.mean5
        elif mean == 8:
            return self.mean8
        elif mean == 13:
            return self.mean13
        elif mean == 21:
            return self.mean21
        elif mean == 34:
            return self.mean34
        elif mean == 38:
            return self.mean38
        elif mean == 50:
            return self.mean50
        elif mean == 55:
            return self.mean55
        elif mean == 89:
            return self.mean89
        elif mean == 100:
            return self.mean100
        elif mean == 144:
            return self.mean144
        elif mean == 200:
            return self.mean200
        elif mean == 233:
            return self.mean233
        else:
            return 0.0

    def setMeanValue(self, mean, value):
        if mean == 5:
            self.mean5 = value
        elif mean == 8:
            self.mean8 = value
        elif mean == 13:
            self.mean13 = value
        elif mean == 21:
            self.mean21 = value
        elif mean == 34:
            self.mean34 = value
        elif mean == 38:
            self.mean38 = value
        elif mean == 50:
            self.mean50 = value
        elif mean == 55:
            self.mean55 = value
        elif mean == 89:
            self.mean89 = value
        elif mean == 100:
            self.mean100 = value
        elif mean == 144:
            self.mean144 = value
        elif mean == 200:
            self.mean200 = value
        elif mean == 233:
            self.mean233 = value
        else:
            pass


    def setMean(self, mean):
        self.mean5 = mean.mean5.getMeanValue()
        self.mean8 = mean.mean8.getMeanValue()
        self.mean13 = mean.mean13.getMeanValue()
        self.mean21 = mean.mean21.getMeanValue()
        self.mean34 = mean.mean34.getMeanValue()
        self.mean38 = mean.mean38.getMeanValue()
        self.mean50 = mean.mean50.getMeanValue()
        self.mean55 = mean.mean55.getMeanValue()
        self.mean89 = mean.mean89.getMeanValue()
        self.mean100 = mean.mean100.getMeanValue()
        self.mean144 = mean.mean144.getMeanValue()
        self.mean200 = mean.mean200.getMeanValue()
        self.mean233 = mean.mean233.getMeanValue()

    def getDictionary(self):
        return { "date": datetime.datetime(self.date.year,
                                           self.date.month,
                                           self.date.day),
                 "open": self.close,
                 "high": self.high,
                 "low": self.low,
                 "close": self.close,
                 "mean5": self.mean5,
                 "mean8": self.mean8,
                 "mean13": self.mean13,
                 "mean21": self.mean21,
                 "mean34": self.mean34,
                 "mean38": self.mean38,
                 "mean50": self.mean50,
                 "mean55": self.mean55,
                 "mean89": self.mean89,
                 "mean100": self.mean100,
                 "mean144": self.mean144,
                 "mean200": self.mean200,
                 "mean233": self.mean233 }

    def setDictionary(self, data):
        self.date = data["date"]
        self.open = data["open"]
        self.high = data["high"]
        self.low = data["low"]
        self.close = data["close"]
        self.mean5 = data["mean5"]
        self.mean8 = data["mean8"]
        self.mean13 = data["mean13"]
        self.mean21 = data["mean21"]
        self.mean34 = data["mean34"]
        self.mean38 = data["mean38"]
        self.mean50 = data["mean50"]
        self.mean55 = data["mean55"]
        self.mean89 = data["mean89"]
        self.mean100 = data["mean100"]
        self.mean144 = data["mean144"]
        self.mean200 = data["mean200"]
        self.mean233 = data["mean233"]
        self._checkData()

class IndexHistory:
    '''
    IndexHistory defines the history of a stock index. For each available day there is one
    entry stored in a queue.
    '''
    def __init__(self):
        self.indexHistory = collections.deque()

    def readIndex(self, fileName, historyLimit = 0):
        with open(self.fileName, "rb") as iFile:
            csvReader = csv.DictReader(iFile, ['Date', 'Open', 'High', 'Low', 'Close'])
            for row in csvReader:
                current = IndexData()
                currentDate = string.split(row['Date'], '.')
                current.set( datetime.date(int(currentDate[2]), int(currentDate[1]), int(currentDate[0])),
                             float(row['Open']),
                             float(row['Close']),
                             float(row['High']),
                             float(row['Low']) )
                self.indexHistory.append( current )
                if (self.historyLimit > 0) and (len(self.indexHistory) > self.historyLimit):
                    break


        self.indexHistory.reverse()
        self.calcMeanValues()

    def addIndexData(self, data):
        self.indexHistory.append(data)

    def calcMeanValues(self):
        meanSet = MeanSet()
        for indexData in self.indexHistory:
            meanSet.setData(indexData.close)
            indexData.setMean(meanSet)

    def len(self):
        return len(self.indexHistory)

    def getFirst(self):
        return self.indexHistory[0]

    def getLast(self):
        return self.indexHistory[len(self.indexHistory)-1]

    def getIndex(self, idx):
        return self.indexHistory[idx]

class TransactionResult:
    '''
    TransactionResult defines the result of one transaction, together with the historical data
    entries between buy and sell.
    '''
    def __init__(self):
        self.indexBuy = IndexData()
        self.indexSell = IndexData()
        self.indexHistory = IndexHistory()
        self.knockOut = False

    def setResult(self, indexBuy, indexSell, knockOut = False):
        self.indexBuy = indexBuy
        self.indexSell = indexSell
        self.knockOut = knockOut

    def setResultHistory(self, indexBuy, indexSell, indexHistory, knockOut = False ):
        self.indexBuy = indexBuy
        self.indexSell = indexSell
        self.indexHistory = indexHistory
        self.knockOut = knockOut

    def getLowValue(self):
        lowValue = self.indexBuy.close
        if self.indexSell.low < lowValue:
            lowValue = self.indexSell.low

        if self.indexHistory.len() > 0:
            for idxData in self.indexHistory.indexHistory:
                if idxData.low < lowValue:
                    lowValue = idxData.low

        return lowValue

    def getHighValue(self):
        highValue = self.indexBuy.close
        if self.indexSell.high > highValue:
            highValue = self.indexSell.high

        if self.indexHistory.len() > 0:
            for idxData in self.indexHistory.indexHistory:
                if idxData.high > highValue:
                    highValue = idxData.high

        return highValue

    def isValid(self):
        return (self.indexBuy.close) > 0 and (self.indexSell.close > 0)

class TransactionResultHistory:
    '''
    IndexResultHistory defines the history of all transactions (index results) done for
    a period.
    '''
    def __init__(self):
        self.resultHistory = collections.deque()

    def addTransactionResult(self, result):
        self.resultHistory.append(result)

    def evaluateResult(self, evaluationResult, printTransaction = None):
        for transactionResult in self.resultHistory:
            evaluationResult.evaluate( transactionResult, printTransaction )

