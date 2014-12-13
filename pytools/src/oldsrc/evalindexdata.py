
class EvalIndexData:
    def updateState(self, indexData, lastBuy):
        pass
    
class EvalIndexDataBuy():
    def evaluateBuy(self, indexData):
        return True    

class EvalIndexDataSell(EvalIndexData):
    def evaluateSell(self, indexData):
        return False