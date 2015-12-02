'''
Created on 04.11.2015

@author: selen00r
'''

import datetime

from pymongo.mongo_client import MongoClient

import evalresult

class EvalRunner(object):
    '''
    Base class to run an evaluation of an index.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.dbName = "indexdb"

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

    def setUp(self):
        self.startDate = datetime.datetime( 2000, 1, 1 )
        self.endDate = datetime.datetime( 2015, 12, 1 )

        self.startInvest = 1000.0
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeTransaction()
        self.resultCalculator = evalresult.ResultCalculator()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)

    def tearDown(self):
        pass

    def _createResultEvaluation(self, indexName):
        self.resultCalculator.reset()
        self.resultCalculatorEuro.reset()

        resultEvaluation = evalresult.EvalResultCall( indexName + " Monthly", self.startInvest, self.fixedInvest )
        resultEvaluation.setExcludeChecker( self.excludeChecker )
        resultEvaluation.setResultCalculator(self.resultCalculator )
        resultEvaluation.setResultCalculatorEuro(self.resultCalculatorEuro)
        return resultEvaluation

    def _createIndexEvaluation(self):
        return None

    def _evaluateIndex(self, indexName):
        resultEvaluation = self._createResultEvaluation(indexName)
        evaluation = self.createIndexEvaluation()

        evaluation.loadIndexHistory(self.startDate, self.endDate)
        transactionList = evaluation.calculateResult()
        transactionList.evaluateResult( resultEvaluation )
        #transactionList.evaluateResult( resultEvaluation, printLastDayTransaction )

    def runEvaluation(self):
        pass

    def run(self):
        self.setUp()
        self.runEvaluation()
        self.tearDown()

