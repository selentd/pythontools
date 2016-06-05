'''
Created on 06.04.2016

@author: selen00r
'''

import indexdata

class StartTransactionChecker:

    def checkStartTransaction(self, idxData):
        return True

class StartTransactionCheckerStrategie(StartTransactionChecker):

    def __init__(self, checkerList, isAnd = True):
        self.checkerList = checkerList
        self.isAnd = isAnd

    def checkStartTransaction(self, idxData):
        startTransaction = self.isAnd
        for checker in self.checkerList:
            if self.isAnd:
                startTransaction = startTransaction and checker.checkStartTransaction( idxData )
            else:
                startTransaction = startTransaction or checker.checkStartTransaction( idxData )
        return startTransaction

    def addTransactionChecker(self, checker):
        self.checkerList.append( checker )

class StartTransactionCheckerMean(StartTransactionChecker):

    def __init__(self, mean, offset = 0.0, isCall=True):
        self.mean = mean
        self.offset = offset
        self.isCall = isCall

    def checkStartTransaction(self, idxData):
        startTransaction = False
        meanValue = idxData.getMeanValue( self.mean ) * (1.0 + self.offset)
        if meanValue != 0:
            if self.isCall:
                startTransaction = (idxData.close > meanValue)
            else:
                startTransaction = (idxData.close < meanValue)

        return startTransaction

class StartTransactionCheckerGrad(StartTransactionChecker):

    def __init__(self, grad, minGrad=0.0, isCall=True):
        self.grad = grad
        self.minGrad = minGrad
        self.isCall = isCall

    def checkStartTransaction(self, idxData):
        startTransaction = False
        gradValue = idxData.getGradValue( self.grad ) - self.minGrad
        if gradValue != 0.0:
            if self.isCall:
                startTransaction = (gradValue > 0.0)
            else:
                startTransaction = (gradValue < 0.0)
        return startTransaction

class EndTransactionChecker:

    def __init__(self):
        self.idxBuy = indexdata.IndexData()

    def _updateData(self, idxData, idxHistoryLen):

        if self.maxClose < idxData.close:
            self.maxClose = idxData.close

        if self.maxHigh < idxData.high:
            self.maxHigh = idxData.high

        if self.minClose > idxData.close:
            self.minClose = idxData.close

        if self.minLow > idxData.low:
            self.minLow = idxData.low

    def reset(self, idxBuy):
        self.idxBuy = idxBuy
        self.maxClose = idxBuy.close
        self.maxHigh = idxBuy.close
        self.minClose = idxBuy.close
        self.minLow = idxBuy.close

    def checkEndTransaction(self, idxData, idxHistoryLength):
        return False

class EndTransactionCheckerStrategie(EndTransactionChecker):

    def __init__(self, checkerList, isAnd = False):
        EndTransactionChecker.__init__(self)

        self.checkerList = checkerList
        self.isAnd = isAnd

    def _updateData(self, idxData, idxHistoryLen):
        for checker in self.checkerList:
            checker._updateData( idxData, idxHistoryLen)

    def reset(self, idxBuy):
        for checker in self.checkerList:
            checker.reset( idxBuy )

    def checkEndTransaction(self, idxData, idxHistoryLength):
        endTransaction = False
        for checker in self.checkerList:
            if self.isAnd:
                endTransaction = endTransaction and checker.checkEndTransaction( idxData, idxHistoryLength )
            else:
                endTransaction = endTransaction or checker.checkEndTransaction( idxData, idxHistoryLength )

        return endTransaction

    def addTransactionChecker(self, checker):
        self.checkerList.append( checker )

class EndTransactionCheckerMean(EndTransactionChecker):

    def __init__(self, mean, offset = 0.0, isCall=True):
        EndTransactionChecker.__init__(self)
        self.mean = mean
        self.offset = offset
        self.isCall = isCall

    def checkEndTransaction(self, idxData, idxHistoryLen):
        endTransaction = False
        meanValue = idxData.getMeanValue( self.mean ) * (1.0 + self.offset)
        if meanValue != 0:
            if self.isCall:
                endTransaction = (idxData.close < meanValue)
            else:
                endTransaction = (idxData.close > meanValue)

        return endTransaction

class EndTransactionCheckerMaxLoss(EndTransactionChecker):

    def __init__(self, maxLoss):
        EndTransactionChecker.__init__(self)
        self.maxLoss = maxLoss

    def _checkMaxLoss(self, idxData):
        endTransaction = False

        if idxData.date != self.idxBuy.date:
            result = (float(idxData.close) / float(self.idxBuy.close)) - 1.0
            if self.maxLoss > 0.0:
                if result > self.maxLoss:
                    endTransaction = True

            if self.maxLoss < 0.0:
                if result < self.maxLoss:
                    endTransaction = True

        return endTransaction

    def checkEndTransaction(self, idxData, idxHistoryLen):
        self._updateData(idxData, idxHistoryLen)
        return self._checkMaxLoss( idxData )

class EndTransactionCheckerMaxWin(EndTransactionChecker):

    def __init__(self, maxWin):
        EndTransactionChecker.__init__(self)
        self.maxWin = maxWin
        self.peakWin = 0.0

    def _checkMaxWin(self, idxData):
        endTransaction = False

        if idxData.date != self.idxBuy.date:
            if self.maxWin > 0.0:
                result = (float(idxData.close) / float(self.idxBuy.close)) - 1.0

                if (self.peakWin - result > self.maxWin):
                    endTransaction = True
            else:
                result = (float(idxData.close) / float(self.idxBuy.close)) -1.0

                if (self.peakWin - result < self.maxWin):
                    endTransaction = True
        else:
            self.peakWin = 0.0

        return endTransaction

    def _updateData(self, idxData, idxHistoryLen):
        EndTransactionChecker._updateData(self, idxData, idxHistoryLen)
        if self.maxWin > 0:
            maxResult = (self.maxHigh / self.idxBuy.close) - 1.0
            if maxResult > self.peakWin:
                self.peakWin = maxResult
        else:
            maxResult = (self.minLow / self.idxBuy.close) - 1.0
            if maxResult < self.peakWin:
                self.peakWin = maxResult

    def reset(self, idxBuy):
        EndTransactionChecker.reset(self, idxBuy)
        self.peakWin = 0.0

    def checkEndTransaction(self, idxData, idxHistoryLen):
        self._updateData(idxData, idxHistoryLen)
        return self._checkMaxWin(idxData)

class EndTransactionCheckerKnockOut(EndTransactionChecker):

    def __init__(self, knockOutPerc):
        EndTransactionChecker.__init__(self)
        self.knockOutPerc = knockOutPerc

    def _checkKnockOut(self, idxData):
        endTransaction = False

        if self.knockOutPerc > 0.0:
            result = (float(idxData.high) / float(self.idxBuy.close)) - 1.0
            if result > self.knockOutPerc:
                endTransaction = True

        if self.knockOutPerc < 0.0:
            result = (float(idxData.low) / float(self.idxBuy.close)) - 1.0
            if result < self.knockOutPerc:
                endTransaction = True

        return endTransaction

    def checkEndTransaction(self, idxData, idxHistoryLen):
        self._updateData(idxData, idxHistoryLen)
        return self._checkKnockOut(idxData)

class EndTransactionCheckerMaxJump(EndTransactionChecker):

    def __init__(self, maxJumpPerc):
        EndTransactionChecker.__init__(self)
        self.maxJumpPerc = maxJumpPerc

    def _checkMaxJump(self, idxData):
        endTransaction = False

        if self.maxJumpPerc > 0.0:
            result = (float(idxData.close) / float(self.minLow)) - 1.0
            if result > self.maxJumpPerc:
                endTransaction = True

        if self.maxJumpPerc < 0.0:
            result = (float(idxData.close) / float(self.maxHigh)) - 1.0
            if result < self.maxJumpPerc:
                endTransaction = True

        return endTransaction

    def checkEndTransaction(self, idxData, idxHistoryLen):
        self._updateData(idxData, idxHistoryLen)
        return self._checkMaxJump(idxData)

class EndTransactionCheckerMaxHighJump(EndTransactionChecker):

    def __init__(self, maxHighJumpPerc):
        EndTransactionChecker.__init__(self)
        self.maxHighJumpPerc = maxHighJumpPerc

    def _checkMaxHighJump(self, idxData):
        endTransaction = False

        if self.maxHighJumpPerc > 0.0:
            result = (float(idxData.close) / float(self.minClose)) - 1.0
            if result > self.maxHighJumpPerc:
                endTransaction = True

        if self.maxHighJumpPerc < 0.0:
            result = (float(idxData.close) / float(self.maxClose)) - 1.0
            if result < self.maxHighJumpPerc:
                endTransaction = True

        return endTransaction

    def checkEndTransaction(self, idxData, idxHistoryLen):
        self._updateData(idxData, idxHistoryLen)
        return self._checkMaxHighJump(idxData)

class EndTransactionCheckerMaxDays(EndTransactionChecker):

    def __init__(self, maxDays):
        EndTransactionChecker.__init__(self)
        self.maxDays = maxDays

    def _checkMaxHistoryDays(self, historyLen):
        endTransaction = False

        if self.maxDays > 0:
            endTransaction = ((historyLen-1) >= self.maxDays)

        return endTransaction

    def checkEndTransaction(self, idxData, idxHistoryLen):
        self._updateData(idxData, idxHistoryLen)
        return self._checkMaxHistoryDays(idxHistoryLen)

class EndTransactionCheckerGrad(EndTransactionChecker):

    def __init__(self, grad, minGrad=0.0, isCall=True):
        self.grad = grad
        self.minGrad = minGrad
        self.isCall = isCall

    def checkEndTransaction(self, idxData, idxHistoryLen):
        endTransaction = False
        gradValue = idxData.getGradValue( self.grad ) - self.minGrad
        if gradValue != 0.0:
            if self.isCall:
                endTransaction = (gradValue < 0.0)
            else:
                endTransaction = (gradValue > 0.0)
        return endTransaction
