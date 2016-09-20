'''
Created on 03.09.2013

@author: selen00r
'''

import collections
import csv
import datetime
import string


class MeanSet:

    class MeanData:
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

        def getDiffValue(self):
            if len(self.valueQueue) < self.meanSize:
                return 0.0
            else:
                return (self.valueQueue[self.meanSize-1] / self.valueQueue[0]) - 1.0

    class MeanData2(MeanData):
        def __init__(self, size1, size2):
            self.meanSize1 = size1
            self.meanSize2 = size2
            self.valueQueue1 = collections.deque()
            self.valueQueue2 = collections.deque()
            self.meanValue1 = 0
            self.meanValue2 = 0
            self.meanValue = 0
            
            self.lambdaValue = float(self.meanSize1)/float(self.meanSize2)
            self.alpha = (float(self.meanSize1) - 1.0) / (float(self.meanSize2) - self.lambdaValue)
            
        def addValue(self, value):
            if len(self.valueQueue1) < self.meanSize1:
                self.valueQueue1.append(value)
                self.meanValue1 = self.meanValue1 + value
            else:
                self.meanValue1 = self.meanValue1 - self.valueQueue1.popleft()
                self.valueQueue1.append(value)
                self.meanValue1 = self.meanValue1 + value
                
                if len(self.valueQueue2) < self.meanSize2:
                    self.valueQueue2.append(self.meanValue1 / self.meanSize1)
                    self.meanValue2 = self.meanValue2 + (self.meanValue1 / self.meanSize1)
                else:
                    self.meanValue2 = self.meanValue2 - self.valueQueue2.popleft()
                    self.valueQueue2.append(self.meanValue1 / self.meanSize1)
                    self.meanValue2 = self.meanValue2 + (self.meanValue1 / self.meanSize1)
                    
                    self.meanValue = ((1.0 + self.alpha) * (self.meanValue1 / self.meanSize1)) - (self.alpha) * (self.meanValue2 / self.meanSize2) 

        def getMeanValue(self):
            return self.meanValue

        def getDiffValue(self):
            if len(self.valueQueue1) < self.meanSize1:
                return 0.0
            else:
                return (self.valueQueue1[self.meanSize1-1] / self.valueQueue1[0]) - 1.0
        
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
    def __init__(self):
        self.date = datetime.date.today()
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.mean5 = 0.0
        self.mean8 = 0.0
        self.mean13 = 0.0
        self.mean21 = 0.0
        self.mean34 = 0.0
        self.mean38 = 0.0
        self.mean50 = 0.0
        self.mean55 = 0.0
        self.mean89 = 0.0
        self.mean100 = 0.0
        self.mean144 = 0.0
        self.mean200 = 0.0
        self.mean233 = 0.0
        self.grad5 = 0.0
        self.grad8 = 0.0
        self.grad13 = 0.0
        self.grad21 = 0.0
        self.grad34 = 0.0
        self.grad38 = 0.0
        self.grad50 = 0.0
        self.grad55 = 0.0
        self.grad89 = 0.0
        self.grad100 = 0.0
        self.grad144 = 0.0
        self.grad200 = 0.0
        self.grad233 = 0.0
        
        self.atr10 = 0.0


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


    def setMeanValues(self, mean5, mean13, mean38, mean89, mean200 ):
        self.mean5 = mean5
        self.mean13 = mean13
        self.mean38 = mean38
        self.mean89 = mean89
        self.mean200 = mean200

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

    def setGrad(self, mean):
        self.grad5 = mean.mean5.getDiffValue()
        self.grad8 = mean.mean8.getDiffValue()
        self.grad13 = mean.mean13.getDiffValue()
        self.grad21 = mean.mean21.getDiffValue()
        self.grad34 = mean.mean34.getDiffValue()
        self.grad38 = mean.mean38.getDiffValue()
        self.grad50 = mean.mean50.getDiffValue()
        self.grad55 = mean.mean55.getDiffValue()
        self.grad89 = mean.mean89.getDiffValue()
        self.grad100 = mean.mean100.getDiffValue()
        self.grad144 = mean.mean144.getDiffValue()
        self.grad200 = mean.mean200.getDiffValue()
        self.grad233 = mean.mean233.getDiffValue()

    def setATR(self, atr):
        self.atr10 = atr.getMeanValue()
        
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
                 "mean233": self.mean233,
                 "grad5": self.grad5,
                 "grad8": self.grad8,
                 "grad13": self.grad13,
                 "grad21": self.grad21,
                 "grad34": self.grad34,
                 "grad38": self.grad38,
                 "grad50": self.grad50,
                 "grad55": self.grad55,
                 "grad89": self.grad89,
                 "grad100": self.grad100,
                 "grad144": self.grad144,
                 "grad200": self.grad200,
                 "grad233": self.grad233,
                 "atr10" : self.atr10 }

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
        self.grad5 = data["grad5"]
        self.grad8 = data["grad8"]
        self.grad13 = data["grad13"]
        self.grad21 = data["grad21"]
        self.grad34 = data["grad34"]
        self.grad38 = data["grad38"]
        self.grad50 = data["grad50"]
        self.grad55 = data["grad55"]
        self.grad89 = data["grad89"]
        self.grad100 = data["grad100"]
        self.grad144 = data["grad144"]
        self.grad200 = data["grad200"]
        self.grad233 = data["grad233"]
        self.atr10 = data["atr10"]
        self._checkData()

class ATRCalc: 
    def __init__(self, size = 10):
        self.meanSize = size
        self.valueQueue = collections.deque()
        self.meanValue = 0.0
        self.idxYesterday = None
        self.idxToday = None

    def _updateValue(self, value):        
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
        
    def setData(self, idxData):
        if self.idxYesterday == None:
            self.idxYesterday = idxData
        else:    
            self.idxToday = idxData
            
        if self.idxYesterday != None and self.idxToday != None:
            atr = self.idxToday.high - self.idxToday.low
            if self.idxToday.high > self.idxYesterday.close:
                atr2 = self.idxToday.high - self.idxYesterday.close
            else:
                atr2 = self.idxYesterday.close - self.idxToday.high
                
            if atr2 > atr:
                atr = atr2
                
            if self.idxToday.low > self.idxYesterday.close:
                atr3 = self.idxToday.low - self.idxYesterday.close
            else:
                atr3 = self.idxYesterday.close - self.idxToday.low
                
            if atr3 > atr:
                atr = atr3        
                
            self._updateValue(atr)
            self.idxYesterday = self.idxToday 
        

class IndexHistory:
    def __init__(self, fileName, historyLimit = 0):
        self.fileName = fileName
        self.historyLimit = historyLimit
        self.indexHistory = collections.deque()

    def readIndex(self):
        with open(self.fileName, "rb") as iFile:
            csvReader = csv.DictReader(iFile, ['Date', 'Open', 'High', 'Low', 'Close'])
            for row in csvReader:
                print row
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

        meanSet = MeanSet()
        atrCalc = ATRCalc()
        
        for indexData in self.indexHistory:
            meanSet.setData(indexData.close)
            atrCalc.setData(indexData)
            indexData.setMean( meanSet )
            indexData.setGrad( meanSet )
            indexData.setATR( atrCalc )

    def addIndexData(self, data):
        self.indexHistory.append(data)


class IndexResultHistory:
    def __init__(self):
        self.winCount = 0
        self.looseCount = 0

        self.resultHistory = collections.deque()

    def addIndexResult(self, result):
        self.resultHistory.append(result)

    def evaluateResult(self, result):
        for indexResult in self.resultHistory:
            result.evaluate( indexResult )

