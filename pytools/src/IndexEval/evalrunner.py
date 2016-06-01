'''
Created on 04.11.2015

@author: selen00r
'''

import datetime

from pymongo.mongo_client import MongoClient

import evalresult
import indexdatabase

class EvalResultPrinter:

    def printResultHead(self, descriptionStr ):
        pass

    def printResult(self, indexName, descriptionStr, resultEvaluation):
        pass

class EvalResultPrinterSimple:

    def printResultHead(self, descriptionStr ):
        print str.format( '{:10} {:20} {:>4} {:>4} {:>4} {:>6} {:>6} {:>6} {:>6} {:>10} {:>10}',
                          "index",
                          "descr",
                          "tot",
                          "win",
                          "loss",
                          "winR",
                          "maxL",
                          "maxw",
                          "total",
                          "total-EUR",
                          "invest-EUR" )

    def printResult(self, indexName, descriptionStr, resultEvaluation):
        print str.format( '{:10} {:20} {:>4} {:>4} {:>4} {:>6.2f} {:>6.3f} {:>6.3f} {:>6.3f} {:>10.2f} {:>10.2f}',
                          indexName,
                          descriptionStr,
                          resultEvaluation.getTotalCount(),
                          resultEvaluation.winCount,
                          resultEvaluation.lossCount,
                          resultEvaluation.getWinRatio(),
                          resultEvaluation.maxLoss,
                          resultEvaluation.maxWin,
                          resultEvaluation.getTotalResult(),
                          resultEvaluation.getTotalResultEuro(),
                          resultEvaluation.getTotalInvestEuro() )


class EvalRunner(object):
    '''
    Base class to run an evaluation of an index.
    '''
    startInvestKey = "startInvest"
    maxInvestKey   = "maxInvest"
    fixedInvestKey = "fixedInvest"
    idxDistanceKey = "idxDistance"
    isCallKey      = "isCall"

    startDateKey   = "startDateKey"
    endDateKey     = "endDateKey"

    excludeCheckerKey = "excludeCheckerKey"

    resultPrinterKey      = "resultPrinterKey"
    transactionPrinterKey = "transactionPrinterKey"

    def __init__(self, runParameters = None):
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

        self.idxGold        = "gold"
        self.idxBrent       = "brent"

        self.allIndices = [self.idxATX, self.idxCAC, self.idxDax, self.idxDowJones, self.idxEStoxx50,
                           self.idxFTS100, self.idxFtseMib, self.idxHangSeng, self.idxIbex, self.idxMDax,
                           self.idxNasdaq100, self.idxNikkei, self.idxSDax, self.idxSMI, self.idxSP500, self.idxTecDax,
                           self.idxGold, self.idxBrent]

        self.indexDB = indexdatabase.getIndexDatabase()

        self.transactionListDict = dict()
        self.resultEvaluationDict = dict()
        self.runParameters = dict()
        if runParameters != None:
            self.runParameters = runParameters

    def _setupStartEndTime(self):
        if self.runParameters.has_key(EvalRunner.startDateKey):
            self.startDate = self.runParameters[EvalRunner.startDateKey]
        else:
            self.startDate = datetime.datetime( 2000, 1, 1 )

        if self.runParameters.has_key(EvalRunner.endDateKey):
            self.endDate = self.runParameters[EvalRunner.endDateKey]
        else:
            self.endDate = datetime.datetime.today()

    def _setupResultCalculator(self):
        if self.runParameters.has_key(EvalRunner.startInvestKey):
            self.startInvest = self.runParameters[EvalRunner.startInvestKey]
        else:
            self.startInvest = 1000.0

        if self.runParameters.has_key(EvalRunner.maxInvestKey):
            self.maxInvest = self.runParameters[EvalRunner.maxInvestKey]
        else:
            self.maxInvest = 100000.0

        if self.runParameters.has_key(EvalRunner.fixedInvestKey):
            self.fixedInvest = self.runParameters[EvalRunner.fixedInvestKey]
        else:
            self.fixedInvest = True

        if self.runParameters.has_key(EvalRunner.isCallKey):
            self.isCall = self.runParameters[EvalRunner.isCallKey]
        else:
            self.isCall = True

        if self.isCall:
            self.resultCalculator = evalresult.ResultCalculator()
        else:
            self.resultCalculator = evalresult.ResultCalculatorPut()

        if self.runParameters.has_key(EvalRunner.idxDistanceKey):
            if self.isCall:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( self.runParameters[EvalRunner.idxDistanceKey],
                                                                                     self.startInvest,
                                                                                     self.fixedInvest,
                                                                                     self.maxInvest )
            else:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeveragePut( self.runParameters[EvalRunner.idxDistanceKey],
                                                                                        self.startInvest,
                                                                                        self.fixedInvest,
                                                                                        self.maxInvest )

        else:
            if self.isCall:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest, self.maxInvest)
            else:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuroPut(self.startInvest, self.fixedInvest, self.maxInvest)

    def _setupResultExcludeChecker(self):
        if self.runParameters.has_key(EvalRunner.excludeCheckerKey):
            self.excludeChecker = self.runParameters[EvalRunner.excludeCheckerKey]
        else:
            self.excludeChecker = evalresult.ExcludeTransaction()

    def _setupTransactionPrinter(self):
        if self.runParameters.has_key(EvalRunner.transactionPrinterKey):
            self.resultTransactionPrinter = self.runParameters[EvalRunner.transactionPrinterKey]
        else:
            self.resultTransactionPrinter = evalresult.TransactionResultPrinter()

    def _setupEvalResultPrinter(self):
        if self.runParameters.has_key(EvalRunner.resultPrinterKey):
            self.evaluationResultPrinter = self.runParameters[EvalRunner.resultPrinterKey]
        else:
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

        resultEvaluation = evalresult.EvalResult( indexName + " " + descriptionStr, self.startInvest, self.fixedInvest )
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
        self.transactionListDict[indexName] = transactionList
        self.resultEvaluationDict[indexName] = resultEvaluation

    def runEvaluation(self, descriptionStr, indexList = None):
        self.evaluationResultPrinter.printResultHead( descriptionStr )
        if indexList == None:
            indexList = self.allIndices

        for indexName in indexList:
            self.evaluateIndex( indexName, descriptionStr )

    def runIndex(self, indexName, descriptionStr = "" ):
        self.setUp()
        self.evaluationResultPrinter.printResultHead( descriptionStr )
        self.evaluateIndex( indexName, descriptionStr )
        self.tearDown()

    def run(self, descriptionStr, indexList = None ):
        self.setUp()
        self.runEvaluation( descriptionStr, indexList )
        self.tearDown()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    EvalRunner.run()