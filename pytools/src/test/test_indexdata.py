'''
Created on 20.10.2015

@author: SELEN00R
'''
import datetime

import unittest

from indexdata import IndexData
from indexdata import IndexHistory

class IndexHistoryTest(unittest.TestCase):


    def setUp(self):
        self.testlist = list()
        for count in range(0, 250):
            idxData = IndexData()
            idxData.set( datetime.datetime( 2014, 1, 1, 0, 0, 0) + datetime.timedelta( count ),
                         1000.0 + count, 1100.0 + count, 1200.0 + count, 900.0 + count)
            self.testlist.append( idxData )


    def tearDown(self):
        pass


    def testIndexHistoryLen(self):
        idxHistory = IndexHistory()
        for idxData in self.testlist:
            idxHistory.addIndexData(idxData)

        self.assertEqual( idxHistory.len(), 250, "Invalid length of history list")

    def testIndexHistoryAccess(self):
        idxHistory = IndexHistory()
        for idxData in self.testlist:
            idxHistory.addIndexData(idxData)

        self.assertEqual( idxHistory.len(), 250, "Invalid length of history list")
        self.assertEqual( idxHistory.getFirst().close, 1100, "Invalid value in first element")
        self.assertEqual( idxHistory.getLast().close, 1100 + 249, "Invalid value in last element")
        self.assertEqual( idxHistory.getIndex(15).close, 1100 + 15, "Invalid value at index 15")

    def testIndexHistoryMean(self):
        idxHistory = IndexHistory()
        for idxData in self.testlist:
            idxHistory.addIndexData(idxData)

        idxHistory.calcMeanValues()

        self.assertEqual( idxHistory.len(), 250, "Invalid length of history list")

        # --- check for zero values at the start
        self.assertEqual( idxHistory.getFirst().mean5, 0, "Invalid mean5 at first element")
        self.assertEqual( idxHistory.getFirst().mean13, 0, "Invalid mean13 at first element")
        self.assertEqual( idxHistory.getFirst().mean38, 0, "Invalid mean38 at first element")
        self.assertEqual( idxHistory.getFirst().mean89, 0, "Invalid mean89 at first element")
        self.assertEqual( idxHistory.getFirst().mean200, 0, "Invalid mean200 at first element")

        # --- check for correct values at first 5 mean value
        self.assertEqual( idxHistory.getIndex(4).mean5, 1102, "Invalid mean5 at element 4")
        self.assertEqual( idxHistory.getIndex(4).mean13, 0, "Invalid mean13 at element 4")
        self.assertEqual( idxHistory.getIndex(4).mean38, 0, "Invalid mean38 at element 4")
        self.assertEqual( idxHistory.getIndex(4).mean89, 0, "Invalid mean89 at element 4")
        self.assertEqual( idxHistory.getIndex(4).mean200, 0, "Invalid mean200 at element 4")

        # --- check for correct value at first 13 mean value
        self.assertEqual( idxHistory.getIndex(12).mean5, 1110, "Invalid mean5 at element 13")
        self.assertEqual( idxHistory.getIndex(12).mean13, 1106, "Invalid mean13 at element 13")
        self.assertEqual( idxHistory.getIndex(12).mean38, 0, "Invalid mean38 at element 13")
        self.assertEqual( idxHistory.getIndex(12).mean89, 0, "Invalid mean89 at element 13")
        self.assertEqual( idxHistory.getIndex(12).mean200, 0, "Invalid mean200 at element 13")

        # --- check for correct value at first 38 mean value
        self.assertEqual( idxHistory.getIndex(37).mean5, 1135, "Invalid mean5 at element 37")
        self.assertEqual( idxHistory.getIndex(37).mean13, 1131, "Invalid mean13 at element 37")
        self.assertEqual( idxHistory.getIndex(37).mean38, 1118.5, "Invalid mean38 at element 37")
        self.assertEqual( idxHistory.getIndex(37).mean89, 0, "Invalid mean89 at element 37")
        self.assertEqual( idxHistory.getIndex(37).mean200, 0, "Invalid mean200 at element 37")

        # --- check for correct value at first 89 mean value
        self.assertEqual( idxHistory.getIndex(88).mean5, 1186, "Invalid mean5 at element 88")
        self.assertEqual( idxHistory.getIndex(88).mean13, 1182, "Invalid mean13 at element 88")
        self.assertEqual( idxHistory.getIndex(88).mean38, 1169.5, "Invalid mean38 at element 88")
        self.assertEqual( idxHistory.getIndex(88).mean89, 1144, "Invalid mean89 at element 88")
        self.assertEqual( idxHistory.getIndex(88).mean200, 0, "Invalid mean200 at element 88")

        # --- check for correct value at first 200 mean value
        self.assertEqual( idxHistory.getIndex(199).mean5, 1297, "Invalid mean5 at element 199")
        self.assertEqual( idxHistory.getIndex(199).mean13, 1293, "Invalid mean13 at element 199")
        self.assertEqual( idxHistory.getIndex(199).mean38, 1280.5, "Invalid mean38 at element 199")
        self.assertEqual( idxHistory.getIndex(199).mean89, 1255, "Invalid mean89 at element 199")
        self.assertEqual( idxHistory.getIndex(199).mean200, 1199.5, "Invalid mean200 at element 199")

        # --- check for correctly calculated values at the end
        self.assertEqual( idxHistory.getLast().mean5, 1347, "Invalid mean5 at last element")
        self.assertEqual( idxHistory.getLast().mean13, 1343, "Invalid mean13 at last element")
        self.assertEqual( idxHistory.getLast().mean38, 1330.5, "Invalid mean38 at last element")
        self.assertEqual( idxHistory.getLast().mean89, 1305, "Invalid mean89 at last element")
        self.assertEqual( idxHistory.getLast().mean200, 1249.5, "Invalid mean200 at last element")

def suite():
    moduleSuite = unittest.TestSuite()
    moduleSuite.addTests( unittest.TestLoader().loadTestsFromTestCase(IndexHistoryTest) )
    return moduleSuite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()