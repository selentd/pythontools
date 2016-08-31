'''
Created on 30.08.2016

@author: SELEN00R
'''

import datetime

import evalbase
import evalrunner
import fetchdata
import indexdata
import indexselector


class EvalBest(evalbase.EvalBase):

    maxDaysKey = "maxDays"
    maxWinKey  = "maxWin"
    maxLossKey = "maxLoss"
    maxJumpKey = "maxJump"
    maxHighJumpKey = "maxHighJump"

    def __init__(self, dbName, idxName, runParameters = None):
        evalbase.EvalBase.__init__(self, dbName, idxName, runParameters)

    def _isCurrentIndex(self, idxName, idxList):
        return( idxName == idxList[0][0] or
                idxName == idxList[1][0] or
                idxName == idxList[2][0] or
                idxName == idxList[3][0] or
                idxName == idxList[4][0] )

    def _createTransaction(self, idxName, startDate, endDate):
        fetchdata = fetchdata.FetchData( idxName )

        endEval = endDate + datetime.timedelta(1)
        idxBuy = fetchdata.fetchNextHistoryValue( startDate.year, startDate.month, startDate.day )
        idxSell = fetchdata.fetchNextHistoryValue( endEval.year, endEval.month, endEval.day )
        if idxBuy != None and idxSell != None:
            transaction = indexdata.TransactionResult()
            transaction.setResultHistory(idxBuy, idxSell, fetchdata.fetchDataByDate( startDate, endEval + datetime.timedelta(1)), False)
            transaction.indexName = idxName
            return transaction
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
            if not currentList.hasKey(idxList[0][0]):
                # --- best index is currently not active
                currentList[idxList[0][0]] = startEval

            if not currentList.hasKey(idxList[1][0]):
                # --- second best index is currently not active
                currentList[idxList[1][0]] = startEval

            if not currentList.hasKey(idxList[2][0]):
                # --- third best index is currently not active
                currentList[idxList[2][0]] = startEval

            # --- check if current entries are not worse than on 5th place
            for currentIdx in currentList:
                if not self._isCurrentIndex( currentIdx, idxList):
                    transactionList.addTransactionResult(self._createTransaction(currentIdx, currentList[currentIdx], startEval))
                    del currentList[currentIdx]

            startEval = startEval + datetime.timedelta( 1 )

        return transactionList

class EvalBestRunner(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _createIndexEvaluation(self, indexName):
        evaluation = EvalBest( self.dbName, indexName, self.runParameters )
        return evaluation

