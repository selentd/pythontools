'''
Created on 23.10.2015

@author: selen00r
'''
import datetime
import unittest

import evalmonthly
import evalresult

class EvalLastDayTest(unittest.TestCase):


    def setUp(self):
        self.dbName = "stockdb"
        self.startDate = datetime.datetime( 2000, 1, 1 )
        self.endDate = datetime.datetime( 2014, 1, 1)
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeTransaction()

    def tearDown(self):
        pass


    def _createResultEvalution(self, indexName):
        resultEvaluation = evalresult.EvalResultCall( indexName + " Monthly", 1000.0, self.fixedInvest )
        resultEvaluation.setExcludeChecker( self.excludeChecker )
        return resultEvaluation

    def _testIndexYear(self, index, year, resultEvaluation = None):
        self.startDate = datetime.datetime( year, 1, 1 )
        self.endDate = datetime.datetime( year+1, 1, 1)

        evaluation = evalmonthly.EvalLastDay(self.dbName, index)

        if not resultEvaluation:
            resultEvaluation = self._createResultEvalution(index)

        evaluation.loadIndexHistory(self.startDate, self.endDate)
        transactionList = evaluation.calculateResult()
        transactionList.evaluateResult( resultEvaluation )

        print str.format( '{:10} {:>4} {:>4} {:>4} {:>4} {:>6.2f} {:>6.3f} {:>6.3f} {:>8.2f}',
                          index,
                          year,
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
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def calcLastDayMDax(self):
        indexName = "mdax"
        resultEvaluation = self._createResultEvalution(indexName)
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def calcLastDayTecDax(self):
        indexName = "tecdax"
        resultEvaluation = self._createResultEvalution(indexName)
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def calcLastDaySP500(self):
        indexName = "sp500"
        resultEvaluation = self._createResultEvalution(indexName)
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def calcLastDayNasdaq(self):
        indexName = "nasdaq100"
        resultEvaluation = self._createResultEvalution(indexName)
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def calcLastDayEStoxx50(self):
        indexName = "estoxx50"
        resultEvaluation = self._createResultEvalution(indexName)
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def calcLastDayNikkei(self):
        indexName = "nikkei"
        resultEvaluation = self._createResultEvalution(indexName)
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def calcLastDaySMI(self):
        indexName = "smi"
        resultEvaluation = self._createResultEvalution(indexName)
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYear( indexName, year, resultEvaluation )

    def testEvalLastDayFixed(self):
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeTransaction()

        print "--- Calc Last day with fixed invest ---"
        self.calcLastDayDax()
        self.calcLastDayMDax()
        self.calcLastDayTecDax()
        self.calcLastDaySP500()
        self.calcLastDayNasdaq()
        self.calcLastDayEStoxx50()
        self.calcLastDayNikkei()
        self.calcLastDaySMI()

    def testEvalLastDayRolling(self):
        self.fixedInvest = False
        self.excludeChecker = evalresult.ExcludeTransaction()

        print "--- Calc Last day with rolling invest ---"
        self.calcLastDayDax()
        self.calcLastDayMDax()
        self.calcLastDayTecDax()
        self.calcLastDaySP500()
        self.calcLastDayNasdaq()
        self.calcLastDayEStoxx50()
        self.calcLastDayNikkei()
        self.calcLastDaySMI()

    def testEvalLastDayFixed_ExcludeAvg200(self):
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeAvg200Low()

        print "--- Calc Last day with fixed invest, exclude close < Avg200 ---"
        self.calcLastDayDax()
        self.calcLastDayMDax()
        self.calcLastDayTecDax()
        self.calcLastDaySP500()
        self.calcLastDayNasdaq()
        self.calcLastDayEStoxx50()
        self.calcLastDayNikkei()
        self.calcLastDaySMI()

    def testEvalLastDayRolling_ExcludeAvg200(self):
        self.fixedInvest = False
        self.excludeChecker = evalresult.ExcludeAvg200Low()

        print "--- Calc Last day with rolling invest, exclude close < Avg200 ---"
        self.calcLastDayDax()
        self.calcLastDayMDax()
        self.calcLastDayTecDax()
        self.calcLastDaySP500()
        self.calcLastDayNasdaq()
        self.calcLastDayEStoxx50()
        self.calcLastDayNikkei()
        self.calcLastDaySMI()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()