'''
Created on 17.03.2016

@author: selen00r
'''

import datetime

import evalresult
import fetchdata
import indexdata


import transactionchecker


class EvalContinously:
    '''
    classdocs
    '''

    def __init__(self, dbName, idxName, maxDays=0, maxLoss = 0.0, maxJump = 0.0):
        self.dbName = dbName
        self.idxName = idxName
        self.maxDays = maxDays
        self.maxLoss = maxLoss
        self.maxJump = maxJump
        self.hasPostEndTransactionChecker = (self.maxDays > 0 or self.maxLoss != 0.0 or self.maxJump != 0.0)
        self.postEndTransactionChecker = transactionchecker.EndTransactionChecker()

    def loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.indexHistory = fetchdata.FetchData( self.dbName, self.idxName ).fetchDataByDate( self.startDate, self.endDate )

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionChecker()
        self.endTransactionChecker = transactionchecker.EndTransactionChecker()

    def _setupPostTransactionCheckers(self):
        if self.hasPostEndTransactionChecker:
            checkerList = list()
            if self.maxDays > 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxDays(self.maxDays))

            if self.maxLoss != 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxLoss(self.maxLoss) )

            if self.maxJump != 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxJump( self.maxJump ))

            self.postEndTransactionChecker = transactionchecker.EndTransactionCheckerStrategie( checkerList )
        else:
            self.postEndTransactionChecker = transactionchecker.EndTransactionChecker()

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

    def __init__(self, dbName, idxName, mean, offset = 0.0, maxDays=0, maxLoss = 0.0, maxJump = 0.0):
        EvalContinously.__init__(self, dbName, idxName, maxDays, maxLoss, maxJump)
        self.mean = mean
        self.offset = offset


    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionCheckerMean( self.mean, self.offset )
        self.endTransactionChecker = transactionchecker.EndTransactionCheckerMean( self.mean )
        self._setupPostTransactionCheckers()

class EvalContinouslyMean2(EvalContinously):

    def __init__(self, dbName, idxName, mean1, mean2, maxDays=0, maxLoss = 0.0, maxJump = 0.0):
        EvalContinously.__init__(self, dbName, idxName, maxDays, maxLoss, maxJump)
        self.mean1 = mean1
        self.mean2 = mean2

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionCheckerStrategie(
                                                                [transactionchecker.StartTransactionCheckerMean(self.mean1),
                                                                 transactionchecker.StartTransactionCheckerMean(self.mean2)] )
        self.endTransactionChecker = transactionchecker.EndTransactionCheckerMean( self.mean1 )
        self._setupPostTransactionCheckers()

class EvalContinouslyMean3(EvalContinously):

    def __init__(self, dbName, idxName, mean1, mean2, mean3, maxDays=0, maxLoss = 0.0, maxJump = 0.0):
        EvalContinously.__init__(self, dbName, idxName, maxDays, maxLoss, maxJump)
        self.mean1 = mean1
        self.mean2 = mean2
        self.mean3 = mean3
        self.maxDays = maxDays
        self.maxLoss = maxLoss
        self.maxJump = maxJump
        self.hasPostEndTransactionChecker = (self.maxDays > 0 or self.maxLoss != 0.0 or self.maxJump != 0.0)

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionCheckerStrategie(
                                                                        [transactionchecker.StartTransactionCheckerMean(self.mean1),
                                                                         transactionchecker.StartTransactionCheckerMean(self.mean2),
                                                                         transactionchecker.StartTransactionCheckerMean(self.mean3)] )
        self.endTransactionChecker = transactionchecker.EndTransactionCheckerMean( self.mean1 )
        self._setupPostTransactionCheckers()





