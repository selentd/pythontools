'''
Created on 21.10.2015

@author: SELEN00R
'''

import datetime
import unittest

import evalbase
import evalresult
import fetchdata
import indexdata
import transactionchecker

class EvalMonthly(evalbase.EvalBase):
    '''
    Check the result, if investment is done only on the last day of the month.
    '''

    def __init__(self, dbName, idxName, runParameters = None):
        evalbase.EvalBase.__init__(self, dbName, idxName, runParameters)

        self.mean = 0
        self.startOffset = 0.0
        self.endOffset = 0.0

        self.monthlyHistory= list()

    def _setupTransactionCheckers(self):
        if self.runParameters.has_key(evalbase.EvalBase.meanKey):
            self.mean = self.runParameters[evalbase.EvalBase.meanKey]

        if self.runParameters.has_key(evalbase.EvalBase.startOffsetKey):
            self.startOffset = self.runParameters[evalbase.EvalBase.startOffsetKey]

        if self.runParameters.has_key(evalbase.EvalBase.endOffsetKey):
            self.endOffset = self.runParameters[evalbase.EvalBase.endOffsetKey]

        if self.mean != 0:
            self.startTransactionChecker = transactionchecker.StartTransactionCheckerMean( self.mean, self.startOffset, True)
            self.endTransactionChecker = transactionchecker.EndTransactionCheckerMean( self.mean, self.endOffset, True )

    def _loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.monthlyHistory = fetchdata.FetchData( self.indexName ).fetchMonthlyHistory(self.startDate, self.endDate)

class EvalLastDay(EvalMonthly):

    def __init__(self, dbName, idxName, runParameters = None):
        EvalMonthly.__init__(self, dbName, idxName, runParameters)

    def _investOnLastDay(self, idxHistory):
        transaction = indexdata.TransactionResult()

        if idxHistory.len() > 1:
            idxBuy = idxHistory.getIndex( idxHistory.len() - 2 )
            idxSell = idxHistory.getLast()
            transaction.setResult(idxBuy, idxSell)

        return transaction

    def _calculateResult(self):
        transactionList = indexdata.TransactionResultHistory()

        for idxHistory in self.monthlyHistory:
            transaction = self._investOnLastDay(idxHistory)
            if transaction.isValid():
                transactionList.addTransactionResult(transaction)

        return transactionList

class ExcludeAvg200LowAndLastDayNegative(evalresult.ExcludeAvg200Low):

    def __init__(self, offset = 0.0):
        evalresult.ExcludeAvg200Low.__init__(self, offset)

    def exclude(self, transactionResult):
        checkExclude = evalresult.ExcludeAvg200Low.exclude(self, transactionResult)
        if not checkExclude:
            checkExclude = (transactionResult.lastDayResult < 0)

        return checkExclude

class ExcludeAvg200LowAndLastDayPositive(evalresult.ExcludeAvg200Low):
    def __init__(self, offset = 0.0):
        evalresult.ExcludeAvg200Low.__init__(self, offset)

    def exclude(self, transactionResult):
        checkExclude = evalresult.ExcludeAvg200Low.exclude(self, transactionResult)
        if not checkExclude:
            checkExclude = (transactionResult.lastDayResult > 0)

        return checkExclude

class EvalFirstDays(EvalMonthly):

    def __init__(self, dbName, idxName, runParameters = None):
        EvalMonthly.__init__(self, dbName, idxName, runParameters)

    def _investOnFirstDays(self, lastHistory, idxHistory):
        transaction = indexdata.TransactionResult()

        if (lastHistory.len() > 1) and (idxHistory.len() > self.maxDays):
            idxBuy = lastHistory.getLast()
            transaction.lastDayResult = lastHistory.getLast().close / lastHistory.getIndex( lastHistory.len() - 2).close
            transaction.lastDayResult -= 1.0

            if self._checkStartTransaction( idxBuy ):
                self._startTransaction( idxBuy )
                transactionHistory = indexdata.IndexHistory()
                transactionHistory.addIndexData( idxBuy )
                idxSell = indexdata.IndexData()

                if self.maxDays == 0:
                    idxRange = idxHistory.len() - 1
                else:
                    idxRange = self.maxDays

                for idx in range(0, idxRange):
                    idxSell = idxHistory.getIndex(idx)
                    transactionHistory.addIndexData( idxSell )
                    if self._checkEndTransaction( idxSell, transactionHistory.len() ):
                        break

                transaction = self._endTransaction( idxBuy, idxSell, transactionHistory )

        return transaction

    def _calculateResult(self):
        transactionList = indexdata.TransactionResultHistory()
        lastHistory = None

        for idxHistory in self.monthlyHistory:
            if lastHistory:
                transaction = self._investOnFirstDays(lastHistory, idxHistory)
                if transaction.isValid():
                    transactionList.addTransactionResult( transaction )

            lastHistory = idxHistory

        return transactionList

class EvalFirstDaysStopLoss(EvalFirstDays):

    def __init__(self, useDays, dbName, idxName):
        EvalFirstDays.__init__(self, useDays, dbName, idxName)
        self.stopLoss = -0.04
        self.jumpDiff = 0.04

    def _investOnFirstDaysWithStopLoss(self, lastHistory, idxHistory):
        transaction = indexdata.TransactionResultHistory()

        if (lastHistory.len() > 0) and (idxHistory.len() > self.useDays):
            idxBuy = lastHistory.getLast()
            transaction.indexHistory.addIndexData(idxBuy)

            transaction.lastDayResult = lastHistory.getLast().close / lastHistory.getIndex( lastHistory.len() - 2).close
            transaction.lastDayResult -= 1.0

            for idx in range(0, self.useDays):
                transaction.indexHistory.addIndexData(idxHistory.getIndex(idx))
                idxSell = idxHistory.getIndex(idx)
                currentResult = (idxSell.close / idxBuy.close)-1.0
                if currentResult < self.stopLoss:
                    break

                if idx == 0:
                    startResult = currentResult

                breakUp = False
                # --- check for jump result with low values!
                jumpResult = (idxSell.low / idxBuy.close)-1.0
                breakUp = ((startResult - jumpResult) > self.jumpDiff)
                # --- check for jump from last day result with low values!
                breakUp = breakUp or (transaction.lastDayResult - jumpResult) > self.jumpDiff
                # --- check for close below mean200
                breakUp = breakUp or (idxSell.close < idxSell.mean200)
                if breakUp:
                    break

            transaction.setResult(idxBuy, idxSell)

        return transaction

    def calculateResult(self):
        transactionList = indexdata.TransactionResultHistory()
        lastHistory = None
        for idxHistory in self.monthlyHistory:
            if lastHistory:
                transaction = self._investOnFirstDaysWithStopLoss(lastHistory, idxHistory)
                if transaction.isValid():
                    transactionList.addTransactionResult(transaction)

            lastHistory = idxHistory

        return transactionList

class EvalMonthlyInvest(EvalMonthly):

    def __init__(self, dbName, idxName):
        EvalMonthly.__init__(self, dbName, idxName, runParameters)

    def _investMonthly(self, lastHistory, idxHistory):
        transaction = TransactionResultFirstDays()

        if (lastHistory.len() > 0) and (idxHistory.len() > 0):
            idxBuy = lastHistory.getLast()
            idxSell = idxHistory.getLast()
            transaction.setResult(idxBuy, idxSell)
            transaction.indexHistory.addIndexData(idxBuy)

            transaction.lastDayResult = lastHistory.getLast().close / lastHistory.getIndex( lastHistory.len() - 2).close
            transaction.lastDayResult -= 1.0

            for idx in range(0, idxHistory.len()):
                transaction.indexHistory.addIndexData(idxHistory.getIndex(idx))

        return transaction

    def calculateResult(self):
        transactionList = indexdata.TransactionResultHistory()
        lastHistory = None
        for idxHistory in self.monthlyHistory:
            if lastHistory:
                transaction = self._investMonthly(lastHistory, idxHistory)
                if transaction.isValid():
                    transactionList.addTransactionResult(transaction)

            lastHistory = idxHistory

        return transactionList

class EvalMonthlyInvestWithStopLoss(EvalMonthlyInvest):

    def __init__(self, stopLoss, dbName, idxName):
        EvalMonthlyInvest.__init__(self, dbName, idxName)

        self.stopLoss = stopLoss
        self.mean200Level = 0.97

    def _checkBreakUp(self, currentResult, idxSell):
        # --- check for stop loss
        breakUp = (currentResult < self.stopLoss)
        # --- check for value < mean200
        breakUp = breakUp or (idxSell.close < (idxSell.mean200*self.mean200Level))
        return breakUp

    def _investMonthly(self, lastHistory, idxHistory):
        transaction = TransactionResultFirstDays()

        if (lastHistory.len() > 0) and (idxHistory.len() > 0):
            idxBuy = lastHistory.getLast()
            transaction.indexHistory.addIndexData(idxBuy)

            transaction.lastDayResult = lastHistory.getLast().close / lastHistory.getIndex( lastHistory.len() - 2).close
            transaction.lastDayResult -= 1.0

            for idx in range(0, idxHistory.len()):
                breakUp = False
                transaction.indexHistory.addIndexData(idxHistory.getIndex(idx))
                idxSell = idxHistory.getIndex(idx)
                currentResult = (idxSell.close / idxBuy.close)-1.0
                breakUp = self._checkBreakUp(currentResult, idxSell)
                if breakUp:
                    break

        transaction.setResult(idxBuy, idxSell)

        return transaction

class EvalMonthlyInvestWithStopLossAndMaxWin(EvalMonthlyInvestWithStopLoss):

    def __init__(self, maxWin, stopLoss, dbName, idxName):
        EvalMonthlyInvestWithStopLoss.__init__(self, stopLoss, dbName, idxName)

        self.maxWin = maxWin

    def _checkBreakUp(self, currentResult, idxSell):
        breakUp = EvalMonthlyInvestWithStopLoss._checkBreakUp(self, currentResult, idxSell)
        breakUp = breakUp or (currentResult > self.maxWin)
        return breakUp

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

