'''
Created on 01.04.2016

@author: selen00r
'''

import evalcontinously
import evalresult
import evalrunner


class TestEvalContinously(evalrunner.EvalRunner):

    def __init__(self, mean, maxDays):
        evalrunner.EvalRunner.__init__(self)
        self.mean = mean
        self.maxDays = maxDays

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = True
        self.resultCalculator = evalresult.ResultCalculator()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, self.mean, self.maxDays )
        return evaluation

class TestEvalContinously2(evalrunner.EvalRunner):

    def __init__(self, mean1, mean2, maxDays):
        evalrunner.EvalRunner.__init__(self)
        self.mean1 = mean1
        self.mean2 = mean2
        self.maxDays = maxDays

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = True
        self.resultCalculator = evalresult.ResultCalculator()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyMean2( self.dbName, indexName, self.mean1, self.mean2, self.maxDays )
        return evaluation

if __name__ == "__main__":
    testEvaluation = TestEvalContinously2( 5, 21, 4 )
    testEvaluation.run( "Mean 5/21" )