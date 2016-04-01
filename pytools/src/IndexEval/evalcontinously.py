'''
Created on 17.03.2016

@author: selen00r
'''

import datetime
import unittest


import evalresult
import fetchdata
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

class StartTransactionCheckerMean(StartTransactionChecker):

    def __init__(self, mean, isCall=True):
        self.mean = mean
        self.isCall = isCall

    def checkStartTransaction(self, idxData):
        startTransaction = False
        meanValue = idxData.getMeanValue( self.mean )
        if meanValue != 0:
            if self.isCall:
                startTransaction = (idxData.close > meanValue)
            else:
                startTransaction = (idxData.close < meanValue)

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
        self.maxHigh = idxBuy.high
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

class EndTransactionCheckerMean(EndTransactionChecker):

    def __init__(self, mean, isCall=True):
        EndTransactionChecker.__init__(self)
        self.mean = mean
        self.isCall = isCall

    def checkEndTransaction(self, idxData, idxHistoryLen):
        endTransaction = False
        meanValue = idxData.getMeanValue( self.mean )
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

    def _checkMaxWin(self, idxData):
        endTransaction = False

        result = (float(idxData.close) / float(self.idxBuy.close)) - 1.0
        if self.maxWin > 0.0:
            if result > self.maxWin:
                endTransaction = True

        if self.maxWin < 0.0:
            if result < self.maxWin:
                endTransaction = True

        return endTransaction

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
            result = (float(idxData.close) / float(self.maxLow)) - 1.0
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

class EvalContinously:
    '''
    classdocs
    '''

    def __init__(self, dbName, idxName):
        self.dbName = dbName
        self.idxName = idxName
        self.hasPostEndTransactionChecker = False
        self.postEndTransactionChecker = None

    def loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.indexHistory = fetchdata.FetchData( self.dbName, self.idxName ).fetchDataByDate( self.startDate, self.endDate )

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = StartTransactionChecker()
        self.endTransactionChecker = EndTransactionChecker()

    def _checkStartTransaction(self, idxData):
        return self.startTransactionChecker.checkStartTransaction(idxData)

    def _checkEndTransaction(self, idxData, indexHistoryLength):
        return self.endTransactionChecker.checkEndTransaction( idxData, indexHistoryLength )

    def _startTransaction(self, idxBuy):
        self.endTransactionChecker.reset( idxBuy )

    def _endTransaction(self, idxBuy, idxSell, idxHistory):
        transactionHistory = indexdata.IndexHistory()
        transactionResult = indexdata.TransactionResult()
        if self.hasPostEndTransactionChecker:
            self.postEndTransactionChecker.reset( idxBuy )
            for idxData in idxHistory.indexHistory:
                transactionHistory.addIndexData( idxData )
                if self.postEndTransactionChecker.checkEndTransaction( idxData, transactionHistory.len() ):
                    idxSell = idxData
                    break

            transactionResult.setResultHistory( idxBuy, idxSell, transactionHistory )
        else:
            transactionResult.setResultHistory( idxBuy, idxSell, idxHistory )
        return transactionResult

    def calculateResult(self):
        idxBuy = indexdata.IndexData()
        idxHistory = indexdata.IndexHistory()
        transactionList = indexdata.TransactionResultHistory()

        self._setupTransactionCheckers()
        isInTransaction = False

        for idxData in self.indexHistory.indexHistory:
            if isInTransaction:
                idxHistory.addIndexData( idxData )

                if self._checkEndTransaction( idxData, idxHistory.len() ):
                    transactionList.addTransactionResult( self._endTransaction( idxBuy, idxData, idxHistory ) )
                    isInTransaction = False

            if not isInTransaction:
                if self._checkStartTransaction( idxData ):
                    self._startTransaction( idxData )
                    isInTransaction = True
                    idxBuy = idxData
                    idxHistory = indexdata.IndexHistory()
                    idxHistory.addIndexData( idxData )

        return transactionList


class EvalContinouslyMean(EvalContinously):

    def __init__(self, dbName, idxName, mean, maxDays=0):
        EvalContinously.__init__(self, dbName, idxName)
        self.mean = mean
        self.maxDays = maxDays

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = StartTransactionCheckerMean( self.mean )
        self.endTransactionChecker = EndTransactionCheckerMean( self.mean )
        if self.maxDays > 0:
            self.hasPostEndTransactionChecker = True
            self.postEndTransactionChecker = EndTransactionCheckerMaxDays( self.maxDays)
        else:
            self.endTransactionChecker = EndTransactionCheckerMean( self.mean )

class EvalContinouslyMean2(EvalContinously):

    def __init__(self, dbName, idxName, mean1, mean2, maxDays=0):
        EvalContinously.__init__(self, dbName, idxName)
        self.mean1 = mean1
        self.mean2 = mean2
        self.maxDays = maxDays

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = StartTransactionCheckerStrategie( [StartTransactionCheckerMean(self.mean1),
                                                                          StartTransactionCheckerMean(self.mean2)] )
        self.endTransactionChecker = EndTransactionCheckerMean( self.mean1 )
        if self.maxDays > 0:
            self.hasPostEndTransactionChecker = True
            self.postEndTransactionChecker = EndTransactionCheckerStrategie( [ EndTransactionCheckerMaxDays( self.maxDays),
                                                                               EndTransactionCheckerMaxLoss( -0.04 ) ] )






