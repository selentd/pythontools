
from resultdata import IndexResult

class EvalResult:
    def __init__(self, name, invest, knockOutLoss, leverage):
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
        self.leverage = leverage
        self.invest = invest
        self.knockOutLoss = knockOutLoss

    def getTotalCount(self):
        return (self.winCount + self.lossCount)

    def getWinRatio(self):
        if (self.getTotalCount() > 0):
            return (float(self.winCount)/float(self.getTotalCount()))*100.0
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
        winLoss = sell / buy
        winLoss -= 1.0
        return winLoss

    def getWinLossEuroCall(self, buy, sell):
        result = self.getWinLoss(buy, sell)
        result *= self.invest * self.leverage
        if (result < -self.knockOutLoss):
            result = -self.knockOutLoss
        return result

    def getWinLossEuroPut(self, buy, sell):
        result = self.getWinLoss(buy, sell)
        result *= self.invest * self.leverage
        if (result < -self.knockOutLoss):
            result = -self.knockOutLoss
        return result

    def evaluate(self, indexResult):
        pass

    def evaluateIndex(self, indexResultHistory):
        for indexResult in indexResultHistory:
            self.evaluate( indexResult )

class EvalResultCall( EvalResult ):
    def __init__(self, name, invest, knockOutLoss, leverage):
        EvalResult.__init__(self, name, invest, knockOutLoss, leverage)

    def evaluate(self, indexResult):
        result = self.getWinLoss( indexResult.indexBuy.close, indexResult.indexSell.close )
        resultEuro = self.getWinLossEuroCall(indexResult.indexBuy.close, indexResult.indexSell.close )
        if (indexResult.indexSell.close > indexResult.indexBuy.close):
            self.winCount += 1
            self.sumWin += result
            if (self.maxWin < result):
                self.maxWin = result

            self.sumWinEuro += resultEuro

        else:
            self.lossCount += 1
            self.sumLoss += result
            if (self.maxLoss > result):
                self.maxLoss = result

            self.sumLossEuro += resultEuro



class EvalResultPut( EvalResult ):
    def __init__(self, name, invest, knockOutLoss, leverage):
        EvalResult.__init__(self, name, invest, knockOutLoss, leverage)

    def evaluate(self, indexResult):
        result = self.getWinLoss( indexResult.indexSell.close, indexResult.indexBuy.close)
        resultEuro = self.getWinLossEuroPut( indexResult.indexSell.close, indexResult.indexBuy.close)
        if (indexResult.indexSell.close < indexResult.indexBuy.close):
            self.winCount += 1
            self.sumWin += result
            if (self.maxWin < result):
                self.maxWin = result

            self.sumWinEuro += resultEuro

        else:
            self.lossCount += 1
            self.sumLoss += result
            if (self.maxLoss > result):
                self.maxLoss = result

            self.sumLossEuro += resultEuro


