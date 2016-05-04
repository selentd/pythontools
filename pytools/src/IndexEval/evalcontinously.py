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

    maxDaysKey = "maxDays"
    maxWinKey  = "maxWin"
    maxLossKey = "maxLoss"
    maxJumpKey = "maxJump"

    def __init__(self, dbName, idxName, runParameters = None):
        self.dbName = dbName
        self.idxName = idxName
        if runParameters != None:
            self.runParameters = runParameters
            if self.runParameters.has_key(EvalContinously.maxDaysKey):
                self.maxDays = self.runParameters[EvalContinously.maxDaysKey]
            if self.runParameters.has_key(EvalContinously.maxWinKey):
                self.maxWin = self.runParameters[EvalContinously.maxWinKey]
            if self.runParameters.has_key(EvalContinously.maxLossKey):
                self.maxLoss = self.runParameters[EvalContinously.maxLossKey]
            if self.runParameters.has_key(EvalContinously.maxJumpKey):
                self.maxJump = self.runParameters[EvalContinously.maxJumpKey]
        else:
            self.runParameters = dict()
            self.maxDays = 0
            self.maxWin  = 0.0
            self.maxLoss = 0.0
            self.maxJump = 0.0

        self.hasPostEndTransactionChecker = (self.maxDays > 0 or self.maxLoss != 0.0 or self.maxJump != 0.0 or self.maxWin > 0.0)
        self.postEndTransactionChecker = transactionchecker.EndTransactionChecker()

    def loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.indexHistory = fetchdata.FetchData( self.idxName ).fetchDataByDate( self.startDate, self.endDate )

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

            if self.maxWin > 0:
                checkerList.append( transactionchecker.EndTransactionCheckerMaxWin(self.maxWin))

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

    isCallKey       = "isCall"
    meanKey         = "mean"
    mean2Key        = "mean2"
    mean3Key        = "mean3"
    mean4Key        = "mean4"
    mean5Key        = "mean5"
    gradKey         = "grad"
    grad2Key        = "grad2"
    grad3Key        = "grad3"
    minGradKey      = "minGrad"
    minGrad2Key     = "minGrad2"
    minGrad3Key     = "minGrad3"
    startOffsetKey  = "startOfset"
    endOffsetKey    = "endOffset"

    def __init__(self, dbName, idxName, runParameters = None):
        EvalContinously.__init__(self, dbName, idxName, runParameters)

        if self.runParameters.has_key( EvalContinouslyMean.isCallKey):
            self.isCall = self.runParameters[EvalContinouslyMean.isCallKey]
        else:
            self.isCall = True

        if self.runParameters.has_key( EvalContinouslyMean.meanKey):
            self.mean = self.runParameters[EvalContinouslyMean.meanKey]
        else:
            self.mean = 200

        if self.runParameters.has_key( EvalContinouslyMean.startOffsetKey):
            self.startOffset = self.runParameters[EvalContinouslyMean.startOffsetKey]
        else:
            self.startOffset = 0.0

        if self.runParameters.has_key( EvalContinouslyMean.endOffsetKey):
            self.endOffset = self.runParameters[EvalContinouslyMean.endOffsetKey]
        else:
            self.endOffset = 0.0

        if self.runParameters.has_key( EvalContinouslyMean.gradKey ):
            self.grad = self.runParameters[EvalContinouslyMean.gradKey]
        else:
            self.grad = 0.0

        if self.runParameters.has_key( EvalContinouslyMean.minGradKey):
            self.minGrad = self.runParameters[EvalContinouslyMean.minGradKey]
        else:
            self.minGrad = 0.0

        if self.runParameters.has_key( EvalContinouslyMean.grad2Key ):
            self.grad2 = self.runParameters[EvalContinouslyMean.grad2Key]
        else:
            self.grad2 = 0.0

        if self.runParameters.has_key( EvalContinouslyMean.minGrad2Key):
            self.minGrad2 = self.runParameters[EvalContinouslyMean.minGrad2Key]
        else:
            self.minGrad2 = 0.0

        if self.runParameters.has_key( EvalContinouslyMean.grad3Key ):
            self.grad3 = self.runParameters[EvalContinouslyMean.grad3Key]
        else:
            self.grad3 = 0.0

        if self.runParameters.has_key( EvalContinouslyMean.minGrad3Key):
            self.minGrad3 = self.runParameters[EvalContinouslyMean.minGrad3Key]
        else:
            self.minGrad3 = 0.0

    def _setupStartGradTransactionCheckers(self):
        if self.grad != 0.0:
            self.startTransactionChecker.addTransactionChecker(transactionchecker.StartTransactionCheckerGrad(self.grad, self.minGrad, self.isCall))

        if self.grad2 != 0.0:
            self.startTransactionChecker.addTransactionChecker(transactionchecker.StartTransactionCheckerGrad(self.grad2, self.minGrad2, self.isCall))

        if self.grad3 != 0.0:
            self.startTransactionChecker.addTransactionChecker(transactionchecker.StartTransactionCheckerGrad(self.grad3, self.minGrad3, self.isCall))

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionCheckerStrategie(
                                                                [transactionchecker.StartTransactionCheckerMean(self.mean, self.startOffset, self.isCall)] )

        self.endTransactionChecker = transactionchecker.EndTransactionCheckerMean( self.mean, self.endOffset, self.isCall )
        self._setupPostTransactionCheckers()

class EvalContinouslyMean2(EvalContinouslyMean):

    def __init__(self, dbName, idxName, runParameters = None):
        EvalContinouslyMean.__init__(self, dbName, idxName, runParameters)

        if self.runParameters.has_key(EvalContinouslyMean.mean2Key):
            self.mean2 = self.runParameters[EvalContinouslyMean.mean2Key]
        else:
            self.mean2 = self.mean

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionCheckerStrategie(
                                                                [transactionchecker.StartTransactionCheckerMean(self.mean, 0.0, self.isCall),
                                                                 transactionchecker.StartTransactionCheckerMean(self.mean2, 0.0, self.isCall)] )
        self._setupStartGradTransactionCheckers()
        self.endTransactionChecker = transactionchecker.EndTransactionCheckerMean( self.mean, self.endOffset, self.isCall )
        self._setupPostTransactionCheckers()

class EvalContinouslyMean3(EvalContinouslyMean):

    def __init__(self, dbName, idxName, runParameters = None):
        EvalContinouslyMean.__init__(self, dbName, idxName, runParameters)

        if self.runParameters.has_key(EvalContinouslyMean.mean2Key):
            self.mean2 = self.runParameters[EvalContinouslyMean.mean2Key]
        else:
            self.mean2 = self.mean

        if self.runParameters.has_key(EvalContinouslyMean.mean3Key):
            self.mean3 = self.runParameters[EvalContinouslyMean.mean3Key]
        else:
            self.mean3 = self.mean

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionCheckerStrategie(
                                                                        [transactionchecker.StartTransactionCheckerMean(self.mean, 0.0, self.isCall),
                                                                         transactionchecker.StartTransactionCheckerMean(self.mean2, 0.0, self.isCall),
                                                                         transactionchecker.StartTransactionCheckerMean(self.mean3, 0.0, self.isCall)] )
        self._setupStartGradTransactionCheckers()
        self.endTransactionChecker = transactionchecker.EndTransactionCheckerMean( self.mean, self.endOffset, self.isCall )
        self._setupPostTransactionCheckers()





