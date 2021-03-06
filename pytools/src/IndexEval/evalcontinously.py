'''
Created on 17.03.2016

@author: selen00r
'''

import datetime

import evalbase
import evalrunner
import fetchdata
import indexdata

import transactionchecker

class EvalContinously(evalbase.EvalBase):
    '''
    classdocs
    '''

    maxDaysKey = "maxDays"
    maxWinKey  = "maxWin"
    maxLossKey = "maxLoss"
    maxJumpKey = "maxJump"
    maxHighJumpKey = "maxHighJump"

    def __init__(self, dbName, idxName, runParameters = None):
        evalbase.EvalBase.__init__(self, dbName, idxName, runParameters)

    def _loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.indexHistory = fetchdata.FetchData( self.indexName ).fetchDataByDate( self.startDate, self.endDate )

    def _calculateResult(self):
        idxBuy = indexdata.IndexData()
        idxHistory = indexdata.IndexHistory()
        transactionList = indexdata.TransactionResultHistory()

        isInTransaction = False

        for idxData in self.indexHistory.indexHistory:
        # --- check transaction
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

        if isInTransaction:
            transactionList.addTransactionResult(self._endTransaction(idxBuy, idxData, idxHistory))

        return transactionList


class EvalContinouslyMean(EvalContinously):

    isCallKey       = "isCall"
    meanKey         = "mean"
    mean2Key        = "mean2"
    mean3Key        = "mean3"
    mean4Key        = "mean4"
    mean5Key        = "mean5"
    endMeanKey      = "endMean"
    endMeanKey2     = "endMean2"
    endMeanKey3     = "endMean3"
    endMeanKey4     = "endMean4"
    endMeanKey5     = "endMean5"
    gradKey         = "grad"
    grad2Key        = "grad2"
    grad3Key        = "grad3"
    minGradKey      = "minGrad"
    minGrad2Key     = "minGrad2"
    minGrad3Key     = "minGrad3"
    startOffsetKey  = "startOffset"
    endOffsetKey    = "endOffset"
    startOffset2Key  = "startOffset2"
    endOffset2Key    = "endOffset2"
    startOffset3Key  = "startOffset3"
    endOffset3Key    = "endOffset3"

    def __init__(self, dbName, idxName, runParameters = None):
        EvalContinously.__init__(self, dbName, idxName, runParameters)

#        if self.runParameters.has_key( EvalContinouslyMean.isCallKey):
        if EvalContinouslyMean.isCallKey in self.runParameters:
            self.isCall = self.runParameters[EvalContinouslyMean.isCallKey]
        else:
            self.isCall = True

#        if self.runParameters.has_key( EvalContinouslyMean.meanKey):
        if EvalContinouslyMean.endMeanKey in self.runParameters:
            self.mean = self.runParameters[EvalContinouslyMean.meanKey]
        else:
            self.mean = 200

#        if self.runParameters.has_key(EvalContinouslyMean.mean2Key):
        if EvalContinouslyMean.mean2Key in self.runParameters:
            self.mean2 = self.runParameters[EvalContinouslyMean.mean2Key]
        else:
            self.mean2 = 0

#        if self.runParameters.has_key(EvalContinouslyMean.mean3Key):
        if EvalContinouslyMean.mean3Key in self.runParameters:
            self.mean3 = self.runParameters[EvalContinouslyMean.mean3Key]
        else:
            self.mean3 = 0

#        if self.runParameters.has_key(EvalContinouslyMean.endMeanKey):
        if EvalContinouslyMean.endMeanKey in self.runParameters:
            self.endMean = self.runParameters[EvalContinouslyMean.endMeanKey]
        else:
            self.endMean = self.mean

#        if self.runParameters.has_key(EvalContinouslyMean.endMeanKey2):
        if EvalContinouslyMean.endMeanKey2 in self.runParameters:
            self.endMean2 = self.runParameters[EvalContinouslyMean.endMeanKey2]
        else:
            self.endMean2 = 0

#        if self.runParameters.has_key(EvalContinouslyMean.endMeanKey3):
        if EvalContinouslyMean.endMeanKey3 in self.runParameters:
            self.endMean3 = self.runParameters[EvalContinouslyMean.endMeanKey3]
        else:
            self.endMean3 = 0

#        if self.runParameters.has_key( EvalContinouslyMean.gradKey ):
        if EvalContinouslyMean.gradKey in self.runParameters:
            self.grad = self.runParameters[EvalContinouslyMean.gradKey]
        else:
            self.grad = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.minGradKey):
        if EvalContinouslyMean.minGradKey in self.runParameters:
            self.minGrad = self.runParameters[EvalContinouslyMean.minGradKey]
        else:
            self.minGrad = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.grad2Key ):
        if EvalContinouslyMean.grad2Key in self.runParameters:
            self.grad2 = self.runParameters[EvalContinouslyMean.grad2Key]
        else:
            self.grad2 = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.minGrad2Key):
        if EvalContinouslyMean.minGrad2Key in self.runParameters:
            self.minGrad2 = self.runParameters[EvalContinouslyMean.minGrad2Key]
        else:
            self.minGrad2 = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.grad3Key ):
        if EvalContinouslyMean.grad3Key in self.runParameters:
            self.grad3 = self.runParameters[EvalContinouslyMean.grad3Key]
        else:
            self.grad3 = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.minGrad3Key):
        if EvalContinouslyMean.minGrad3Key in self.runParameters:
            self.minGrad3 = self.runParameters[EvalContinouslyMean.minGrad3Key]
        else:
            self.minGrad3 = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.startOffsetKey):
        if EvalContinouslyMean.startOffsetKey in self.runParameters:
            self.startOffset = self.runParameters[EvalContinouslyMean.startOffsetKey]
        else:
            self.startOffset = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.endOffsetKey):
        if EvalContinouslyMean.endOffsetKey in self.runParameters:
            self.endOffset = self.runParameters[EvalContinouslyMean.endOffsetKey]
        else:
            self.endOffset = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.startOffset2Key):
        if EvalContinouslyMean.startOffset2Key in self.runParameters:
            self.startOffset2 = self.runParameters[EvalContinouslyMean.startOffset2Key]
        else:
            self.startOffset2 = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.endOffset2Key):
        if EvalContinouslyMean.endOffset2Key in self.runParameters:
            self.endOffset = self.runParameters[EvalContinouslyMean.endOffset2Key]
        else:
            self.endOffset2 = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.startOffset3Key):
        if EvalContinouslyMean.startOffset3Key in self.runParameters:
            self.startOffset3 = self.runParameters[EvalContinouslyMean.startOffset3Key]
        else:
            self.startOffset3 = 0.0

#        if self.runParameters.has_key( EvalContinouslyMean.endOffset3Key):
        if EvalContinouslyMean.endOffset3Key in self.runParameters:
            self.endOffset = self.runParameters[EvalContinouslyMean.endOffset3Key]
        else:
            self.endOffset3 = 0.0

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

        if self.mean2 != 0:
            self.startTransactionChecker.addTransactionChecker(transactionchecker.StartTransactionCheckerMean(self.mean2, self.startOffset2, self.isCall))

        if self.mean3 != 0:
            self.startTransactionChecker.addTransactionChecker(transactionchecker.StartTransactionCheckerMean(self.mean3, self.startOffset3, self.isCall))

        self.endTransactionChecker = transactionchecker.EndTransactionCheckerStrategie(
                                                                [transactionchecker.EndTransactionCheckerMean( self.endMean, self.endOffset, self.isCall )] )
        
        if self.endMean2 != 0:
            self.endTransactionChecker.addTransactionChecker(transactionchecker.EndTransactionCheckerMean( self.endMean2, self.endOffset2, self.isCall))

        if self.endMean3 != 0:
            self.endTransactionChecker.addTransactionChecker(transactionchecker.EndTransactionCheckerMean( self.endMean3, self.endOffset3, self.isCall))

class EvalContinouslyGrad(EvalContinouslyMean):

    def __init__(self, dbName, idxName, runParameters = None):
        EvalContinouslyMean.__init__(self, dbName, idxName, runParameters)

    def _setupTransactionCheckers(self):
        self.startTransactionChecker = transactionchecker.StartTransactionCheckerStrategie(
                                                                [transactionchecker.StartTransactionCheckerGrad(self.grad, self.minGrad, self.isCall)])

        self.endTransactionChecker = transactionchecker.EndTransactionCheckerGrad( self.grad, -(self.minGrad), self.isCall)

class EvalContinouslyMeanRunner(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _createIndexEvaluation(self, indexName):
        evaluation = EvalContinouslyMean( self.dbName, indexName, self.runParameters )
        return evaluation

class EvalContinouslyGradRunner(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _createIndexEvaluation(self, indexName):
        evaluation = EvalContinouslyGrad( self.dbName, indexName, self.runParameters )
        return evaluation
