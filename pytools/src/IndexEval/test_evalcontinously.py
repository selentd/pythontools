'''
Created on 01.04.2016

@author: selen00r
'''

import evalcontinously
import evalresult
import evalrunner

class TestEvalContinously(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)
        self.mean = mean
        self.maxDays = maxDays
        self.maxLoss = maxLoss
        self.maxJump = maxJump
        self.offset = offset

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = False
        self.resultCalculator = evalresult.ResultCalculator()
        #self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 20.0, self.startInvest, self.fixedInvest )

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, self.mean, self.offset, self.maxDays, self.maxLoss, self.maxJump )
        return evaluation

class TestEvalContinously2(evalrunner.EvalRunner):

    def __init__(self, mean1, mean2, maxDays=0, maxLoss = 0.0, maxJump = 0.0):
        evalrunner.EvalRunner.__init__(self)
        self.mean1 = mean1
        self.mean2 = mean2
        self.maxDays = maxDays
        self.maxLoss = maxLoss
        self.maxJump = maxJump

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = True
        self.resultCalculator = evalresult.ResultCalculator()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)
        #self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 15.0, self.startInvest, self.fixedInvest )

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyMean2( self.dbName, indexName, self.mean1, self.mean2, self.maxDays, self.maxLoss, self.maxJump )
        return evaluation

class TestEvalContinously3(evalrunner.EvalRunner):

    def __init__(self, mean1, mean2, mean3, maxDays=0, maxLoss = 0.0, maxJump = 0.0):
        evalrunner.EvalRunner.__init__(self)
        self.mean1 = mean1
        self.mean2 = mean2
        self.mean3 = mean3
        self.maxDays = maxDays
        self.maxLoss = maxLoss
        self.maxJump = maxJump

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = False
        self.resultCalculator = evalresult.ResultCalculator()
        #self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 10.0, self.startInvest, self.fixedInvest )

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyMean3( self.dbName, indexName, self.mean1, self.mean2, self.mean3, self.maxDays, self.maxLoss, self.maxJump )
        return evaluation

if __name__ == "__main__":

    mean = 200
    mean2 = 34
    mean3 = 34
    offset = 0.00
    maxDays = 100
    maxLoss = -0.08
    maxJump = -0.02

    descr = str.format("Mean {:3} {:3.2f} {:3.2f}", mean, offset, maxLoss)
    testEvaluation = TestEvalContinously( mean, offset, maxLoss )
    testEvaluation.run( descr )
    print ""

    offset = 0.01
    descr = str.format("Mean {:3} {:3.2f} {:3.2f}", mean, offset, maxLoss)
    testEvaluation = TestEvalContinously( mean, offset, maxLoss )
    testEvaluation.run( descr )
    print ""

    offset = 0.03
    descr = str.format("Mean {:3} {:3.2f} {:3.2f}", mean, offset, maxLoss)
    testEvaluation = TestEvalContinously( mean, offset, maxLoss )
    testEvaluation.run( descr )
    print ""

    mean = 21
    descr = str.format("Mean {:3} {:3} {:3}", mean, mean2, mean3)
    testEvaluation = TestEvalContinously3( mean, mean2, mean3 )
    testEvaluation.run( descr )
    print ""

    testEvaluation = TestEvalContinously3( mean, mean2, mean3, maxDays, maxLoss )
    testEvaluation.run( descr )
    print ""

    testEvaluation = TestEvalContinously3( mean, mean2, mean3, maxDays, maxLoss, maxJump )
    testEvaluation.run( descr )
    print ""

