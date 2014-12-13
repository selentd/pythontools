
from evalindexdata import EvalIndexDataBuy
from evalindexdata import EvalIndexDataSell

class EvalMeanOrder():
    def hasData(self, indexData):
        return False
    
class EvalMeanOrderCallBuy(EvalIndexDataBuy, EvalMeanOrder):
    def updateState(self, indexData, indexBuy):
        pass

class EvalMeanOrderCallSell(EvalIndexDataSell, EvalMeanOrder):
    def updateState(self, indexData, indexBuy):
        pass

class EvalMeanOrder5_13CallBuy(EvalMeanOrderCallBuy):   
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean13 > 0)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 > indexData.mean13)
        return checkBuy
        
class EvalMeanOrder5_13CallSell(EvalMeanOrderCallSell):    
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean13 > 0)
            
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 < indexData.mean13)
        return checkSell

class EvalMeanOrder5_38CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean38 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 > indexData.mean38)
        return checkBuy
    
class EvalMeanOrder5_38CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean38 > 0)

    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 < indexData.mean38)
        return checkSell
    
class EvalMeanOrder5_89CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean89 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 > indexData.mean89)
        return checkBuy
    
class EvalMeanOrder5_89CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean89 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 < indexData.mean89)
        return checkSell

class EvalMeanOrder5_200CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 > indexData.mean200)
        return checkBuy
    
class EvalMeanOrder5_200CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 < indexData.mean200)
        return checkSell

class EvalMeanOrder13_38CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean38 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean13 > indexData.mean38)
        return checkBuy
    
class EvalMeanOrder13_38CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean38 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean13 < indexData.mean38)
        return checkSell

class EvalMeanOrder13_89CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean89 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean13 > indexData.mean89)
        return checkBuy
    
class EvalMeanOrder13_89CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean89 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean13 < indexData.mean89)
        return checkSell

class EvalMeanOrder13_200CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean13 > indexData.mean200)
        return checkBuy
    
class EvalMeanOrder13_200CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean13 < indexData.mean200)
        return checkSell
        
class EvalMeanOrder38_89CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean89 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean38 > indexData.mean89)
        return checkBuy
    
class EvalMeanOrder38_89CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean89 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean38 < indexData.mean89)
        return checkSell

class EvalMeanOrder38_200CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean38 > indexData.mean200)
        return checkBuy
    
class EvalMeanOrder38_200CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean38 < indexData.mean200)
        return checkSell

class EvalMeanOrder89_200CallBuy(EvalMeanOrderCallBuy):
    def hasData(self, indexData):
        return (indexData.mean89 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean89 > indexData.mean200)
        return checkBuy
    
class EvalMeanOrder89_200CallSell(EvalMeanOrderCallSell):
    def hasData(self, indexData):
        return (indexData.mean89 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean89 < indexData.mean200)
        return checkSell

class EvalMeanOrder5_13_38CallBuy(EvalMeanOrder5_13CallBuy, EvalMeanOrder13_38CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder13_38CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_38CallSell(EvalMeanOrder5_13CallSell, EvalMeanOrder13_38CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder13_38CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_89CallBuy(EvalMeanOrder5_13CallBuy, EvalMeanOrder13_89CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder13_89CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_89CallSell(EvalMeanOrder5_13CallSell, EvalMeanOrder13_89CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder13_89CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_200CallBuy(EvalMeanOrder5_13CallBuy, EvalMeanOrder13_200CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder13_200CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_200CallSell(EvalMeanOrder5_13CallSell, EvalMeanOrder13_200CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder13_200CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder13_38_89CallBuy(EvalMeanOrder13_38CallBuy, EvalMeanOrder38_89CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_89CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder13_38_89CallSell(EvalMeanOrder13_38CallSell, EvalMeanOrder38_89CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_89CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder13_38_200CallBuy(EvalMeanOrder13_38CallBuy, EvalMeanOrder38_200CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_200CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder13_38_200CallSell(EvalMeanOrder13_38CallSell, EvalMeanOrder38_200CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_200CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder38_89_200CallBuy(EvalMeanOrder38_89CallBuy, EvalMeanOrder89_200CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder38_89CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder89_200CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder38_89_200CallSell(EvalMeanOrder38_89CallSell, EvalMeanOrder89_200CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder38_89CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder89_200CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_38_89CallBuy(EvalMeanOrder5_13_38CallBuy, EvalMeanOrder38_89CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_89CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_38_89CallSell(EvalMeanOrder5_13_89CallSell, EvalMeanOrder38_89CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_89CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_38_200CallBuy(EvalMeanOrder5_13_38CallBuy, EvalMeanOrder38_200CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_200CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_38_200CallSell(EvalMeanOrder5_13_38CallSell, EvalMeanOrder38_200CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_200CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder13_38_89_200CallBuy(EvalMeanOrder13_38_89CallBuy, EvalMeanOrder89_200CallBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder13_38_89CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder89_200CallBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder13_38_89_200CallSell(EvalMeanOrder13_38_89CallSell, EvalMeanOrder89_200CallSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder13_38_89CallSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder89_200CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrderPutBuy(EvalIndexDataBuy, EvalMeanOrder):
    def updateState(self, indexData, indexBuy):
        pass

class EvalMeanOrderPutSell(EvalIndexDataSell, EvalMeanOrder):
    pass

class EvalMeanOrder5_13PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean13 > 0)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 < indexData.mean13)
        return checkBuy
        
class EvalMeanOrder5_13PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean13 > 0)
            
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 > indexData.mean13)
        return checkSell

class EvalMeanOrder5_38PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean38 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 < indexData.mean38)
        return checkBuy
    
class EvalMeanOrder5_38PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean38 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 > indexData.mean38)
        return checkSell
    
class EvalMeanOrder5_89PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean89 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 < indexData.mean89)
        return checkBuy
    
class EvalMeanOrder5_89PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean89 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 > indexData.mean89)
        return checkSell

class EvalMeanOrder5_200PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean5 < indexData.mean200)
        return checkBuy
    
class EvalMeanOrder5_200PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean5 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean5 > indexData.mean200)
        return checkSell

class EvalMeanOrder13_38PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean38 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean13 < indexData.mean38)
        return checkBuy
    
class EvalMeanOrder13_38PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean38 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean13 > indexData.mean38)
        return checkSell

class EvalMeanOrder13_89PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean89 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean13 < indexData.mean89)
        return checkBuy
    
class EvalMeanOrder13_89PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean89 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean13 > indexData.mean89)
        return checkSell

class EvalMeanOrder13_200PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean13 < indexData.mean200)
        return checkBuy
    
class EvalMeanOrder13_200PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean13 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean13 > indexData.mean200)
        return checkSell
        
class EvalMeanOrder38_89PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean89 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean38 < indexData.mean89)
        return checkBuy
    
class EvalMeanOrder38_89PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean89 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean38 > indexData.mean89)
        return checkSell

class EvalMeanOrder38_200PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean38 < indexData.mean200)
        return checkBuy
    
class EvalMeanOrder38_200PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean38 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean38 > indexData.mean200)
        return checkSell

class EvalMeanOrder89_200PutBuy(EvalMeanOrderPutBuy):
    def hasData(self, indexData):
        return (indexData.mean89 > 0) and (indexData.mean200 > 0)
        
    def evaluateBuy(self, indexData):
        checkBuy = self.hasData(indexData)
        checkBuy = checkBuy and (indexData.mean89 < indexData.mean200)
        return checkBuy
    
class EvalMeanOrder89_200PutSell(EvalMeanOrderPutSell):
    def hasData(self, indexData):
        return (indexData.mean89 > 0) and (indexData.mean200 > 0)
        
    def evaluateSell(self, indexData):
        checkSell = self.hasData(indexData)
        checkSell = checkSell and (indexData.mean89 > indexData.mean200)
        return checkSell

class EvalMeanOrder5_13_38PutBuy(EvalMeanOrder5_13PutBuy, EvalMeanOrder13_38PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder13_38PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_38PutSell(EvalMeanOrder5_13PutSell, EvalMeanOrder13_38PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder13_38PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_89PutBuy(EvalMeanOrder5_13PutBuy, EvalMeanOrder13_89PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder13_89PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_89PutSell(EvalMeanOrder5_13PutSell, EvalMeanOrder13_89PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder13_89PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_200PutBuy(EvalMeanOrder5_13PutBuy, EvalMeanOrder13_200PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder13_200PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_200PutSell(EvalMeanOrder5_13PutSell, EvalMeanOrder13_200PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder13_200PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder13_38_89PutBuy(EvalMeanOrder13_38PutBuy, EvalMeanOrder38_89PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_89PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder13_38_89PutSell(EvalMeanOrder13_38PutSell, EvalMeanOrder38_89PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_89PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder13_38_200PutBuy(EvalMeanOrder13_38PutBuy, EvalMeanOrder38_200PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_200PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder13_38_200PutSell(EvalMeanOrder13_38PutSell, EvalMeanOrder38_200PutBuy):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_200PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder38_89_200PutBuy(EvalMeanOrder38_89PutBuy, EvalMeanOrder89_200PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder38_89PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder89_200PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder38_89_200PutSell(EvalMeanOrder38_89PutSell, EvalMeanOrder89_200PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder38_89PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder89_200PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_38_89PutBuy(EvalMeanOrder5_13_38PutBuy, EvalMeanOrder38_89PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_89PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_38_89PutSell(EvalMeanOrder5_13_38PutSell, EvalMeanOrder38_89PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_89PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder5_13_38_200PutBuy(EvalMeanOrder5_13_38PutBuy, EvalMeanOrder38_200PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder5_13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder38_200PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder5_13_38_200PutSell(EvalMeanOrder5_13_38PutSell, EvalMeanOrder38_200PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder5_13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder38_200PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMeanOrder13_38_89_200PutBuy(EvalMeanOrder13_38_89PutBuy, EvalMeanOrder89_200PutBuy):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMeanOrder13_38_89PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMeanOrder89_200PutBuy.evaluateBuy(self, indexData)
        return checkBuy
    
class EvalMeanOrder13_38_89_200PutSell(EvalMeanOrder13_38_89PutSell, EvalMeanOrder89_200PutSell):
    def evaluateSell(self, indexData):
        checkSell = EvalMeanOrder13_38_89PutSell.evaluateSell(self, indexData)
        checkSell = checkSell or EvalMeanOrder89_200PutSell.evaluateSell(self, indexData)
        return checkSell
