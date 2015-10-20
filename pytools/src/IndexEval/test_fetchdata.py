'''
Created on 20.10.2015

@author: SELEN00R
'''

import datetime

import unittest

from fetchdata import FetchData

class FetchDataTest(unittest.TestCase):

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

    def tearDown(self):
        pass

    def testFetchNoData(self):
        resultList = FetchData(self.dbName, self.idxDax).fetchDataByDate( datetime.datetime(1950, 01, 02, 0, 0),
                                                                          datetime.datetime(1960, 01, 02, 0, 0) )
        self.assertEqual( resultList.len(), 0, "Result list is not empty")

    def testFetchJanuary(self):
        resultList = FetchData(self.dbName, self.idxDax).fetchDataByMonth( 2010, 1 )
        self.assertNotEqual( resultList.len(), 0, "Result list is empty")
        self.assertEqual( resultList.getFirst().date.year, 2010, "Invalid year for first value")
        self.assertEqual( resultList.getLast().date.year, 2010, "Invalid year for last value")
        self.assertEqual( resultList.getFirst().date.month, 1, "Invalid month (not january) for first value")
        self.assertEqual( resultList.getLast().date.month, 1, "Invalid month (not january) for last value")
        self.assertEqual( resultList.getFirst().date.day, 4, "Invalid day (not january) for first value")
        self.assertEqual( resultList.getLast().date.day, 29, "Invalid day (not january) for last value")


    def testFetchDecember(self):
        resultList = FetchData(self.dbName, self.idxDax).fetchDataByMonth( 2010, 12 )
        self.assertNotEqual( resultList.len(), 0, "Result list is empty")
        self.assertEqual( resultList.getFirst().date.year, 2010, "Invalid year for first value")
        self.assertEqual( resultList.getLast().date.year, 2010, "Invalid year for last value")
        self.assertEqual( resultList.getFirst().date.month, 12, "Invalid month (not december) for first value")
        self.assertEqual( resultList.getLast().date.month, 12, "Invalid month (not december) for last value")
        self.assertEqual( resultList.getFirst().date.day, 1, "Invalid day (not january) for first value")
        self.assertEqual( resultList.getLast().date.day, 31, "Invalid day (not january) for last value")

    def testFetchMarch(self):
        resultList = FetchData(self.dbName, self.idxDax).fetchDataByMonth( 2010, 3 )
        self.assertNotEqual( resultList.len(), 0, "Result list is empty")
        self.assertEqual( resultList.getFirst().date.year, 2010, "Invalid year for first value")
        self.assertEqual( resultList.getLast().date.year, 2010, "Invalid year for last value")
        self.assertEqual( resultList.getFirst().date.month, 3, "Invalid month (not march) for first value")
        self.assertEqual( resultList.getLast().date.month, 3, "Invalid month (not march) for last value")
        self.assertEqual( resultList.getFirst().date.day, 1, "Invalid day (not january) for first value")
        self.assertEqual( resultList.getLast().date.day, 31, "Invalid day (not january) for last value")


def suite():
    moduleSuite = unittest.TestSuite()
    moduleSuite.addTests( unittest.TestLoader().loadTestsFromTestCase(FetchDataTest) )
    return moduleSuite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()