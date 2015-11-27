'''
Created on 21.10.2015

@author: SELEN00R
'''

import datetime
import unittest


import evalresult
import fetchdata
import indexdata
from cookielib import offset_from_tz_string

class EvalMonthly:
    '''
    Check the result, if investment is done only on the last day of the month.
    '''

    def __init__(self, dbName, idxName):
        self.dbName = dbName
        self.idxName = idxName
        self.monthlyHistory= list()

    def loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.monthlyHistory = fetchdata.FetchData( self.dbName, self.idxName ).fetchMonthlyHistory(self.startDate, self.endDate)

    def calculateResult(self):
        return indexdata.TransactionResultHistory()

class EvalLastDay(EvalMonthly):

    def __init__(self, dbName, idxName):
        EvalMonthly.__init__(self, dbName, idxName)

    def _investOnLastDay(self, idxHistory):
        transaction = indexdata.TransactionResult()

        if idxHistory.len() > 1:
            idxBuy = idxHistory.getIndex( idxHistory.len() - 2 )
            idxSell = idxHistory.getLast()
            transaction.setResult(idxBuy, idxSell)

        return transaction

    def calculateResult(self):
        transactionList = indexdata.TransactionResultHistory()

        for idxHistory in self.monthlyHistory:
            transaction = self._investOnLastDay(idxHistory)
            if transaction.isValid():
                transactionList.addTransactionResult(transaction)

        return transactionList

class TransactionResultFirstDays(indexdata.TransactionResult):

    def __init__(self):
        indexdata.TransactionResult.__init__(self)

        self.lastDayResult = 0.0

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

    def __init__(self, useDays, dbName, idxName):
        EvalMonthly.__init__(self, dbName, idxName)
        self.useDays = useDays

    def _investOnFirstDays(self, lastHistory, idxHistory):
        transaction = TransactionResultFirstDays()

        if (lastHistory.len() > 0) and (idxHistory.len() > self.useDays):
            idxBuy = lastHistory.getLast()
            idxSell = idxHistory.getIndex(self.useDays - 1)
            transaction.setResult(idxBuy, idxSell)
            transaction.indexHistory.addIndexData(idxBuy)

            transaction.lastDayResult = lastHistory.getLast().close / lastHistory.getIndex( lastHistory.len() - 2).close
            transaction.lastDayResult -= 1.0

            for idx in range(0, self.useDays):
                transaction.indexHistory.addIndexData(idxHistory.getIndex(idx))


        return transaction

    def calculateResult(self):
        transactionList = indexdata.TransactionResultHistory()
        lastHistory = None
        for idxHistory in self.monthlyHistory:
            if lastHistory:
                transaction = self._investOnFirstDays(lastHistory, idxHistory)
                if transaction.isValid():
                    transactionList.addTransactionResult(transaction)

            lastHistory = idxHistory

        return transactionList

class EvalFirstDaysStopLoss(EvalFirstDays):

    def __init__(self, useDays, dbName, idxName):
        EvalFirstDays.__init__(self, useDays, dbName, idxName)
        self.stopLoss = -0.04
        self.jumpDiff = 0.04

    def _investOnFirstDaysWithStopLoss(self, lastHistory, idxHistory):
        transaction = TransactionResultFirstDays()

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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()