'''
Created on 21.10.2015

@author: SELEN00R
'''

import datetime
import unittest

import fetchdata
import indexdata

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

class EvalFirstDays(EvalMonthly):

    def __init__(self, useDays, dbName, idxName):
        EvalMonthly.__init__(self, dbName, idxName)
        self.useDays = useDays

    def _investOnFirstDays(self, lastHistory, idxHistory):
        transaction = indexdata.TransactionResult()

        if (lastHistory.len() > 0) and (idxHistory.len() > self.useDays):
            idxBuy = lastHistory.getLast()
            idxSell = idxHistory.getIndex(self.useDays - 1)
            transaction.setResult(idxBuy, idxSell)
            transaction.indexHistory.addIndexData(idxBuy)
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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()