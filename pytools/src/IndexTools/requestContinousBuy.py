'''
Created on 10.05.2016

@author: selen00r
'''

import datetime

import evalcontinously
import evalresult
import evalrunner
import indexdatabase

import test_evalcontinously

class DetailedTransactionPrinter(evalresult.TransactionResultPrinter):
    def printResult(self, transactionResult, result, resultEuro, hasResult = False ):
        if hasResult:
            buy = transactionResult.indexBuy.close

            print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {:> 6.3f} {:> 6.3f} {:> 6.3f}',
                          transactionResult.indexName,
                          transactionResult.indexBuy.date,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          transactionResult.getLowValue(),
                          transactionResult.getHighValue(),
                          resultEuro,
                          result,
                          (buy / transactionResult.indexBuy.mean8)-1.0,
                          (buy / transactionResult.indexBuy.mean13)-1.0,
                          (buy / transactionResult.indexBuy.mean21)-1.0,
                          (buy / transactionResult.indexBuy.mean89)-1.0,
                          (buy / transactionResult.indexBuy.mean200)-1.0,
                          transactionResult.indexBuy.grad13,
                          transactionResult.indexBuy.grad21,
                          transactionResult.indexBuy.grad200 )

        else:
            print str.format( '{:10} no result', transactionResult.indexName )


def requestContinousCallBuys( runParameters ):

    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 6.0
    runParameters[evalcontinously.EvalContinously.maxLossKey] = -0.001
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = 0.0

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = True
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = 0

    evalBuys = test_evalcontinously.TestEvalContinously( runParameters )
    descrStr = "run current calls"
    evalBuys.run( descrStr )

def requestContinousPutBuys( runParameters ):

    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 10.0

    runParameters[evalcontinously.EvalContinously.maxLossKey] = 0.0
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = 0.0

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = False
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = 13
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = 200

    evalBuys = test_evalcontinously.TestEvalContinously( runParameters )
    descrStr = "run current puts"
    evalBuys.run( descrStr )

def requestContinousBuys():
    runParameters = dict()

    runParameters[evalrunner.EvalRunner.startDateKey] = datetime.datetime(2016,8,1)
    runParameters[evalrunner.EvalRunner.endDateKey] = datetime.datetime.now()

    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = False

    runParameters[evalrunner.EvalRunner.resultPrinterKey] = evalrunner.EvalResultPrinterSimple()
    runParameters[evalrunner.EvalRunner.transactionPrinterKey] = DetailedTransactionPrinter()

    runParameters[evalcontinously.EvalContinously.maxDaysKey] = 100
    runParameters[evalcontinously.EvalContinously.maxWinKey] = 0.0

    requestContinousCallBuys( runParameters )
    #requestContinousPutBuys( runParameters )

if __name__ == '__main__':
    requestContinousBuys()

