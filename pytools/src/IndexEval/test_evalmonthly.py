'''
Created on 23.10.2015

@author: selen00r
'''
import datetime
import unittest

import evalmonthly

class EvalLastDayTest(unittest.TestCase):


    def setUp(self):
        self.dbName = "stockdb"
        self.idxDax = "dax"
        self.startDate = datetime.datetime( 2013, 12, 1 )
        self.endDate = datetime.datetime( 2014, 2, 1)


    def tearDown(self):
        pass


    def testEvalLastDay(self):
        evaluation = evalmonthly.EvalLastDay(self.dbName, self.idxDax)

        evaluation.loadIndexHistory(self.startDate, self.endDate)
        transactionList = evaluation.calculateResult()




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()