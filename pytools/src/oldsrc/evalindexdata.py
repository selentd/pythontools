
class EvalIndexData:
    def updateState(self, indexData, lastBuy):
        pass
    
class EvalIndexDataBuy():
    def evaluateBuy(self, indexData):
        return True
    
    def evaluateKnockOut(self, indexData):
        return False    

class EvalIndexDataSell(EvalIndexData):
    def evaluateSell(self, indexData):
        return False
    
    def evaluateKnockOut(self, indexData):
        return False    
    