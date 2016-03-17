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

    def __init__(self):
        pass

    def checkStartTransaction(self, idxData):
        return False

class EndTransactionChecker:

    def __init__(self, maxLoss, maxWin, knockOutPerc, maxJumpPerc, maxDays):
        self.maxLoss = maxLoss
        self.maxWin = maxWin
        self.knockOutPerc = knockOutPerc
        self.maxJumpPerc = maxJumpPerc
        self.maxDays = maxDays
        self.idxBuy = indexdata.IndexData()

    def reset(self, idxBuy ):
        self.idxBuy = idxBuy
        self.maxClose = idxBuy.close
        self.maxHigh = idxBuy.high
        self.minClose = idxBuy.close
        self.minLow = idxBuy.close

    def _updateData(self, idxData, idxHistoryLen):

        if self.maxClose < idxData.close:
            self.maxClose = idxData.close

        if self.maxHigh < idxData.high:
            self.maxHigh = idxData.high

        if self.minClose > idxData.close:
            self.minClose = idxData.close

        if self.minLow > idxData.low:
            self.minLow = idxData.low

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

    def _checkMaxHistoryDays(self, historyLen):
        endTransaction = False

        if self.maxDays > 0:
            endTransaction = ((historyLen-1) > self.maxDays)

        return endTransaction

    def checkEndTransaction(self, idxData, idxHistoryLen):
        self._updateData( idxData, idxHistoryLen )

        endTranscation = self._checkMaxLoss( idxData )
        endTransaction = endTransaction or self._checkMaxWin( idxData )
        endTransaction = endTransaction or self._checkKnockOut( idxData )
        endTransaction = endTransaction or self._checkMaxJump( idxData )
        endTransaction = endTransaction or self._checkMaxHistoryDays( idxHistoryLen )

        return endTransaction



class EvalContinously:
    '''
    classdocs
    '''

    def __init__(self, dbName, idxName):
        self.dbName = dbName
        self.idxName = idxName

    def loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.indexHistory = fetchdata.FetchData( self.dbName, self.idxName ).fetchDataByDate( self.startDate, self.endDate )

    def _checkStartTransaction(self, idxData):
        return False

    def _checkEndTransaction(self, idxData):
        return True

    def _startTransaction(self, idxBuy):
        pass

    def _endTransaction(self, idxBuy, idxSell, idxHistory):
        return indexdata.TransactionResult().setResultHistory( idxBuy, idxSell, idxHistory )

    def calculateResult(self):
        idxBuy = indexdata.IndexData()
        idxHistory = indexdata.IndexHistory()
        transactionList = indexdata.TransactionResultHistory()

        isInTransaction = False

        for idxData in self.indexHistory:
            if isInTransaction:
                idxHistory.addIndexData( idxData )

                if self._checkEndTransaction( idxData ):
                    transactionList.addTransactionResult( self._endTransaction( idxBuy, idxData, idxHistory ) )
                    isInTransaction = False

            if not isInTransaction:
                if self._checkStartTransaction( idxData ):
                    self._startTransaction( idxData )
                    isInTransaction = True
                    idxBuy = idxData
                    idxHistory = indexdata.IndexHistory()

                    idxHistory.addIndexData( idxData )








