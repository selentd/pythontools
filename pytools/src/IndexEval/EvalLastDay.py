'''
Created on 21.10.2015

@author: SELEN00R
'''

import datetime
import unittest

import fetchdata
from src.IndexEval.fetchdata import FetchData

class EvalLastDayTest(unittest.TestCase):
    '''
    Check the result, if investment is done only on the last day of the month.
    '''
    def setUp(self):
        self.dbName =       "stockdb"
        self.idxDax =       "dax"
        self.idxEstoxx50 =  "estoxx50"
        self.idxMdax =      "mdax"
        self.idxNasdaq =    "nasdaq100"
        self.idxNikkei =    "nikkei"
        self.idxSmi =       "smi"
        self.idxSp500 =     "sp500"
        self.idxTecDax =    "tecdax"

        self.startDate = datetime.datetime( 2000, 1, 1, 0, 0, 0, 0)
        self.endDate = datetime.datetime.now()

    def tearDown(self):
        pass

    def _getNextMonth(self, year, month):
        if month == 12:
            year = year + 1
            month = 1
        return( year, month )

    def _getFirstMonth(self):
        return( self.startDate.year, self.startDate.month )

    def _isEndOfPeriod(self, year, month):
        isEndOfPeriod = (year >= self.endDate.year) and (month >= self.endDate.month)
        return isEndOfPeriod

    def testName(self):
        monthlyHistory = list()
        fetchDataItems = fetchdata.FetchData( self.dbName, self.idxDax )
        currentPeriod = self._getFirstMonth()

        while not self._isEndOfPeriod(currentPeriod[0], currentPeriod[1]):
            indexHistory = fetchDataItems.fetchDataByMonth(currentPeriod[0], currentPeriod[1])
            if indexHistory.len() > 0:
                monthlyHistory.append( indexHistory )

            currentPeriod = self._getNextMonth(currentPeriod[0], currentPeriod[1])





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()