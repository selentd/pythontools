'''
Created on 04.11.2015

@author: selen00r
'''

import datetime

from pymongo.mongo_client import MongoClient

import evalresult

class EvalResultPrinter:

    def printResult(self, indexName, descriptionStr, resultEvaluation):
        pass

class EvalResultPrinterSimple:

    def printResult(self, indexName, descriptionStr, resultEvaluation):
        print str.format( '{:10} {:15} {:>4} {:>4} {:>4} {:>6.2f} {: 6.3f} {:>6.3f} {:>10.2f}',
                          indexName,
                          descriptionStr,
                          resultEvaluation.getTotalCount(),
                          resultEvaluation.winCount,
                          resultEvaluation.lossCount,
                          resultEvaluation.getWinRatio(),
                          resultEvaluation.maxLoss,
                          resultEvaluation.getTotalResult(),
                          resultEvaluation.getTotalResultEuro() )


class EvalRunner(object):
    '''
    Base class to run an evaluation of an index.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.dbName = "stockdb"

        self.idxATX         = "atx"
        self.idxCAC         = "cac"
        self.idxDax         = "dax"
        self.idxDowJones    = "dowjones"
        self.idxEStoxx50    = "estoxx50"
        self.idxFTS100      = "ftse100"
        self.idxFtseMib     = "ftsemib"
        self.idxHangSeng    = "hangseng"
        self.idxIbex        = "ibex"
        self.idxMDax        = "mdax"
        self.idxNasdaq100   = "nasdaq100"
        self.idxNikkei      = "nikkei"
        self.idxSDax        = "sdax"
        self.idxSMI         = "smi"
        self.idxSP500       = "sp500"
        self.idxTecDax      = "tecdax"

        self.allIndices = [self.idxATX, self.idxCAC, self.idxDax, self.idxDowJones, self.idxEStoxx50,
                           self.idxFTS100, self.idxFtseMib, self.idxHangSeng, self.idxIbex, self.idxMDax,
                           self.idxNasdaq100, self.idxNikkei, self.idxSDax, self.idxSMI, self.idxTecDax]

        self.mongoClient = MongoClient()
        self.database = self.mongoClient[self.dbName]

    def _setupStartEndTime(self):
        self.startDate = datetime.datetime( 2000, 1, 1 )
        self.endDate = datetime.datetime( 2016, 1, 1 )

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = True
        self.resultCalculator = evalresult.ResultCalculator()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)

    def _setupResultExcludeChecker(self):
        self.excludeChecker = evalresult.ExcludeTransaction()

    def _setupTransactionPrinter(self):
        self.resultTransactionPrinter = evalresult.TransactionResultPrinter()

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = EvalResultPrinter()

    def setUp(self):
        self._setupStartEndTime()
        self._setupResultCalculator()
        self._setupResultExcludeChecker()
        self._setupTransactionPrinter()
        self._setupEvalResultPrinter()

    def tearDown(self):
        pass

    def _createResultEvaluation(self, indexName, descriptionStr):
        self.resultCalculator.reset()
        self.resultCalculatorEuro.reset()

        resultEvaluation = evalresult.EvalResultCall( indexName + " " + descriptionStr, self.startInvest, self.fixedInvest )
        resultEvaluation.setExcludeChecker( self.excludeChecker )
        resultEvaluation.setResultCalculator(self.resultCalculator )
        resultEvaluation.setResultCalculatorEuro(self.resultCalculatorEuro)
        return resultEvaluation

    def _createIndexEvaluation(self, indexName):
        return None

    def evaluateIndex(self, indexName, descriptionStr ):
        resultEvaluation = self._createResultEvaluation(indexName, descriptionStr )
        evaluation = self._createIndexEvaluation(indexName)

        evaluation.loadIndexHistory(self.startDate, self.endDate)
        transactionList = evaluation.calculateResult()
        transactionList.evaluateResult( resultEvaluation, self.resultTransactionPrinter )

        self.evaluationResultPrinter.printResult(indexName, descriptionStr, resultEvaluation)

    def runEvaluation(self, descriptionStr):
        for indexName in self.allIndices:
            self.evaluateIndex( indexName, descriptionStr )

    def runIndex(self, indexName, descriptionStr = "" ):
        self.setUp()
        self.evaluateIndex( indexName, descriptionStr )
        self.tearDown()

    def run(self, descriptionStr ):
        self.setUp()
        self.runEvaluation( descriptionStr )
        self.tearDown()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    EvalRunner.run()