'''
Created on 21.10.2015

@author: selen00r
'''

class ExcludeTransaction:
    '''
    Base class for strategies to exclude transactions while calculating results from the transaction history
    '''

    def exclude(self, idxData):
        return False

class ExcludeAvg200Low(ExcludeTransaction):

    def __init__(self, offset = 0.0):
        self.offset = offset

    def exclude(self, transactionResult):
        if transactionResult.indexBuy.mean200 > 0:
            checkValue = transactionResult.indexBuy.mean200 + (transactionResult.indexBuy.mean200 * self.offset)
            return (transactionResult.indexBuy.close < checkValue)
        else:
            return True

class TransactionResultPrinter:
    '''
    Base class for printing of transactions
    '''

    def printResult(self, transactionResult, result, resultEuro, hasResult = False ):
        pass

class ResultCalculator:
    '''
    Base class to calculate a transaction result
    '''
    def __init__(self):
        self.total = 0.0

    def calcResult(self, buy, sell):
        result = (float(sell)/float(buy))-1.0
        self.total += result
        return result

    def reset(self):
        self.total = 0

    def getTotal(self):
        return self.total

class ResultCalculatorPut(ResultCalculator):

    def __init__(self):
        ResultCalculator.__init__(self)

    def calcResult(self, buy, sell):
        return ResultCalculator.calcResult(self, buy, sell) * (-1.0)

class ResultCalculatorEuro(ResultCalculator):
    '''
    Base class to calculate a transaction result in Euros
    '''
    def __init__(self, invest, fixInvest = True, maxInvest = 0.0):
        ResultCalculator.__init__(self)

        self.invest = invest
        self.total = invest
        self.totalInvest = invest
        self.fixInvest = fixInvest
        self.maxInvest = maxInvest

    def _checkTotal(self):
        if self.total < 0:
            self.total = 0

        if self.total < self.invest:
            self.totalInvest = self.totalInvest +(self.invest - self.total)
            self.total = self.invest

    def calcResult(self, buy, sell):
        result = ResultCalculator().calcResult(buy, sell)
        if self.fixInvest:
            result *= self.invest
        else:
            result *= self.total

        self.total += result
        self._checkTotal()
        return result

    def reset(self):
        self.total = self.invest
        self.totalInvest = self.invest

    def getTotalInvest(self):
        return self.totalInvest

class ResultCalculatorEuroPut(ResultCalculatorEuro):

    def __init__(self, invest, fixInvest = True, maxInvest = 0.0):
        ResultCalculatorEuro.__init__(self, invest, fixInvest, maxInvest)

    def calcResult(self, buy, sell):
        return ResultCalculatorEuro.calcResult(self, buy, sell, knockOut) * (-1.0)

class ResultCalculatorEuroLeverage(ResultCalculatorEuro):
    def __init__(self, distance, invest, fixInvest = True, maxInvest = 0.0):
        ResultCalculatorEuro.__init__(self, invest, fixInvest, maxInvest)
        self.distance = distance
        self.k = 1.1302864364
        self.d = 0.2029128054

    def calcResult(self, buy, sell):
        result = ResultCalculator().calcResult(buy, sell)

        startCalc = (self.k * (self.distance)) + self.d
        actCalc = (self.k * ((self.distance) + (result*100.0))) + self.d
        percCalc = (actCalc / startCalc)-1

        if self.fixInvest:
            result = self.invest * percCalc
        else:
            newInvest = self.total
            if newInvest < self.invest:
                newInvest = self.invest

            if (self.maxInvest > 0.0) and (newInvest > self.maxInvest):
                result = (self.maxInvest) * percCalc
            else:
                result = newInvest * percCalc

        self.total += result
        self._checkTotal()

        return result

class ResultCalculatorEuroLeveragePut(ResultCalculatorEuroLeverage):
    def __init__(self, distance, invest, fixInvest = True, maxInvest = 0.0):
        ResultCalculatorEuroLeverage.__init__(self, distance, invest, fixInvest, maxInvest)

    def calcResult(self, buy, sell):
        return ResultCalculatorEuroLeverage.calcResult(self, buy, sell) * (-1.0)

class EvalResult:
    '''
    Base class for transaction result evaluation
    '''
    def __init__(self, name, invest, fixInvest = True):
        self.name = name
        self.winCount = 0
        self.lossCount = 0
        self.knockOutCount = 0
        self.maxWin = 0.0
        self.maxLoss = 0.0
        self.sumWin = 0.0
        self.sumLoss = 0.0
        self.maxWinEuro = 0.0
        self.maxLossEuro = 0.0
        self.sumWinEuro = 0.0
        self.sumLossEuro = 0.0
        self.invest = invest
        self.fixInvest = fixInvest
        self.checkExclude = ExcludeTransaction()
        self.resultCalculator = ResultCalculator()
        self.resultCalculatorEuro = ResultCalculatorEuro( self.invest, self.fixInvest )

    def _updateWin(self, result, resultEuro):
        self.winCount += 1
        self.sumWin += result
        if (self.maxWin < result):
            self.maxWin = result

        if (self.maxWinEuro < resultEuro):
            self.maxWinEuro = resultEuro

        self.sumWinEuro += resultEuro

    def _updateLoss(self, result, resultEuro):
        self.lossCount += 1
        self.sumLoss += result
        if (self.maxLoss > result):
            self.maxLoss = result

        if (self.maxLossEuro > resultEuro):
            self.maxLossEuro = resultEuro

        self.sumLossEuro += resultEuro

    def setExcludeChecker(self, checkExclude):
        self.checkExclude = checkExclude

    def setResultCalculator(self, calculator):
        self.resultCalculator = calculator

    def setResultCalculatorEuro(self, calculator):
        self.resultCalculatorEuro = calculator

    def getTotalCount(self):
        return (self.winCount + self.lossCount)

    def getTotalResult(self):
        return self.resultCalculator.getTotal()

    def getTotalResultEuro(self):
        return self.resultCalculatorEuro.getTotal()

    def getTotalInvestEuro(self):
        return self.resultCalculatorEuro.getTotalInvest()

    def getWinRatio(self):
        if (self.getTotalCount() > 0):
            return (float(self.winCount)/float(self.getTotalCount()))
        else:
            return 0.0

    def getMeanWin(self):
        if (self.winCount > 0):
            return (self.sumWin / float(self.winCount))
        else:
            return 0

    def getMeanLoss(self):
        if (self.lossCount > 0):
            return (self.sumLoss / float(self.lossCount))
        else:
            return 0

    def getWinLoss(self, buy, sell):
        return self.resultCalculator.calcResult(buy, sell)

    def getWinLossEuro(self, buy, sell):
        return self.resultCalculatorEuro.calcResult(buy, sell)

    def evaluateIndex(self, transactionResultHistory, resultPrinter = None ):
        for transactionResult in transactionResultHistory:
            self.evaluate( transactionResult, resultPrinter )

    def _updateResult(self, transactionResult, result, resultEuro ):
        if result < 0.0:
            self._updateLoss(result, resultEuro)
        else:
            self._updateWin(result, resultEuro)

    def evaluate(self, transactionResult, resultPrinter = None):
        hasResult = False
        result = 0.0
        resultEuro = 0.0
        if not (self.checkExclude.exclude(transactionResult)):
            indexSell = transactionResult.indexSell.close
            
            if transactionResult.knockOut != 0.0:
                indexKnockOut = transactionResult.indexBuy.close + (transactionResult.indexBuy.close * transactionResult.knockOut)
                if transactionResult.knockOut < 0:
                    if transactionResult.getLowValue() < indexKnockOut:
                        indexSell = indexKnockOut
                else:
                    if transactionResult.getHighValue() > indexKnockOut:
                        indexSell = indexKnockOut
                
            result = self.getWinLoss( transactionResult.indexBuy.close, indexSell)
            resultEuro = self.getWinLossEuro(transactionResult.indexBuy.close, indexSell)
            self._updateResult( transactionResult, result, resultEuro)
            hasResult = True

            if resultPrinter:
                resultPrinter.printResult( transactionResult, result, resultEuro, hasResult )

