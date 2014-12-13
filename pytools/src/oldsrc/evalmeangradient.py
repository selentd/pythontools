
import collections
from evalindexdata import EvalIndexDataBuy
from evalindexdata import EvalIndexDataSell

class EvalMeanGradient():
    def __init__(self, gradientSize, lookBack, minGradient=0.0 ):
        self.gradientSize = gradientSize
        self.lookBack = lookBack
        if self.lookBack > self.gradientSize:
            self.lookBack = self.gradientSize
        self.lookBackIndex = self.gradientSize - lookBack
        self.gradientData = collections.deque( (0,0), self.gradientSize)
        self.minGradient = minGradient
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.close )
                
    def hasRisingMean(self):
        isRisingMean = False           
        if self.gradientData[0] > 0:
            isRisingMean = (self.gradientData[self.gradientSize-1] - self.gradientData[self.lookBackIndex]) > 0
            
        if isRisingMean and self.minGradient > 0.0:
            gradient = (self.gradientData[self.gradientSize-1] / self.gradientData[self.lookBackIndex])
            gradient -= 1.0
            gradient *= 100.0
            gradient /= self.lookBack
            isRisingMean = (gradient > self.minGradient)

        return isRisingMean
    
    def hasFallingMean(self):
        isFallingMean = False
        if self.gradientData[0] > 0:
            isFallingMean = (self.gradientData[self.gradientSize-1] - self.gradientData[self.lookBackIndex]) < 0

        if isFallingMean and self.minGradient > 0.0:
            gradient = (self.gradientData[self.lookBackIndex] / self.gradientData[self.gradientSize-1])
            gradient -= 1.0
            gradient *= 100.0
            gradient /= self.lookBack
            isFallingMean = (gradient > self.minGradient)
        
        return isFallingMean
    
class EvalMeanGradientCallBuy(EvalMeanGradient, EvalIndexDataBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def evaluateBuy(self, indexData):
        return EvalMeanGradient.hasRisingMean(self)    
    
class EvalMeanGradientCallSell(EvalMeanGradient, EvalIndexDataSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def evaluateSell(self, indexData):
        return self.hasFallingMean()

class EvalMeanGradientPutBuy(EvalMeanGradient, EvalIndexDataBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def evaluateBuy(self, indexData):
        return self.hasFallingMean()    
    
class EvalMeanGradientPutSell(EvalMeanGradient, EvalIndexDataSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def evaluateSell(self, indexData):
        return self.hasRisingMean()

class EvalMean5GradientCallBuy(EvalMeanGradientCallBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean5 )
    
class EvalMean5GradientCallSell(EvalMeanGradientCallSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean5 )
        
class EvalMean5GradientPutBuy(EvalMeanGradientPutBuy, EvalIndexDataBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean5 )
    
class EvalMean5GradientPutSell(EvalMeanGradientPutSell, EvalIndexDataSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean5 )

class EvalMean13GradientCallBuy(EvalMeanGradientCallBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean13 )
    
class EvalMean13GradientCallSell(EvalMeanGradientCallSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean13 )
        
class EvalMean13GradientPutBuy(EvalMeanGradientPutBuy, EvalIndexDataBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean13 )
    
class EvalMean13GradientPutSell(EvalMeanGradientPutSell, EvalIndexDataSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean13 )

class EvalMean38GradientCallBuy(EvalMeanGradientCallBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean38 )
    
class EvalMean38GradientCallSell(EvalMeanGradientCallSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean38 )
        
class EvalMean38GradientPutBuy(EvalMeanGradientPutBuy, EvalIndexDataBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean38 )
    
class EvalMean38GradientPutSell(EvalMeanGradientPutSell, EvalIndexDataSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean38 )

class EvalMean89GradientCallBuy(EvalMeanGradientCallBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean89 )
    
class EvalMean89GradientCallSell(EvalMeanGradientCallSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean89 )
        
class EvalMean89GradientPutBuy(EvalMeanGradientPutBuy, EvalIndexDataBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean89 )
    
class EvalMean89GradientPutSell(EvalMeanGradientPutSell, EvalIndexDataSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean89 )

class EvalMean200GradientCallBuy(EvalMeanGradientCallBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean200 )
    
class EvalMean200GradientCallSell(EvalMeanGradientCallSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )

    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean200 )
        
class EvalMean200GradientPutBuy(EvalMeanGradientPutBuy, EvalIndexDataBuy):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean200 )
    
class EvalMean200GradientPutSell(EvalMeanGradientPutSell, EvalIndexDataSell):
    def __init__(self, gradientSize, lookBack, minGradient=0.0):
        EvalMeanGradient.__init__( self, gradientSize, lookBack, minGradient )
        
    def updateState(self, indexData, lastBuy):
        self.gradientData.append( indexData.mean200 )
