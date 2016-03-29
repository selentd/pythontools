'''
Created on 21.10.2015

@author: selen00r
'''
import datetime
import unittest

import evalresult
import fetchdata
import indexdata

class EvalResultTest(unittest.TestCase):


    def setUp(self):
        self.dbName = "stockdb"
        self.idxDax = "dax"
        self.startDate = datetime.datetime( 2013, 12, 1 )
        self.endDate = datetime.datetime( 2014, 3, 1)


    def tearDown(self):
        pass


    def testResultCalculator(self):
        calculator = evalresult.ResultCalculator()

        self.assertEqual(calculator.getTotal(), 0, "Invalid initial total")

        self.assertAlmostEqual(calculator.calcResult(100, 110), 0.1, 1, "Invalid result calculation")
        self.assertAlmostEqual(calculator.getTotal(), 0.1, 1, "Invalid total calculation")

        self.assertAlmostEqual(calculator.calcResult(100, 90), -0.1, 1, "Invalid result calculation")
        self.assertAlmostEqual(calculator.getTotal(), 0.0, 1, "Invalid total calculation")

        self.assertAlmostEqual(calculator.calcResult(100, 110), 0.1, 1, "Invalid result calculation")
        calculator.reset()
        self.assertEqual(calculator.getTotal(), 0, "Invalid initial total")

    def testResultCalculatorEuroFixed(self):
        calculator = evalresult.ResultCalculatorEuro( 1000 )

        self.assertEqual(calculator.getTotal(), 1000.0, "Invalid initial total")

        self.assertAlmostEqual(calculator.calcResult(100, 110), 100.0, 1, "Invalid result calculation")
        self.assertAlmostEqual(calculator.getTotal(), 1100.0, 1, "Invalid total calculation")

        self.assertAlmostEqual(calculator.calcResult(100, 90), -100.0, 1, "Invalid result calculation")
        self.assertAlmostEqual(calculator.getTotal(), 1000.0, 1, "Invalid total calculation")

        self.assertAlmostEqual(calculator.calcResult(100, 110), 100.0, 1, "Invalid result calculation")
        calculator.reset()
        self.assertEqual(calculator.getTotal(), 1000.0, "Invalid initial total")

    def testResultCalculatorEuroReinvest(self):
        calculator = evalresult.ResultCalculatorEuro( 1000, False )

        self.assertEqual(calculator.getTotal(), 1000.0, "Invalid initial total")

        self.assertAlmostEqual(calculator.calcResult(100, 110), 100.0, 1, "Invalid result calculation")
        self.assertAlmostEqual(calculator.getTotal(), 1100.0, 1, "Invalid total calculation")

        self.assertAlmostEqual(calculator.calcResult(100, 90), -110.0, 1, "Invalid result calculation")
        self.assertAlmostEqual(calculator.getTotal(), 990.0, 1, "Invalid total calculation")

        self.assertAlmostEqual(calculator.calcResult(100, 110), 99.0, 1, "Invalid result calculation")
        self.assertAlmostEqual(calculator.getTotal(), (990.0+99.0), 1, "Invalid total calculation")
        calculator.reset()
        self.assertEqual(calculator.getTotal(), 1000.0, "Invalid initial total")

    def testEvalResultCall(self):
        evaluation = evalresult.EvalResultCall( "test dax", 1000.0 )
        transactionResultList = indexdata.TransactionResultHistory()
        monthlyHistory = fetchdata.FetchData( self.dbName, self.idxDax ).fetchMonthlyHistory(self.startDate, self.endDate)

        for historyList in monthlyHistory:
            transactionResult = indexdata.TransactionResult()
            transactionResult.setResult(historyList.getFirst(), historyList.getLast())
            transactionResultList.addTransactionResult( transactionResult )

        transactionResultList.evaluateResult( evaluation )
        self.assertEqual( evaluation.getTotalCount(), 3, "Invalid total count for evaluation")
        self.assertEqual(evaluation.winCount, 2, "Invalid count for wins")
        self.assertEqual(evaluation.lossCount, 1, "Invalid count for losses")
        self.assertAlmostEqual(evaluation.getWinRatio(), (2.0 / 3.0), 4, "Invalid win ratio" )

def suite():
    moduleSuite = unittest.TestSuite()
    moduleSuite.addTests( unittest.TestLoader().loadTestsFromTestCase(EvalResultTest) )
    return moduleSuite


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()