'''
Created on 13.12.2014

@author: diesel
'''

from evalindexdata import EvalIndexDataBuy
from evalindexdata import EvalIndexDataSell

class EvalCallMW200MeanBuy( EvalIndexDataBuy ):
    def __init__(self, buyDiff):
        self.buyDiff = buyDiff
        
    def updateState(self, indexData, lastBuy):
        pass      
    
    def evaluateBuy(self, indexData):
        checkBuy = False
        buyValue = (indexData.mean200 * self.buyDiff) / 100.0
        buyValue = buyValue + indexData.mean200
        if (indexData.close > buyValue ):
            checkBuy = True
        return checkBuy   


class EvalCallMW200MeanSell( EvalIndexDataSell ):
    def __init__(self, sellDiff):
        self.sellDiff = sellDiff;
        
    def updateState(self, indexData, lastBuy):
        pass
    
    def evaluateSell(self, indexData):
        checkSell = False
        sellValue = (indexData.mean200 * self.sellDiff) / 100.0
        sellValue = sellValue + indexData.mean200
        if (indexData.close < sellValue):
            checkSell = True
        return checkSell    

