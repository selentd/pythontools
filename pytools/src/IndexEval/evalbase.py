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
    knockOutKey = "knockOut"

    endTransactionCalcKey = "endTransactionCalc"

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
        self.knockOut = 0.0

        if runParameters == None:
            self.runParameters = dict()
        else:
            self.runParameters = runParameters
#            if self.runParameters.has_key(EvalBase.maxDaysKey):
            if EvalBase.maxDaysKey in self.runParameters:
                self.maxDays = self.runParameters[EvalBase.maxDaysKey]
#            if self.runParameters.has_key(EvalBase.maxWinKey):
            if EvalBase.maxWinKey in self.runParameters: 
                self.maxWin = self.runParameters[EvalBase.maxWinKey]
#            if self.runParameters.has_key(EvalBase.maxLossKey):
            if EvalBase.maxLossKey in self.runParameters:
                self.maxLoss = self.runParameters[EvalBase.maxLossKey]
#            if self.runParameters.has_key(EvalBase.maxJumpKey):
            if EvalBase.maxJumpKey in self.runParameters:
                self.maxJump = self.runParameters[EvalBase.maxJumpKey]
#            if self.runParameters.has_key(EvalBase.maxHighJumpKey):
            if EvalBase.maxHighJumpKey in self.runParameters:
                self.maxHighJump = self.runParameters[EvalBase.maxHighJumpKey]
#            if self.runParameters.has_key(EvalBase.knockOutKey):
            if EvalBase.knockOutKey in self.runParameters:
                self.knockOut = self.runParameters[EvalBase.knockOutKey]

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
        self.hasPostEndTransactionChecker = (self.maxDays > 0 
                                             or self.maxLoss != 0.0 
                                             or self.maxJump != 0.0 
                                             or self.maxWin != 0.0 
                                             or self.maxHighJump != 0.0
                                             or self.knockOut != 0.0)
        if self.hasPostEndTransactionChecker or self.runParameters.has_key(EvalBase.endTransactionCalcKey):
            self.hasPostEndTransactionChecker = True
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
                
            if self.knockOut != 0:
                checkerList.append( transactionchecker.EndTransactionCheckerKnockOut(self.knockOut))

#            if self.runParameters.has_key(EvalBase.endTransactionCalcKey):
            if EvalBase.endTransactionCalcKey in self.runParameters:
                checkerList.append( self.runParameters[EvalBase.endTransactionCalcKey])

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

            transactionResult.setResultHistory( idxBuy, idxSell, transactionHistory, self.knockOut )
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
