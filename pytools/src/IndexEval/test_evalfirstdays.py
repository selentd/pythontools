'''
Created on 29.10.2015

@author: selen00r
'''

import datetime
import unittest

import evalmonthly
import evalresult

class Test(unittest.TestCase):

    def setUp(self):
        self.dbName = "stockdb"
        self.startDate = datetime.datetime( 2000, 1, 1 )
        self.endDate = datetime.datetime( 2014, 1, 1)
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeTransaction()
        self.resultCalculator = evalresult.ResultCalculator()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(1000.0, self.fixedInvest)

    def tearDown(self):
        pass

    def _createResultEvalution(self, indexName):
        self.resultCalculator.reset()
        self.resultCalculatorEuro.reset()

        resultEvaluation = evalresult.EvalResultCall( indexName + " Monthly", 1000.0, self.fixedInvest )
        resultEvaluation.setExcludeChecker( self.excludeChecker )
        resultEvaluation.setResultCalculator(self.resultCalculator )
        resultEvaluation.setResultCalculatorEuro(self.resultCalculatorEuro)
        return resultEvaluation

    def _testIndexYear(self, index, start, end, resultEvaluation = None):
        self.startDate = datetime.datetime( start, 1, 1 )
        self.endDate = datetime.datetime( end, 1, 1)

        evaluation = evalmonthly.EvalFirstDays(4, self.dbName, index)

        if not resultEvaluation:
            resultEvaluation = self._createResultEvalution(index)

        evaluation.loadIndexHistory(self.startDate, self.endDate)
        transactionList = evaluation.calculateResult()
        transactionList.evaluateResult( resultEvaluation )

        print str.format( '{:10} {:>4} {:>4} {:>4} {:>6.2f} {:>6.3f} {:>6.3f} {:>8.2f}',
                          index,
                          resultEvaluation.getTotalCount(),
                          resultEvaluation.winCount,
                          resultEvaluation.lossCount,
                          resultEvaluation.getWinRatio(),
                          resultEvaluation.maxLoss,
                          resultEvaluation.getTotalResult(),
                          resultEvaluation.getTotalResultEuro() )

    def calcLastDayDax(self):
        indexName = "dax"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayMDax(self):
        indexName = "mdax"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayTecDax(self):
        indexName = "tecdax"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDaySP500(self):
        indexName = "sp500"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayNasdaq(self):
        indexName = "nasdaq100"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayEStoxx50(self):
        indexName = "estoxx50"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayNikkei(self):
        indexName = "nikkei"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDaySMI(self):
        indexName = "smi"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayATX(self):
        indexName = "atx"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayCAC(self):
        indexName = "cac"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayDowJones(self):
        indexName = "dowjones"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayFts100(self):
        indexName = "fts100"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayFtseMib(self):
        indexName = "ftsemib"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayHangseng(self):
        indexName = "hangseng"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcLastDayIbex(self):
        indexName = "ibex"
        resultEvaluation = self._createResultEvalution(indexName)
        self._testIndexYear( indexName, 2000, 2014, resultEvaluation )

    def calcIndices(self):
        self.calcLastDayDax()
        self.calcLastDayMDax()
        self.calcLastDayTecDax()
        self.calcLastDaySP500()
        self.calcLastDayNasdaq()
        self.calcLastDayEStoxx50()
        self.calcLastDayNikkei()
        self.calcLastDaySMI()
        self.calcLastDayATX()
        self.calcLastDayCAC()
        self.calcLastDayDowJones()
        self.calcLastDayFts100()
        self.calcLastDayFtseMib()
        self.calcLastDayHangseng()
        self.calcLastDayIbex()

    def _testEvalLastDayFixed(self):
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeTransaction()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, True )

        print "--- Calc first days with fixed invest ---"
        self.calcIndices()

    def _testEvalLastDayRolling(self):
        self.fixedInvest = False
        self.excludeChecker = evalresult.ExcludeTransaction()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )

        print "--- Calc first days with rolling invest ---"
        self.calcIndices()

    def _testEvalLastDayFixed_ExcludeAvg200(self):
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeAvg200Low()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, True )

        print "--- Calc first days with fixed invest, exclude close < Avg200 ---"
        self.calcIndices()

    def testEvalLastDayRolling_ExcludeAvg200(self):
        self.fixedInvest = False
        self.excludeChecker = evalresult.ExcludeAvg200Low()
        #self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 4, 1000.0, False )

        print "--- Calc first days with rolling invest, leverage 15, exclude close < (Avg200-3%) ---"
        self.calcIndices()

'''
        self.excludeChecker = evalresult.ExcludeAvg200Low(-0.02)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 20, 1000.0, False )

        print "--- Calc first days with rolling invest, exclude close < (Avg200-2%) ---"
        self.calcIndices()

        self.excludeChecker = evalresult.ExcludeAvg200Low(-0.01)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 20, 1000.0, False )

        print "--- Calc first days with rolling invest, exclude close < (Avg200-1%) ---"
        self.calcIndices()

        self.excludeChecker = evalresult.ExcludeAvg200Low()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 20, 1000.0, False )

        print "--- Calc first days with rolling invest, exclude close < (Avg200) ---"
        self.calcIndices()

        self.excludeChecker = evalresult.ExcludeAvg200Low(0.01)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 20, 1000.0, False )

        print "--- Calc first days with rolling invest, exclude close < (Avg200+1%) ---"
        self.calcIndices()

        self.excludeChecker = evalresult.ExcludeAvg200Low(0.02)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 20, 1000.0, False )

        print "--- Calc first days with rolling invest, exclude close < (Avg200+2%) ---"
        self.calcIndices()

        self.excludeChecker = evalresult.ExcludeAvg200Low(0.03)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro( 1000.0, False )
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 20, 1000.0, False )

        print "--- Calc first days with rolling invest, exclude close < (Avg200+3%) ---"
        self.calcIndices()
'''


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()