'''
Created on 30.08.2016

@author: SELEN00R
'''

import datetime

import evalbase
import evalrunner
import fetchdata
import indexdata
import indexdatabase
import indexselector


class EvalBest(evalbase.EvalBase):

    maxDaysKey = "maxDays"
    maxWinKey  = "maxWin"
    maxLossKey = "maxLoss"
    maxJumpKey = "maxJump"
    maxHighJumpKey = "maxHighJump"
    
    idxListKey = "idxList"

    def __init__(self, dbName, idxName, runParameters = None):
        evalbase.EvalBase.__init__(self, dbName, idxName, runParameters)
        
        if runParameters.has_key(EvalBest.idxListKey):
            self.idxList = runParameters[EvalBest.idxListKey]
        else:
            self.idxList = indexdatabase.IndexDatabase.allIndices

    def _isCurrentIndex(self, idxName, idxList):
        return( idxName == idxList[0][0] or
                idxName == idxList[1][0] or
                idxName == idxList[2][0] or
                idxName == idxList[3][0] or
                idxName == idxList[4][0] )

    def _createTransaction(self, idxName, startDate, endDate):
        fetch = fetchdata.FetchData( idxName )

        idxBuy = fetch.fetchNextHistoryValue( startDate.year, startDate.month, startDate.day )
        idxSell = fetch.fetchNextHistoryValue( endDate.year, endDate.month, endDate.day )
        if idxBuy != None and idxSell != None:
            return self._endTransaction(idxBuy, idxSell, fetch.fetchDataByDate( startDate, endDate + datetime.timedelta(1)))
            #transaction = indexdata.TransactionResult()
            #transaction.setResultHistory(idxBuy, idxSell, fetch.fetchDataByDate( startDate, endDate + datetime.timedelta(1)), False)
            #transaction.indexName = idxName
        else:
            return None

    def _loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

    def _calculateResult(self):
        startEval = self.startDate
        selector = indexselector.IndexSelectorRSIAvgMonth([1, 3, 6, 12], True)
        currentList = dict()
        transactionList = indexdata.TransactionResultHistory()

        while startEval < self.endDate:
            idxList = selector.select( startEval, startEval + datetime.timedelta(1) )
            # --- check for new entries from 1st .. 3rd position
            if not currentList.has_key(idxList[0][0]):
                # --- best index is currently not active
                if idxList[0][1] > 0.0:
                    currentList[idxList[0][0]] = startEval

            if not currentList.has_key(idxList[1][0]):
                # --- second best index is currently not active
                if idxList[1][1] > 0.0:
                    currentList[idxList[1][0]] = startEval

            if not currentList.has_key(idxList[2][0]):
                # --- third best index is currently not active
                if idxList[2][1] > 0.0:
                    currentList[idxList[2][0]] = startEval

            # --- check if current entries are not worse than on 5th place
            removeList = list()
            for currentIdx in currentList:
                if not self._isCurrentIndex( currentIdx, idxList):
                    transaction = self._createTransaction(currentIdx, currentList[currentIdx], startEval)
                    if transaction != None:
                        transaction.indexName = currentIdx
                        transactionList.addTransactionResult(transaction)
                        
                    removeList.append( currentIdx )
            
            # --- remove items with transaction
            for item in removeList:
                del currentList[item]

            startEval = startEval + datetime.timedelta( 1 )

        return transactionList

class EvalBestRunner(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _createIndexEvaluation(self, indexName):
        self.runParameters[EvalBest.idxListKey] = self.indexList
        evaluation = EvalBest( self.dbName, indexName, self.runParameters )
        return evaluation

    def runEvaluation(self, descriptionStr, indexList=None):
        self.evaluationResultPrinter.printResultHead( descriptionStr )
        if indexList == None:
            indexList = self.allIndices
            
        self.indexList = indexList
        self.evaluateIndex('allIndices', descriptionStr)
        

    def runIndex(self, indexName, descriptionStr = "" ):
        self.runEvaluation(descriptionStr)
        
