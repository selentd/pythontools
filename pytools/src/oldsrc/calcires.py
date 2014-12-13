'''
Created on 13.06.2013

@author: selen00r
'''

import csv
import collections
import datetime
import string

class EvalData:
    def __init__(self, name, meanName):
        self.state = 0
        self.buy = 0.0
        self.initialBuy = 0.0
        self.sell = 0.0
        self.total = 0.0
        self.buyCount = 0
        self.sellCount = 0
        self.minTotal = 0.0
        self.maxTotal = 0.0
        self.winCount = 0
        self.lossCount = 0
        self.totalLossCount = 0
        self.maxLossCall = 0.95
        self.maxLossCallAbsolute = 0.98
        self.maxLossPut = 1.05
        self.maxLossPutAbsolute = 1.01
        self.leverageCall = 45
        self.leveragePut = 55
        self.dayBefore = 0.0
        self.name = name
        self.meanName = meanName
        self.minInvest = 1000
        self.maxInvestLeverageCall = 1
        self.maxInvestLeveragePut = 1
        self.maxLossLimitCall = 1.0
        self.maxLossLimitPut = 1.0
        self.minReserve = 10000
        
        self.mean5Gradient = collections.deque((0,0,0,0,0), 5)
        self.mean13Gradient = collections.deque((0,0,0,0,0,0,0,0,0,0,0,0,0), 13)
        self.mean38Gradient = collections.deque((0,0,0,0,0,0,0,0,0,0,0,0,0), 38)
        self.mean89Gradient = collections.deque((0,0,0,0,0,0,0,0,0,0,0,0,0), 89)     
        self.mean200Gradient = collections.deque((0,0,0,0,0), 200)
        
        self.closeHistory = collections.deque((0,0,0,0,0), 5)
        
    def updateMinMax(self):
        if self.total < self.minTotal:
            self.minTotal = self.total
            
        if self.total > self.maxTotal:
            self.maxTotal = self.total
            
        if self.buy < self.sell:
            self.winCount = self.winCount + 1
        else:
            self.lossCount = self.lossCount + 1
            
    def calcSimpleCallTotal(self):
        self.total = self.total + self.sell - self.buy
        self.updateMinMax()
        
    def calcInvestCallTotal(self):
        invest = self.minInvest
        if self.total > (self.minReserve + self.minInvest):
            invest = self.total - self.minReserve
        if self.total > self.minInvest * self.maxInvestLeverageCall:
            invest = self.minInvest * self.maxInvestLeverageCall
            
        result = self.sell / self.buy
        result = result - 1
        result = result * invest
        result = result * self.leverageCall
        if result < (invest*(-1))*self.maxLossLimitCall:
            result = (invest*(-1))*self.maxLossLimitCall
            self.totalLossCount += 1
            
        self.total = self.total + result - 15.8
        self.updateMinMax()

    def calcInvestPutTotal(self):
        invest = self.minInvest       
        if self.total > (self.minReserve + self.minInvest):
            invest = self.total - self.minReserve
        if self.total > self.minInvest * self.maxInvestLeveragePut:
            invest = self.minInvest * self.maxInvestLeveragePut
        
        result = self.buy / self.sell
        result = result - 1
        result = result * invest
        result = result * self.leveragePut
        if result < (invest*(-1))*self.maxLossLimitPut:
            result = (invest*(-1))*self.maxLossLimitPut
            self.totalLossCount += 1            
            
        self.total = self.total + result - 15.8
        self.updateMinMax()
         
    def evalSingleCall(self, value, limit, mean):
        if mean > 0:
            if self.state == 0:
                if value > mean:
                    self.state = 1
                    self.buy = value
                    self.buyCount = self.buyCount + 1
                    self.dayBefore = value
            else:
                #if (value < limit) or (value < self.buy*self.maxLossCall):
                #if (value < self.buy*self.maxLossCall):
                if (value < self.dayBefore*self.maxLossCall):
                    self.state = 0
                    self.sell = value
                    #self.calcSimpleTotal()
                    self.calcInvestCallTotal()
                    self.sellCount = self.sellCount + 1
                else:
                    if (self.dayBefore < value):                 
                        self.dayBefore = value
            
    def evalDoubleCall(self, value, limit, mean1, mean2):
        if mean1 > 0 and mean2 > 0:
            if self.state == 0:
                if value > mean1 and value > mean2 and mean1 > mean2:
                    self.state = 1
                    self.buy = value
                    self.buyCount = self.buyCount + 1
                    self.dayBefore = value
            else:
                #if (value < limit) or (value < self.buy*self.maxLossCall):
                #if (value < mean1 or value < mean2 or mean1 < mean2) or (value < self.buy*self.maxLossCall):
                #if (value < self.buy*self.maxLossCall):
                if (value < self.dayBefore*self.maxLossCall):
                    self.state = 0
                    self.sell = value
                    #self.calcSimpleTotal()
                    self.calcInvestCallTotal()
                    self.sellCount = self.sellCount + 1
                else:
                    if (self.dayBefore < value): 
                        self.dayBefore = value               
            
    def evalTripleCall(self, value, limit, mean1, mean2, mean3):
        if mean1 > 0 and mean2 > 0 and mean3 > 0:
            if self.state == 0:
                if value > mean1 and value > mean2 and value > mean3 and mean1 > mean2 > mean3:
                    self.state = 1
                    self.buy = value
                    self.buyCount = self.buyCount + 1
                    self.dayBefore = value
            else:
                #if (value < mean1 or value < mean2 or value < mean3 or mean1 < mean2 < mean3) or (value < self.buy*self.maxLossCall):
                #if (value < self.buy*self.maxLossCall):
                #if (value < limit) or (value < self.buy*self.maxLossCall):
                if (value < self.dayBefore*self.maxLossCall):
                    self.state = 0
                    self.sell = value
                    #self.calcSimpleTotal()
                    self.calcInvestCallTotal()
                    self.sellCount = self.sellCount + 1
                else:
                    if (self.dayBefore < value): 
                        self.dayBefore = value

    def evalSinglePut(self, value, limit, mean):
        if mean > 0:
            if self.state == 0:
                if value < mean:
                    self.state = 1
                    self.buy = value
                    self.buyCount = self.buyCount + 1
                    self.dayBefore = value
            else:
                #if (value > mean) or (value > self.buy*self.maxLossPut) or (value > self.dayBefore):
                #if (value > mean) or (value > self.buy*self.maxLossPut):
                #if (value > limit) or (value < self.buy*self.maxLossPut):
                if (value > self.dayBefore*self.maxLossPut):                    
                    self.state = 0
                    self.sell = value
                    #self.calcSimpleTotal()
                    self.calcInvestPutTotal()
                    self.sellCount = self.sellCount + 1
                else:
                    if (self.dayBefore > value): 
                        self.dayBefore = value
            
    def evalDoublePut(self, value, limit, mean1, mean2):
        if mean1 > 0 and mean2 > 0:
            if self.state == 0:
                if value < mean1 and value < mean2 and mean1 < mean2:
                    self.state = 1
                    self.buy = value
                    self.buyCount = self.buyCount + 1
                    self.dayBefore = value
            else:
                #if (value > mean1 and value > mean2 and mean1 > mean2) or (value > self.buy*self.maxLossPut) or (value > self.dayBefore):
                #if (value > mean1 or value > mean2 or mean1 > mean2) or (value > self.buy*self.maxLossPut):
                #if (value > limit) or (value < self.buy*self.maxLossCall):
                if (value > self.dayBefore*self.maxLossPut):
                    self.state = 0
                    self.sell = value
                    #self.calcSimpleTotal()
                    self.calcInvestPutTotal()
                    self.sellCount = self.sellCount + 1
                else:
                    if (self.dayBefore > value): 
                        self.dayBefore = value                
            
    def evalTriplePut(self, value, limit, mean1, mean2, mean3):
        if mean1 > 0 and mean2 > 0 and mean3 > 0:
            if self.state == 0:
                if value < mean1 and value < mean2 and value < mean3 and mean1 < mean2 < mean3:
                    self.state = 1
                    self.buy = value
                    self.buyCount = self.buyCount + 1
                    self.dayBefore = value
            else:
                #if (value > mean1 and value > mean2 and value > mean3 and mean1 > mean2 > mean3) or (value > self.buy*self.maxLossPut)  or (value > self.dayBefore):
                #if (value > mean1 or value > mean2 or value > mean3 or mean1 > mean2 > mean3) or (value > self.buy*self.maxLossPut):
                #if (value > limit) or (value < self.buy*self.maxLossCall):
                if (value > self.dayBefore*self.maxLossPut):
                    self.state = 0
                    self.sell = value
                    #self.calcSimpleTotal()
                    self.calcInvestPutTotal()
                    self.sellCount = self.sellCount + 1
                else:
                    if (self.dayBefore > value): 
                        self.dayBefore = value   
                        
    def evalSpecialCall(self, indexData):
        if indexData.mean5 > 0 and indexData.mean13 > 0 and indexData.mean38 > 0:
            self.mean5Gradient.append(indexData.mean5)
            self.mean13Gradient.append(indexData.mean13)
            self.mean38Gradient.append(indexData.mean38)
            self.mean89Gradient.append(indexData.mean89)
            self.mean200Gradient.append(indexData.mean200)
            self.closeHistory.append(indexData.close)
            
            if self.state == 0:
                #checkMean = (indexData.close > indexData.mean13) and (indexData.close > indexData.mean38) and (indexData.close > indexData.mean200)
                #checkMean = (indexData.close > indexData.mean200)
                checkMean = (indexData.close > indexData.mean38) and (indexData.close > indexData.mean89)
                checkValue = True
                checkGradient = False
                
                #if self.sell > 0:
                #    checkValue = (indexData.close > self.sell)
                    
                if self.mean89Gradient[0] > 0:
                    checkGradient = (self.mean13Gradient[12] > self.mean13Gradient[0]) #and (self.mean89Gradient[88] > self.mean89Gradient[0])                      
                         
                checkBuy = checkMean and checkGradient
                if checkBuy == True:
                    self.state = 1
                    self.buy = indexData.close
                    self.initialBuy = indexData.close
                    self.buyCount += 1
                    self.dayBefore = indexData.close
            else:                   
                checkSell = (indexData.close < self.initialBuy*self.maxLossCallAbsolute) or (indexData.close < self.dayBefore*self.maxLossCall)                
                #if (self.dayBefore / self.buy) > 1.01:
            
                if (self.dayBefore / self.initialBuy) > 1.02:
                    checkSell = checkSell or (indexData.close < self.initialBuy)
                #if (self.dayBefore / self.buy) > 1.05:
                #    checkSell = checkSell or ((indexData.close / self.buy) < 1.03)
                    
                if checkSell == True:
                    self.state = 0
                    self.sell = indexData.close
                    self.calcInvestCallTotal()
                    self.sellCount += 1
                else:
                    if (indexData.close / self.buy) > 1.02:
                        self.sell = indexData.close
                        self.calcInvestCallTotal()
                        self.buy = self.sell
                        
                    if (indexData.close / self.buy) < 0.98:
                        self.sell = indexData.close
                        self.calcInvestCallTotal()
                        self.buy = self.sell
                                                
                    if (self.dayBefore < indexData.close):
                        self.dayBefore = indexData.close

    def evalSpecialPut(self, indexData):
        if indexData.mean5 > 0 and indexData.mean13 > 0 and indexData.mean38 > 0:
            self.mean5Gradient.append(indexData.mean5)
            self.mean13Gradient.append(indexData.mean13)
            self.mean38Gradient.append(indexData.mean38)
            self.mean89Gradient.append(indexData.mean89)
            self.mean200Gradient.append(indexData.mean200)
            self.closeHistory.append(indexData.close)
            
            if self.state == 0:
                #checkMean = (indexData.close > indexData.mean13) and (indexData.close > indexData.mean38) and (indexData.close > indexData.mean200)
                #checkMean = (indexData.close > indexData.mean200)
                checkMean = (indexData.close < indexData.mean38) and (indexData.close < indexData.mean89)
                checkValue = True
                checkGradient = False
                
                #if self.sell > 0:
                #    checkValue = (indexData.close < self.sell)
                    
                if self.mean89Gradient[0] > 0:
                    checkGradient = (self.mean13Gradient[12] < self.mean13Gradient[0]) and (self.mean89Gradient[88] < self.mean89Gradient[0])                        
                         
                checkBuy = checkMean and checkGradient
                if checkBuy == True:
                    self.state = 1
                    self.buy = indexData.close
                    self.buyCount += 1
                    self.dayBefore = indexData.close
            else:
                checkSell = (indexData.close > self.initialBuy*self.maxLossPutAbsolute) or (indexData.close > self.dayBefore*self.maxLossPut)
                
                if (self.initialBuy / self.dayBefore) > 1.01:
                    checkSell = checkSell or (indexData.close > self.initialBuy)
                    
                if checkSell == True:
                    self.state = 0
                    self.sell = indexData.close
                    self.calcInvestPutTotal()
                    self.sellCount += 1
                else:
                    if (self.buy / indexData.close) > 1.02:
                        self.sell = indexData.close
                        self.calcInvestCallTotal()
                        self.buy = self.sell
                        
                    if (self.buy / indexData.close) < 0.98:
                        self.sell = indexData.close
                        self.calcInvestCallTotal()
                        self.buy = self.sell
                    
                    if (self.dayBefore > indexData.close):
                        self.dayBefore = indexData.close
        

class IndexEvaluation:
    def __init__(self, filename):
        self.filename = filename
        self.dataSet = collections.deque()
        self.callSet = collections.deque()
        self.putSet = collections.deque()
        
    def readIndexData(self):
        meanSet = MeanSet()

        with open(self.filename, "rb") as iFile:
            csvReader = csv.DictReader(iFile, ['Date', 'Open', 'High', 'Low', 'Close'])
            for row in csvReader:
                current = IndexData()
                currentDate = string.split(row['Date'], '.')            
                current.set( datetime.date(int(currentDate[2]), int(currentDate[1]), int(currentDate[0])),
                             float(row['Open']),
                             float(row['Close']),
                             float(row['High']),
                             float(row['Low']) )
                self.dataSet.append( current )
                if len(self.dataSet) > (260*10):
                    break
                
        self.dataSet.reverse()
        for idxData in self.dataSet:
            meanSet.setData(idxData.close)
            idxData.setMean(meanSet)
            
    def readIndexDataShort(self):
        meanSet = MeanSet()

        with open(self.filename, "rb") as iFile:
            csvReader = csv.DictReader(iFile, ['Date', 'Close'])
            for row in csvReader:
                current = IndexData()
                currentDate = string.split(row['Date'], '.')            
                current.set( datetime.date(int(currentDate[2]), int(currentDate[1]), int(currentDate[0])),
                             0.0,
                             float(row['Close']),
                             0.0,
                             0.0 )
                self.dataSet.append( current )
                
        self.dataSet.reverse()
        for idxData in self.dataSet:
            meanSet.setData(idxData.close)
            idxData.setMean(meanSet)
        
        
                
    def evaluateData5(self):
        evalCall = EvalData( self.filename + " Call", "M(5)" )
        evalPut = EvalData( self.filename + " Put", "M(5)" )
        for idxData in self.dataSet:
            evalCall.evalSingleCall( idxData.close, idxData.mean13, idxData.mean5 )
            evalPut.evalSinglePut(idxData.close, idxData.mean13, idxData.mean5)
            
        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
        
    def evaluateData5_13(self):
        evalCall = EvalData( self.filename + " Call", "M(5 13)" )
        evalPut = EvalData( self.filename + " Put", "M(5 13)" )
        for idxData in self.dataSet:
            evalCall.evalDoubleCall( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean13 )
            evalPut.evalDoublePut( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean13 )
            
        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
            
        
    def evaluateData5_38(self):
        evalCall = EvalData( self.filename + " Call", "M(5 38)" )
        evalPut = EvalData( self.filename + " Put", "M(5 38)" )
        for idxData in self.dataSet:
            evalCall.evalDoubleCall( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean38 )
            evalPut.evalDoublePut( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean38 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)

    def evaluateData5_200(self):
        evalCall = EvalData( self.filename + " Call", "M(5 200)" )
        evalPut = EvalData( self.filename + " Put", "M(5 200)" )
        for idxData in self.dataSet:
            evalCall.evalDoubleCall( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean200 )
            evalPut.evalDoublePut( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean200 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
        
    def evaluateData5_13_38(self):
        evalCall = EvalData( self.filename + " Call", "M(5 13 38)" )
        evalPut = EvalData( self.filename + " Put", "M(5 13 38)" )
        for idxData in self.dataSet:
            evalCall.evalTripleCall( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean13, idxData.mean38 )
            evalPut.evalTriplePut( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean13, idxData.mean38 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)

    def evaluateData5_13_200(self):
        evalCall = EvalData( self.filename + " Call", "M(5 13 200)" )
        evalPut = EvalData( self.filename + " Put", "M(5 13 200)" )
        for idxData in self.dataSet:
            evalCall.evalTripleCall( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean13, idxData.mean200 )
            evalPut.evalTriplePut( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean13, idxData.mean200 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
        
    def evaluateData5_38_200(self):
        evalCall = EvalData( self.filename + " Call", "M(5 38 200)" )
        evalPut = EvalData( self.filename + " Put", "M(5 38 200)" )
        for idxData in self.dataSet:
            evalCall.evalTripleCall( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean38, idxData.mean200 )
            evalPut.evalTriplePut( idxData.close,  idxData.mean13, idxData.mean5, idxData.mean38, idxData.mean200 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
            
    def evaluateData13(self):
        evalCall = EvalData( self.filename + " Call", "M(13)" )
        evalPut = EvalData( self.filename + " Put", "M(13)" )
        for idxData in self.dataSet:
            evalCall.evalSingleCall( idxData.close,  idxData.mean13, idxData.mean13 )
            evalPut.evalSinglePut( idxData.close,  idxData.mean13, idxData.mean13 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
            
    def evaluateData13_38(self):
        evalCall = EvalData( self.filename + " Call", "M(13 38)" )
        evalPut = EvalData( self.filename + " Put", "M(13 38)" )
        for idxData in self.dataSet:
            evalCall.evalDoubleCall( idxData.close,  idxData.mean13, idxData.mean13, idxData.mean38 )
            evalPut.evalDoublePut( idxData.close,  idxData.mean13, idxData.mean13, idxData.mean38 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)

    def evaluateData13_200(self):
        evalCall = EvalData( self.filename + " Call", "M(13 200)" )
        evalPut = EvalData( self.filename + " Put", "M(13 200)" )
        for idxData in self.dataSet:
            evalCall.evalDoubleCall( idxData.close,  idxData.mean13, idxData.mean13, idxData.mean200 )
            evalPut.evalDoublePut( idxData.close,  idxData.mean13, idxData.mean13, idxData.mean200 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
            
    def evaluateData13_38_200(self):
        evalCall = EvalData( self.filename + " Call", "M(13 38 200)" )
        evalPut = EvalData( self.filename + " Put", "M(13 38 200)" )
        for idxData in self.dataSet:
            evalCall.evalTripleCall( idxData.close,  idxData.mean13, idxData.mean13, idxData.mean38, idxData.mean200 )
            evalPut.evalTriplePut( idxData.close,  idxData.mean13, idxData.mean13, idxData.mean38, idxData.mean200 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
        
    def evaluateData38(self):
        evalCall = EvalData( self.filename + " Call", "M(38)" )
        evalPut = EvalData( self.filename + " Put", "M(38)" )
        for idxData in self.dataSet:
            evalCall.evalSingleCall( idxData.close,  idxData.mean13, idxData.mean38 )
            evalPut.evalSinglePut( idxData.close,  idxData.mean13, idxData.mean38 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
        
    def evaluateData38_200(self):
        evalCall = EvalData( self.filename + " Call", "M(38_200)" )
        evalPut = EvalData( self.filename + " Put", "M(38_200)" )
        for idxData in self.dataSet:
            evalCall.evalDoubleCall( idxData.close,  idxData.mean13, idxData.mean38, idxData.mean200 )
            evalPut.evalDoublePut( idxData.close,  idxData.mean13, idxData.mean38, idxData.mean200 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)
        
    def evaluateData200(self):
        evalCall = EvalData( self.filename + " Call", "M(200)" )
        evalPut = EvalData( self.filename + " Put", "M(200)" )
        for idxData in self.dataSet:
            evalCall.evalSingleCall( idxData.close,  idxData.mean13, idxData.mean200 )
            evalPut.evalSinglePut( idxData.close,  idxData.mean13, idxData.mean200 )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)

    def evaluateDataSpecial(self):
        evalCall = EvalData( self.filename + " Call", "Special" )
        evalPut = EvalData( self.filename + " Put", "Special" )
        for idxData in self.dataSet:
            evalCall.evalSpecialCall( idxData )
            evalPut.evalSpecialPut( idxData )

        self.callSet.append(evalCall)
        self.putSet.append(evalPut)        
        
    def calculateData(self):
        self.evaluateData5()
        self.evaluateData5_13()
        self.evaluateData5_38()
        self.evaluateData5_200()
        self.evaluateData5_13_38()
        self.evaluateData5_13_200()
        self.evaluateData5_38_200()
        self.evaluateData13()
        self.evaluateData13_38()
        self.evaluateData13_200()
        self.evaluateData13_38_200()
        self.evaluateData38()
        self.evaluateData38_200()
        self.evaluateData200()
        
    def showData(self, call, put):
        if call == 1:
            for evalData in self.callSet:
                print evalData.name, ",", evalData.total, ",", evalData.minTotal, ",", evalData.maxTotal, ",", evalData.buyCount, ",", evalData.winCount, ",", evalData.lossCount, ",", evalData.totalLossCount
                
        if put == 1:
            for evalData in self.putSet:
                print evalData.name, ",", evalData.total, ",", evalData.minTotal, ",", evalData.maxTotal, ",", evalData.buyCount, ",", evalData.lossCount, ",", evalData.winCount, ",", evalData.totalLossCount
                
    def exportData(self, filename, call, put ):
        with open(filename, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            csvWrite.writerow( ('File', 'Mean', 'Total', 'minTotal', 'maxTotal', 'buyCount', 'winCount', 'lossCount') )
            if call == 1:
                for evalData in self.callSet:                    
                    csvWrite.writerow( (evalData.name,
                                        evalData.meanName,
                                        evalData.total, 
                                        evalData.minTotal,
                                        evalData.maxTotal,
                                        evalData.buyCount,
                                        evalData.winCount,
                                        evalData.lossCount,
                                        len(self.dataSet)) )
                    
            if put == 1:
                for evalData in self.putSet:
                    csvWrite.writerow( (evalData.name,
                                        evalData.meanName,
                                        evalData.total, 
                                        evalData.minTotal,
                                        evalData.maxTotal,
                                        evalData.buyCount,
                                        evalData.lossCount,
                                        evalData.winCount,
                                        len(self.dataSet)) )
            
    def exportSpecial(self, filename, call, put ):
        with open(filename, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            #csvWrite.writerow( ('File', 'Mean', 'Total', 'minTotal', 'maxTotal', 'buyCount', 'winCount', 'lossCount') )
            if call == 1:
                for evalData in self.callSet:                    
                    csvWrite.writerow( (evalData.name,
                                        evalData.meanName,
                                        evalData.total, 
                                        evalData.minTotal,
                                        evalData.maxTotal,
                                        evalData.buyCount,
                                        evalData.winCount,
                                        evalData.lossCount,
                                        len(self.dataSet)) )
                    
            if put == 1:
                for evalData in self.putSet:
                    csvWrite.writerow( (evalData.name,
                                        evalData.meanName,
                                        evalData.total, 
                                        evalData.minTotal,
                                        evalData.maxTotal,
                                        evalData.buyCount,
                                        evalData.lossCount,
                                        evalData.winCount,
                                        len(self.dataSet)) )
        
                                               
def evaluateIndex( source, destination, short ):
    index = IndexEvaluation( source )

    print "reading", source
    if short == 0:    
        index.readIndexData()
    else:
        index.readIndexDataShort()
        
    print "calculating", source
    index.calculateData()
    
    print "writing", destination
    index.exportData( destination, 1, 0)
    index.exportData( destination, 0, 1)
    
def evaluateAllIndizes():
    evaluateIndex( "20120928_EUR_USD.csv", "res_20120928_EUR_USD.csv", 1 )
    evaluateIndex( '20130822_DAX.csv', 'res_20130822_DAX.csv', 0)
    evaluateIndex( 'estoxx50.csv', 'res_estoxx50.csv', 0)
    evaluateIndex( 'sp500.csv', 'res_sp500.csv', 0)
    evaluateIndex("smi.csv", "res_smi.csv", 0)
    evaluateIndex("nikkei225.csv", "res_nikkei225.csv", 0)
    evaluateIndex( "20130822_MDAX.csv", "res_20130822_MDAX.csv", 0 )    
        
def evaluateIndexSpecial( source ):
    index = IndexEvaluation( source)
    #print "reading"
    index.readIndexData()
    #print "calculating"
    index.evaluateDataSpecial()
    index.showData(1, 0)
    index.showData(0, 1)
    #index.exportData("specialresult.csv", 1, 0)
    #index.exportData("specialresult.csv", 0, 1)
            
def evaluateAllIndizesSpecial():
    #evaluateIndex( "20120928_EUR_USD.csv" )
    evaluateIndexSpecial( '20130822_DAX.csv')
    evaluateIndexSpecial( 'estoxx50.csv')
    evaluateIndexSpecial( 'sp500.csv')
    evaluateIndexSpecial("smi.csv")
    evaluateIndexSpecial("nikkei225.csv")
    evaluateIndexSpecial( "20130822_MDAX.csv")   
    #evaluateIndexSpecial( "ftse100.csv") 
                
if __name__ == '__main__':
    evaluateAllIndizesSpecial()