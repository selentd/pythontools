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
                 
    def __init__(self):
        self.mean5 = self.MeanData(5)
        self.mean13 = self.MeanData(13)
        self.mean38 = self.MeanData(38)
        self.mean89 = self.MeanData(89)        
        self.mean200 = self.MeanData(200)
    
    def setData(self, value):
        self.mean5.addValue( value )
        self.mean13.addValue( value )
        self.mean38.addValue( value )
        self.mean89.addValue( value )
        self.mean200.addValue( value ) 

class IndexData:
    def __init__(self):
        self.date = datetime.date.today()
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.mean5 = 0
        self.mean13 = 0
        self.mean38 = 0
        self.mean89 = 0
        self.mean200 = 0 

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
        self.mean13 = mean.mean13.getMeanValue()
        self.mean38 = mean.mean38.getMeanValue()
        self.mean89 = mean.mean89.getMeanValue()
        self.mean200 = mean.mean200.getMeanValue()
        
    def getDictionary(self):
        return { "date": datetime.datetime(self.date.year,
                                           self.date.month,
                                           self.date.day),
                 "open": self.close,
                 "high": self.high,
                 "low": self.low,
                 "close": self.close,
                 "mean5": self.mean5,
                 "mean13": self.mean13,
                 "mean38": self.mean38,
                 "mean89": self.mean89,
                 "mean200": self.mean200 }
        
    def setDictionary(self, data):
        self.date = data["date"]
        self.open = data["open"]
        self.high = data["high"]
        self.low = data["low"]
        self.close = data["close"]
        self.mean5 = data["mean5"]
        self.mean13 = data["mean13"]
        self.mean38 = data["mean38"]
        self.mean89 = data["mean89"]
        self.mean200 = data["mean200"]
        self._checkData()

class IndexHistory:
    def __init__(self, fileName, historyLimit = 0):
        self.fileName = fileName
        self.historyLimit = historyLimit
        self.indexHistory = collections.deque()       
        
    def readIndex(self):
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
        
        meanSet = MeanSet()
        for indexData in self.indexHistory:
            meanSet.setData(indexData.close)
            indexData.setMean( meanSet )
            
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
                                
        