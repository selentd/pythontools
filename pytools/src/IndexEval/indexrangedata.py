'''
Created on 15.02.2015

@author: diesel
'''

class IndexRangeData(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    def setData(self, resultHistory):
        self.firstEntry = resultHistory[0]
        self.lastEntry = resultHistory[len(resultHistory)-1]
        self.maxClose = 0
        self.minClose = 1000000000
        self.maxHigh = 0
        self.minLow = self.minClose
        
        for entry in resultHistory:
            if entry.close > self.maxClose:
                self.maxClose = entry.close
                
            if entry.close < self.minClose:
                self.minClose = entry.close
                
            if entry.high > self.maxHigh:
                self.maxHigh = self.high
                
            if entry.low < self.minLow:
                self.minLow = self.low
                
 