
from evalindexdata import EvalIndexDataBuy
from evalindexdata import EvalIndexDataSell

class EvalMeanBuy( EvalIndexDataBuy ):
    def updateState(self, indexData, lastBuy):
        pass        

class EvalMeanSell( EvalIndexDataSell ):
    def updateState(self, indexData, lastBuy):
        pass
    
class EvalMeanCallBuy( EvalMeanBuy ):
    def evaluateMeanBuy(self, close, mean):
        return (mean > 0) and (close > mean)
    
class EvalMeanCallSell( EvalMeanSell ):
    def evaluateMeanSell(self, close, mean):
        return (mean > 0) and (close < mean)
        
class EvalMean5CallBuy( EvalMeanCallBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy(indexData.close, indexData.mean5)

class EvalMean5CallSell( EvalMeanCallSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell(indexData.close, indexData.mean5)
    
class EvalMean13CallBuy( EvalMeanCallBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy(indexData.close, indexData.mean13)

class EvalMean13CallSell( EvalMeanCallSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell(indexData.close, indexData.mean13)
    
class EvalMean38CallBuy( EvalMeanCallBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy(indexData.close, indexData.mean38)

class EvalMean38CallSell( EvalMeanCallSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell(indexData.close, indexData.mean38)

class EvalMean89CallBuy( EvalMeanCallBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy(indexData.close, indexData.mean89)

class EvalMean89CallSell( EvalMeanCallSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell(indexData.close, indexData.mean89)
    
class EvalMean200CallBuy( EvalMeanCallBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy(indexData.close, indexData.mean200)

class EvalMean200CallSell( EvalMeanCallSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell(indexData.close, indexData.mean200)
    
class EvalMean5_13CallBuy( EvalMean5CallBuy, EvalMean13CallBuy ):        
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean13CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_13CallSell( EvalMean5CallSell, EvalMean13CallSell ):    
    def evaluateSell(self, indexData):
        checkSell = EvalMean5CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean13CallSell.evaluateSell(self, indexData)
        return checkSell
           
class EvalMean5_38CallBuy( EvalMean5CallBuy, EvalMean38CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean38CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_38CallSell( EvalMean5CallSell, EvalMean38CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean38CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_89CallBuy( EvalMean5CallBuy, EvalMean89CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_89CallSell( EvalMean5CallSell, EvalMean89CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_200CallBuy( EvalMean5CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_200CallSell( EvalMean5CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean13_38CallBuy( EvalMean13CallBuy, EvalMean38CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean38CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_38CallSell( EvalMean13CallSell, EvalMean38CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean38CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean13_89CallBuy( EvalMean13CallBuy, EvalMean89CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_89CallSell( EvalMean13CallSell, EvalMean89CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean13_200CallBuy( EvalMean13CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_200CallSell( EvalMean13CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean38_89CallBuy( EvalMean38CallBuy, EvalMean89CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean38_89CallSell( EvalMean38CallSell, EvalMean89CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean38_200CallBuy( EvalMean38CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean38_200CallSell( EvalMean38CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean89_200CallBuy( EvalMean89CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean89CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean89_200CallSell( EvalMean89CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean89CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_13_38CallBuy( EvalMean5_13CallBuy, EvalMean38CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean38CallBuy.evaluateBuy(self, indexData)
        return checkBuy    

class EvalMean5_13_38CallSell( EvalMean5_13CallSell, EvalMean38CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean38CallSell.evaluateSell(self, indexData)
        return checkSell    
    
class EvalMean5_13_89CallBuy( EvalMean5_13CallBuy, EvalMean89CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89CallBuy.evaluateBuy(self, indexData)
        return checkBuy    

class EvalMean5_13_89CallSell( EvalMean5_13CallSell, EvalMean89CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89CallSell.evaluateSell(self, indexData)
        return checkSell    

class EvalMean5_13_200CallBuy( EvalMean5_13CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy    

class EvalMean5_13_200CallSell( EvalMean5_13CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell    

class EvalMean13_38_89CallBuy( EvalMean13_38CallBuy, EvalMean89CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_38_89CallSell( EvalMean13_38CallBuy, EvalMean89CallBuy ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMean13_38_200CallBuy( EvalMean13_38CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_38_200CallSell( EvalMean13_38CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell

class EvalMean38_89_200CallBuy( EvalMean38_89CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean38_89CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean38_89_200CallSell( EvalMean38_89CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean38_89CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_13_38_89CallBuy( EvalMean5_13_38CallBuy, EvalMean89CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89CallBuy.evaluateBuy(self, indexData)
        return checkBuy        

class EvalMean5_13_38_89CallSell( EvalMean5_13_38CallSell, EvalMean89CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89CallSell.evaluateSell(self, indexData)
        return checkSell        

class EvalMean5_13_38_200CallBuy( EvalMean5_13_38CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13_38CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy        

class EvalMean5_13_38_200CallSell( EvalMean5_13_38CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13_38CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell        

class EvalMean13_38_89_200CallBuy( EvalMean13_38_89CallBuy, EvalMean200CallBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13_38_89CallBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200CallBuy.evaluateBuy(self, indexData)
        return checkBuy        

class EvalMean13_38_89_200CallSell( EvalMean13_38_89CallSell, EvalMean200CallSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13_38_89CallSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200CallSell.evaluateSell(self, indexData)
        return checkSell        

class EvalMeanPutBuy( EvalMeanBuy ):
    def evaluateMeanBuy(self, close, mean):
        return (mean > 0) and (close < mean)

class EvalMeanPutSell( EvalMeanSell ):
    def evaluateMeanSell(self, close, mean):
        return (mean > 0) and (close > mean)
    
class EvalMean5PutBuy( EvalMeanPutBuy ):           
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy( indexData.close, indexData.mean5 )

class EvalMean5PutSell( EvalMeanPutSell ):           
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell( indexData.close, indexData.mean5 )

class EvalMean13PutBuy( EvalMeanPutBuy ):           
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy( indexData.close, indexData.mean13 )

class EvalMean13PutSell( EvalMeanPutSell ):           
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell( indexData.close, indexData.mean13 )
    
class EvalMean38PutBuy( EvalMeanPutBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy( indexData.close, indexData.mean38 )

class EvalMean38PutSell( EvalMeanPutSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell( indexData.close, indexData.mean38 )

class EvalMean89PutBuy( EvalMeanPutBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy( indexData.close, indexData.mean89 )

class EvalMean89PutSell( EvalMeanPutSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell( indexData.close, indexData.mean89 )
    
class EvalMean200PutBuy( EvalMeanPutBuy ):   
    def evaluateBuy(self, indexData):
        return self.evaluateMeanBuy( indexData.close, indexData.mean200 )

class EvalMean200PutSell( EvalMeanPutSell ):   
    def evaluateSell(self, indexData):
        return self.evaluateMeanSell( indexData.close, indexData.mean200 )
    
class EvalMean5_13PutBuy( EvalMean5PutBuy, EvalMean13PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean13PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_13PutSell( EvalMean5PutSell, EvalMean13PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean13PutSell.evaluateSell(self, indexData)
        return checkSell
        
class EvalMean5_38PutBuy( EvalMean5PutBuy, EvalMean38PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean38PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_38PutSell( EvalMean5PutSell, EvalMean38PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean38PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_89PutBuy( EvalMean5PutBuy, EvalMean89PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_89PutSell( EvalMean5PutSell, EvalMean89PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_200PutBuy( EvalMean5PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean5_200PutSell( EvalMean5PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean13_38PutBuy( EvalMean13PutBuy, EvalMean38PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean38PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_38PutSell( EvalMean13PutSell, EvalMean38PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean38PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean13_89PutBuy( EvalMean13PutBuy, EvalMean89PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_89PutSell( EvalMean13PutSell, EvalMean89PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean13_200PutBuy( EvalMean13PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_200PutSell( EvalMean13PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean38_89PutBuy( EvalMean38PutBuy, EvalMean89PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean38_89PutSell( EvalMean38PutSell, EvalMean89PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean38_200PutBuy( EvalMean38PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean38_200PutSell( EvalMean38PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean89_200PutBuy( EvalMean89PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean89PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean89_200PutSell( EvalMean89PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean89PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_13_38PutBuy( EvalMean5_13PutBuy, EvalMean38PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean38PutBuy.evaluateBuy(self, indexData)
        return checkBuy    

class EvalMean5_13_38PutSell( EvalMean5_13PutSell, EvalMean38PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean38PutSell.evaluateSell(self, indexData)
        return checkSell    
    
class EvalMean5_13_89PutBuy( EvalMean5_13PutBuy, EvalMean89PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89PutBuy.evaluateBuy(self, indexData)
        return checkBuy    

class EvalMean5_13_89PutSell( EvalMean5_13PutSell, EvalMean89PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89PutSell.evaluateSell(self, indexData)
        return checkSell    

class EvalMean5_13_200PutBuy( EvalMean5_13PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy    

class EvalMean5_13_200PutSell( EvalMean5_13PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell    

class EvalMean13_38_89PutBuy( EvalMean13_38PutBuy, EvalMean89PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_38_89PutSell( EvalMean13_38PutSell, EvalMean89PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMean13_38_200PutBuy( EvalMean13_38PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean13_38_200PutSell( EvalMean13_38PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell

class EvalMean38_89_200PutBuy( EvalMean38_89PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean38_89PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy

class EvalMean38_89_200PutSell( EvalMean38_89PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean38_89PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell
    
class EvalMean5_13_38_89PutBuy( EvalMean5_13_38PutBuy, EvalMean89PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean89PutBuy.evaluateBuy(self, indexData)
        return checkBuy        

class EvalMean5_13_38_89PutSell( EvalMean5_13_38PutSell, EvalMean89PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean89PutSell.evaluateSell(self, indexData)
        return checkSell        

class EvalMean5_13_38_200PutBuy( EvalMean5_13_38PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean5_13_38PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy        

class EvalMean5_13_38_200PutSell( EvalMean5_13_38PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean5_13_38PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell        

class EvalMean13_38_89_200PutBuy( EvalMean13_38_89PutBuy, EvalMean200PutBuy ):
    def evaluateBuy(self, indexData):
        checkBuy = EvalMean13_38_89PutBuy.evaluateBuy(self, indexData)
        checkBuy = checkBuy and EvalMean200PutBuy.evaluateBuy(self, indexData)
        return checkBuy        

class EvalMean13_38_89_200PutSell( EvalMean13_38_89PutSell, EvalMean200PutSell ):
    def evaluateSell(self, indexData):
        checkSell = EvalMean13_38_89PutSell.evaluateSell(self, indexData)
        checkSell = checkSell and EvalMean200PutSell.evaluateSell(self, indexData)
        return checkSell        

