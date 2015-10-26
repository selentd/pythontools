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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()