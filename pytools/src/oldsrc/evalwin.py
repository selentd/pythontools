from evalindexdata import EvalIndexDataSell

class EvalWinSellCall(EvalIndexDataSell):
    def __init__(self, maxLoss):
        self.maxLoss = maxLoss
        self.lastClose = 0.0
        
    def updateState(self, indexData, lastBuy):
        self.lastClose = lastBuy.close
        
    def evaluateMaxLoss(self, close):
        checkSell = False
        result = close / self.lastClose
        result -= 1.0
        result *= 100.0
        if result < self.maxLoss:
            checkSell = True
            
        return checkSell
            
    def evaluateSell(self, indexData):
        return self.evaluateMaxLoss(indexData.close)
    
class EvalWinSellPut(EvalIndexDataSell):
    def __init__(self, maxLoss):
        self.maxLoss = maxLoss
        self.lastClose = 0.0
        
    def updateState(self, indexData, lastBuy):
        self.lastClose = lastBuy.close
        
    def evaluateMaxLoss(self, close):
        checkSell = False
        result = self.lastClose / close
        result -= 1.0
        result *= 100.0
        if result < self.maxLoss:
            checkSell = True
            
        return checkSell
            
    def evaluateSell(self, indexData):
        return self.evaluateMaxLoss(indexData.close)
        