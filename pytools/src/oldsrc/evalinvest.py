'''
Created on 13.06.2013

@author: selen00r
'''

import collections
import datetime

class MeanData:
    """
    Class to calculate mean values
    """
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

class MeanSet:
    def __init__(self):
        self.mean5 = MeanData(5)
        self.mean13 = MeanData(13)
        self.mean38 = MeanData(38)
        self.mean89 = MeanData(89)        
        self.mean200 = MeanData(200)
    
    def setData(self, value):
        self.mean5.addValue( value )
        self.mean13.addValue( value )
        self.mean38.addValue( value )
        self.mean89.addValue( value )
        self.mean200.addValue( value ) 
                
class IndexData:
    """
    Class to collect the data of one single day in the life of an index
    """
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
      
    def set(self, idxDate, idxOpen, idxClose, idxHigh, idxLow ):
        self.date = idxDate
        self.open = idxOpen
        self.close = idxClose
        self.high = idxHigh
        self.low = idxLow
        
    def setMean(self, meanSet):
        self.mean5 = meanSet.mean5.getMeanValue()
        self.mean13 = meanSet.mean13.getMeanValue()
        self.mean38 = meanSet.mean38.getMeanValue()
        self.mean89 = meanSet.mean89.getMeanValue()
        self.mean200 = meanSet.mean200.getMeanValue()

class EvaluateMean:
    def evaluateBuyMean(self, indexData):
        return False
        
    def evaluateSellMean(self, indexData):
        return False
        
class EvaluateMeanCall5( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean5 > 0) and (indexData.close > indexData.mean5)

    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean5( indexData )
    
class EvaluateMeanCall13( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean13 > 0) and (indexData.close > indexData.mean13)

    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean13(indexData)

class EvaluateMeanCall38( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean38 > 0) and (indexData.close > indexData.mean38)

    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean38(indexData)

class EvaluateMeanCall89( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean89 > 0) and (indexData.close > indexData.mean89)
    
    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean89(indexData)
    
class EvaluateMeanCall200( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean200 > 0) and (indexData.close > indexData.mean200)
        
    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean200(indexData)

class EvaluateMeanPut5( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean5 > 0) and (indexData.close < indexData.mean5)

    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean5( indexData )
    
class EvaluateMeanPut13( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean13 > 0) and (indexData.close < indexData.mean13)

    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean13(indexData)

class EvaluateMeanPut38( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean38 > 0) and (indexData.close < indexData.mean38)

    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean38(indexData)

class EvaluateMeanPut89( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean89 > 0) and (indexData.close < indexData.mean89)
    
    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean89(indexData)
    
class EvaluateMeanPut200( EvaluateMean ):    
    def evaluateBuyMean(self, indexData):
        return (indexData.mean200 > 0) and (indexData.close < indexData.mean200)
        
    def evaluateSellMean(self, indexData):
        return not self.evaluateBuyMean200(indexData)
    
class EvaluateMeanGradient:
    def __init__(self, gradSize, lookBack = 0):
        self.gradSize = gradSize
        self.lookBack = lookBack
        if self.lookBack > self.gradSize:
            self.lookBack = self.gradSize
        self.lookBackIndex = self.gradSize - self.lookBack
        self.meanGradient = collections.deque((0,0), self.gradSize)
        
    def updateGradient(self, meanValue):
        self.meanGradient.append( meanValue )
        
    def isGradRising(self):
        isRising = False
        if self.lookBack > 0:
            isRising = (self.meanGradient[0] > 0) and (self.meanGradient[self.gradSize-1] > self.meanGradient[self.lookBackIndex])
            
        return isRising
    
    def isGradFalling(self):
        return False
               
class EvaluateInvestStrategie:
    """
    Base class for an investment strategy. all other classes must inherit this base class
    """
    def __init__(self):
        self.name = "EvalInvestStrategie"
        self.state = 0
        self.buyValue = 0.0
        self.sellValue = 0.0
        self.maxLossAbsolute = 1.0
        self.maxLoss = 1.0
        
        self.winCount = 0
        self.lossCount = 0
        
        self.gradMean5   = collections.deque((0,0), 5)
        self.gradMean13  = collections.deque((0,0), 13)
        self.gradMean38  = collections.deque((0,0), 38)
        self.gradMean89  = collections.deque((0,0), 89)
        self.gradMean200 = collections.deque((0,0), 200)

        self.lookBack = 200
        
    def isGradMean5Rising(self, lookBack = 5):
        if (lookBack > 5):
            lookBack = 0
        else:
            lookBack = 5 - lookBack
            
        return (self.gradMean5[0] > 0) and (self.gradMean5[4] > self.gradMean5[lookBack])
    
    def isGradMean13Rising(self, lookBack = 13):
        if (lookBack > 13):
            lookBack = 0
        else:
            lookBack = 13 - lookBack
        return (self.gradMean13[0] > 0) and (self.gradMean13[12] > self.gradMean13[lookBack])

    def isGradMean38Rising(self, lookBack = 38):
        if (lookBack > 38):
            lookBack = 0
        else:
            lookBack = 38 - lookBack
        return (self.gradMean38[0] > 0) and (self.gradMean38[37] > self.gradMean38[lookBack])
               
    def isGradMean89Rising(self, lookBack = 89):
        if (lookBack > 89):
            lookBack = 0
        else:
            lookBack = 89 - lookBack
        return (self.gradMean89[0] > 0) and (self.gradMean89[88] > self.gradMean89[lookBack])
    
    def isGradMean200Rising(self, lookBack = 200):
        if (lookBack > 200):
            lookBack = 0
        else:
            lookBack = 200 - lookBack
        return (self.gradMean200[0] > 0) and (self.gradMean200[199] > self.gradMean200[lookBack])

    def isGradMean5Falling(self, lookBack = 5):
        return not self.isGradMean5Rising( lookBack )
    
    def isGradMean13Falling(self, lookBack = 13):
        return not self.isGradMean13Rising( lookBack ) 
    
    def isGradMean38Falling(self, lookBack = 38):
        return not self.isGradMean38Rising( lookBack )
    
    def isGradMean89Falling(self, lookBack = 88):
        return not self.isGradMean89Rising( lookBack )
    
    def isGradMean200Falling(self, lookBack = 200):
        return not self.isGradMean200Rising( lookBack )
                         
    def winRatio(self):
        checkCount = ((self.winCount + self.lossCount) > 0)
        if checkCount == True:
            ratio = (float(self.winCount) / float(self.winCount + self.lossCount))*100.0
            return ratio
        else:
            return 0.0
        
    def evaluateBuy(self, indexData):
        return False
                
    def evaluateSell(self, indexData):
        return False
    
    def calculateResult(self):
        pass
        
    def evaluateInvest(self, indexData):
        self.gradMean5.append(indexData.mean5)
        self.gradMean13.append(indexData.mean13)
        self.gradMean38.append(indexData.mean38)
        self.gradMean89.append(indexData.mean89)
        self.gradMean200.append(indexData.mean200)
        if self.state == 0:
            if self.evaluateBuy( indexData ) == True:
                self.buyValue = indexData.close
                self.state = 1
        else:
            if self.evaluateSell( indexData ) == True:
                self.sellValue = indexData.close
                self.calculateResult()
                self.state = 0
           
class EvaluateInvestStrategieCall( EvaluateInvestStrategie ):
    def __init__(self):
        EvaluateInvestStrategie.__init__(self)

    def calculateResult(self):
        checkWin = (self.sellValue > self.buyValue)
        if checkWin == True:
            self.winCount +=1
        else:
            self.lossCount +=1
            
    def evaluateBuyMean5(self, indexData):
        return (indexData.mean5 > 0) and (indexData.close > indexData.mean5)
    
    def evaluateBuyMean13(self, indexData):
        return (indexData.mean13 > 0) and (indexData.close > indexData.mean13)
    
    def evaluateBuyMean38(self, indexData):
        return (indexData.mean38 > 0) and (indexData.close > indexData.mean38)
    
    def evaluateBuyMean89(self, indexData):
        return (indexData.mean89 > 0) and (indexData.close > indexData.mean89)
    
    def evaluateBuyMean200(self, indexData):
        return (indexData.mean200 > 0) and (indexData.close > indexData.mean200)
    
    def evaluateSellMean5(self, indexData):
        return not self.evaluateBuyMean5( indexData )
    
    def evaluateSellMean13(self, indexData):
        return not self.evaluateBuyMean13(indexData)
    
    def evaluateSellMean38(self, indexData):
        return not self.evaluateBuyMean38(indexData)
    
    def evaluateSellMean89(self, indexData):
        return not self.evaluateBuyMean89(indexData)
    
    def evaluateSellMean200(self, indexData):
        return not self.evaluateBuyMean200(indexData)
            
class EvaluateInvestStrategiePut( EvaluateInvestStrategie ):
    def __init__(self):
        EvaluateInvestStrategie.__init__(self)

    def calculateResult(self):
        checkWin = (self.sellValue < self.buyValue)
        if checkWin == True:
            self.winCount +=1
        else:
            self.lossCount +=1

    def evaluateBuyMean5(self, indexData):
        return (indexData.mean5 > 0) and (indexData.close < indexData.mean5)
    
    def evaluateBuyMean13(self, indexData):
        return (indexData.mean13 > 0) and (indexData.close < indexData.mean13)
    
    def evaluateBuyMean38(self, indexData):
        return (indexData.mean38 > 0) and (indexData.close < indexData.mean38)
    
    def evaluateBuyMean89(self, indexData):
        return (indexData.mean89 > 0) and (indexData.close < indexData.mean89)
    
    def evaluateBuyMean200(self, indexData):
        return (indexData.mean200 > 0) and (indexData.close < indexData.mean200)
    
    def evaluateSellMean5(self, indexData):
        return not self.evaluateBuyMean5( indexData )
    
    def evaluateSellMean13(self, indexData):
        return not self.evaluateBuyMean13(indexData)
    
    def evaluateSellMean38(self, indexData):
        return not self.evaluateBuyMean38(indexData)
    
    def evaluateSellMean89(self, indexData):
        return not self.evaluateBuyMean89(indexData)
    
    def evaluateSellMean200(self, indexData):
        return not self.evaluateBuyMean200(indexData)
            
class EvaluateSimpleCall5( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False, lookBack = 5 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Call Mean5"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d]".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean5Rising( self.lookBack )
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean5Falling( self.lookBack )
        return checkSell
        
class EvaluateSimpleCall13( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 13 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Call Mean13"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
           
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean13Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean13Falling(self.lookBack)
        return checkSell    
    
class EvaluateSimpleCall38( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 38 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Call Mean38"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean38(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean38Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean38(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean38Falling(self.lookBack)
        return checkSell    

class EvaluateSimpleCall89( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Call Mean89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Falling(self.lookBack)
        return checkSell     
    
class EvaluateSimpleCall200( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Call Mean200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall5_13( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 13 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean5/13"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean13(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean13Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell or self.evaluateSellMean13(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean13Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall5_38( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 38 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean5/38"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean38(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean38Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell and self.evaluateSellMean38(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean38Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall5_89( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean5/89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell and self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Falling(self.lookBack)
        return checkSell
           
class EvaluateDoubleCall5_200( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean5/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall13_38( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 38 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean13/38"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean38(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean38Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        checkSell = checkSell or self.evaluateSellMean38(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean38Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall13_89( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean13/89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        checkSell = checkSell or self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall13_200( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean13/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall38_89( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean38/89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean38(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean38(indexData)
        checkSell = checkSell or self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall38_200( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean38/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean38(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean38(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Falling(self.lookBack)
        return checkSell

class EvaluateDoubleCall89_200( EvaluateInvestStrategieCall ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategieCall.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Call Mean89/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean89(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Rising(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean89(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Falling(self.lookBack)
        return checkSell
               
class EvaluateSimpleStrategieCall( EvaluateInvestStrategieCall ):
    
    def __init__(self):
        EvaluateInvestStrategieCall.__init__(self)
        self.name = "SimpleCall"
    
    def evaluateBuy(self, indexData ):
       
        checkBuy = (indexData.mean200 > 0)
        checkBuy = checkBuy and (indexData.close > indexData.mean13)
        checkBuy = checkBuy and (indexData.close > indexData.mean38)
        checkBuy = checkBuy and (indexData.close > indexData.mean89)
        checkBuy = checkBuy and (indexData.close > indexData.mean200)
        checkBuy = checkBuy and (indexData.mean13 > indexData.mean38)
        checkBuy = checkBuy and (indexData.mean38 > indexData.mean89)
        checkBuy = checkBuy and (indexData.mean89 > indexData.mean200) 
           
        return checkBuy
        
    def evaluateSell(self, indexData ):
        
        checkSell = (indexData.close < indexData.mean13)
        checkSell = checkSell or (indexData.close < indexData.mean38)
        checkSell = checkSell or (indexData.close < indexData.mean89)
        checkSell = checkSell or (indexData.close < indexData.mean200)
        checkSell = checkSell or (indexData.mean13 < indexData.mean38)
        checkSell = checkSell or (indexData.mean38 < indexData.mean89)
        checkSell = checkSell or (indexData.mean89 < indexData.mean200)
        
        return checkSell

class EvaluateSimplePut5( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False, lookBack = 5 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Put Mean5"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d]".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean5Falling( self.lookBack )
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean5Rising( self.lookBack )
        return checkSell
        
class EvaluateSimplePut13( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 13 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Put Mean13"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
           
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean13Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean13Rising(self.lookBack)
        return checkSell    
    
class EvaluateSimplePut38( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 38 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Put Mean38"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean38(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean38Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean38(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean38Rising(self.lookBack)
        return checkSell    

class EvaluateSimplePut89( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Put Mean89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Rising(self.lookBack)
        return checkSell     
    
class EvaluateSimplePut200( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Simple Put Mean200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut5_13( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 13 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean5/13"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean13(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean13Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell or self.evaluateSellMean13(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean13Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut5_38( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 38 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean5/38"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean38(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean38Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell and self.evaluateSellMean38(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean38Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut5_89( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean5/89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell and self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Rising(self.lookBack)
        return checkSell
           
class EvaluateDoublePut5_200( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean5/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean5(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean5(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut13_38( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 38 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean13/38"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean38(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean38Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        checkSell = checkSell or self.evaluateSellMean38(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean38Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut13_89( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean13/89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        checkSell = checkSell or self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut13_200( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean13/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean13(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean13(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut38_89( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 89 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean38/89"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean38(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean89(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean89Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean38(indexData)
        checkSell = checkSell or self.evaluateSellMean89(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean89Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut38_200( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean38/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean38(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean38(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Rising(self.lookBack)
        return checkSell

class EvaluateDoublePut89_200( EvaluateInvestStrategiePut ):
    def __init__(self, checkRisingMean = False, checkFallingMean = False,  lookBack = 200 ):
        EvaluateInvestStrategiePut.__init__(self)
        self.checkRisingMean = checkRisingMean
        self.checkFallingMean = checkFallingMean
        self.lookBack = lookBack
        self.name = "Double Put Mean89/200"
        if self.checkRisingMean == True:
            self.name = self.name + " + Rising Mean" + " {0:d}".format(self.lookBack)
        if self.checkFallingMean == True:
            self.name = self.name + " + Falling Mean" + " {0:d}".format(self.lookBack)
            
    def evaluateBuy(self, indexData):
        checkBuy = self.evaluateBuyMean89(indexData)
        checkBuy = checkBuy and self.evaluateBuyMean200(indexData)
        if self.checkRisingMean == True:
            checkBuy = checkBuy and self.isGradMean200Falling(self.lookBack)
        return checkBuy
    
    def evaluateSell(self, indexData):
        checkSell = self.evaluateSellMean89(indexData)
        checkSell = checkSell or self.evaluateSellMean200(indexData)
        if self.checkFallingMean == True:
            checkSell = checkSell or self.isGradMean200Rising(self.lookBack)
        return checkSell

class EvaluateSimpleStrategiePut( EvaluateInvestStrategiePut ):
    
    def __init__(self):
        EvaluateInvestStrategiePut.__init__(self)
        self.name = "SimplePut"
    
    def evaluateBuy(self, indexData ):
       
        checkBuy = (indexData.mean200 > 0)       
        checkBuy = checkBuy and (indexData.close < indexData.mean13)
        checkBuy = checkBuy and (indexData.close < indexData.mean38)
        checkBuy = checkBuy and (indexData.close < indexData.mean89)
        checkBuy = checkBuy and (indexData.close < indexData.mean200)
        checkBuy = checkBuy and (indexData.mean13 < indexData.mean38)
        checkBuy = checkBuy and (indexData.mean38 < indexData.mean89)
        checkBuy = checkBuy and (indexData.mean89 < indexData.mean200) 
           
        return checkBuy
        
    def evaluateSell(self, indexData ):
        
        checkSell = (indexData.close > indexData.mean13)
        checkSell = checkSell or (indexData.close > indexData.mean38)
        checkSell = checkSell or (indexData.close > indexData.mean89)
        checkSell = checkSell or (indexData.close > indexData.mean200)
        checkSell = checkSell or (indexData.mean13 > indexData.mean38)
        checkSell = checkSell or (indexData.mean38 > indexData.mean89)
        checkSell = checkSell or (indexData.mean89 > indexData.mean200)
        
        return checkSell