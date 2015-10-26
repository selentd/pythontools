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
        self.startDate = datetime.datetime( 2013, 1, 1 )
        self.endDate = datetime.datetime( 2014, 1, 1)


    def tearDown(self):
        pass


    def _testIndexYear(self, index, year):
        self.startDate = datetime.datetime( year, 1, 1 )
        self.endDate = datetime.datetime( year+1, 1, 1)

        evaluation = evalmonthly.EvalLastDay(self.dbName, index)
        resultEvaluation = evalresult.EvalResultCall( "DAX 2013", 1000.0, True )


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

    def _testIndexYearExcludeAvg200(self, index, year):
        self.startDate = datetime.datetime( year, 1, 1 )
        self.endDate = datetime.datetime( year+1, 1, 1)

        evaluation = evalmonthly.EvalLastDay(self.dbName, index)
        resultEvaluation = evalresult.EvalResultCall( "DAX 2013", 1000.0 )
        resultEvaluation.setExcludeChecker( evalresult.ExcludeAvg200Low() )


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


    def testEvalLastDayDax(self):
        indexName = "dax"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )

    def testEvalLastDayMDax(self):
        indexName = "mdax"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )

    def testEvalLastDayTecDax(self):
        indexName = "tecdax"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )

    def testEvalLastDaySP500(self):
        indexName = "sp500"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )

    def testEvalLastDayNasdaq100(self):
        indexName = "nasdaq100"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )

    def testEvalLastDayEStoxx50(self):
        indexName = "estoxx50"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )

    def testEvalLastDayNikkei(self):
        indexName = "nikkei"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )

    def testEvalLastDaySMI(self):
        indexName = "smi"
        for year in range(2000, 2014):
            #self._testIndexYear( indexName, year )
            self._testIndexYearExcludeAvg200( indexName, year )




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()