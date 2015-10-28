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

    def exclude(self, idxData):
        return (idxData.close < idxData.mean200)

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

class ResultCalculatorEuro(ResultCalculator):
    '''
    Base class to calculate a transaction result in Euros
    '''
    def __init__(self, invest, fixInvest = True):
        ResultCalculator.__init__(self)

        self.invest = invest
        self.total = invest
        self.fixInvest = fixInvest

    def calcResult(self, buy, sell):
        result = ResultCalculator().calcResult(buy, sell)
        if self.fixInvest:
            result *= self.invest
        else:
            result *= self.total

        self.total += result
        if self.total < 0:
            self.total = 0

        return result

    def reset(self):
        self.total = self.invest

class ResultCalculatorEuroLeverage(ResultCalculatorEuro):
    def __init__(self, distance, invest, fixInvest = True):
        ResultCalculatorEuro.__init__(self, invest, fixInvest)
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
            result = self.total * percCalc

        self.total += result
        if self.total < 0:
            self.total = 0

        return result

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

    def evaluate(self, indexResult):
        pass

    def evaluateIndex(self, transactionResultHistory):
        for transactionResult in transactionResultHistory:
            self.evaluate( transactionResult )

class EvalResultCall( EvalResult ):
    def __init__(self, name, invest, fixInvest = True):
        EvalResult.__init__(self, name, invest, fixInvest)

    def evaluate(self, transactionResult):
        if not (self.checkExclude.exclude(transactionResult.indexBuy)):
            result = self.getWinLoss( transactionResult.indexBuy.close, transactionResult.indexSell.close )
            resultEuro = self.getWinLossEuro(transactionResult.indexBuy.close, transactionResult.indexSell.close )
            if (transactionResult.indexSell.close > transactionResult.indexBuy.close):
                self._updateWin(result, resultEuro)
            else:
                self._updateLoss(result, resultEuro)


class EvalResultPut( EvalResult ):
    def __init__(self, name, invest, fixInvest = True):
        EvalResult.__init__(self, name, invest, fixInvest)

    def evaluate(self, transactionResult):
        if not (self.checkExclude.exclude(transactionResult.indexBuy)):
            result = self.getWinLoss( transactionResult.indexSell.close, transactionResult.indexBuy.close)
            resultEuro = self.getWinLossEuro( transactionResult.indexSell.close, transactionResult.indexBuy.close)
            if (transactionResult.indexSell.close < transactionResult.indexBuy.close):
                self._updateWin(result, resultEuro)
            else:
                self._updateLoss(result, resultEuro)

