'''
Created on 11.05.2016

@author: selen00r
'''

import indexdata
import transactionchecker

class EvalBase:
    '''
    classdocs
    '''

    maxDaysKey = "maxDays"
    maxWinKey  = "maxWin"
    maxLossKey = "maxLoss"
    maxJumpKey = "maxJump"
    maxHighJumpKey = "maxHighJump"

    meanKey        = "mean"
    startOffsetKey = "startOffset"
    endOffsetKey   = "endOffset"

    def __init__(self, dbname, indexName, runParameters = None):
        '''
        Constructor
        '''
        self.dbname = dbname
        self.indexName = indexName

        self.maxDays = 0
        self.maxWin  = 0.0
        self.maxLoss = 0.0
        self.maxJump = 0.0
        self.maxHighJump = 0.0

        if runParameters == None:
            self.runParameters = dict()
        else:
            self.runParameters = runParameters
            if self.runParameters.has_key(EvalBase.maxDaysKey):
                self.maxDays = self.runParameters[EvalBase.maxDaysKey]
            if self.runParameters.has_key(EvalBase.maxWinKey):
                self.maxWin = self.runParameters[EvalBase.maxWinKey]
            if self.runParameters.has_key(EvalBase.maxLossKey):
                self.maxLoss = self.runParameters[EvalBase.maxLossKey]
            if self.runParameters.has_key(EvalBase.maxJumpKey):
                self.maxJump = self.runParameters[EvalBase.maxJumpKey]
            if self.runParameters.has_key(EvalBase.maxHighJumpKey):
                self.maxHighJump = self.runParameters[EvalBase.maxHighJumpKey]

        self.startHistoryChecker = transactionchecker.StartTransactionChecker()
        self.endHistoryChecker = transactionchecker.EndTransactionChecker()

        self.startTransactionChecker = transactionchecker.StartTransactionChecker()
        self.endTransactionChecker = transactionchecker.EndTransactionChecker()

        self.hasPostEndTransactionChecker = False
        self.postEndTransactionChecker = transactionchecker.EndTransactionChecker()

    def _setupHistoryCheckers(self):
        pass

    def _setupTransactionCheckers(self):
        pass

    def _setupPostTransactionCheckers(self):
        self.hasPostEndTransactionChecker = (self.maxDays > 0 or self.maxLoss != 0.0 or self.maxJump != 0.0 or self.maxWin > 0.0 or self.maxHighJump != 0.0)
        if self.hasPostEndTransactionChecker:
            checkerList = list()
            if self.maxDays > 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxDays(self.maxDays))

            if self.maxLoss != 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxLoss(self.maxLoss) )

            if self.maxJump != 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxJump( self.maxJump ))

            if self.maxWin != 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxWin(self.maxWin))

            if self.maxHighJump != 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxHighJump( self.maxHighJump ))

            self.postEndTransactionChecker = transactionchecker.EndTransactionCheckerStrategie( checkerList )


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

    def _loadIndexHistory(self, startDate, endDate ):
        pass

    def loadIndexHistory(self, startDate, endDate):
        self._setupHistoryCheckers()
        self._loadIndexHistory( startDate, endDate )

    def calculateResult(self):
        self._setupTransactionCheckers()
        self._setupPostTransactionCheckers()
        return self._calculateResult()
