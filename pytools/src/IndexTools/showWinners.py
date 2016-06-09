'''
Created on 08.06.2016

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
            indexBuy = transactionResult.indexBuy
            indexSell = transactionResult.indexSell
            intraDay = 1.0 - (indexBuy.high / indexBuy.close)
            minCloseValue = transactionResult.getHighClose()
            minClose = 1.0 -(minCloseValue / indexBuy.close)

            if (indexBuy.close > indexSell.close) and (minClose >= 0.0):
                print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:3} {:10.2f} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          indexBuy.date,
                          indexSell.date,
                          transactionResult.indexHistory.len(),
                          indexBuy.close,
                          indexSell.close,
                          resultEuro,
                          result,
                          1.0 - (indexBuy.high / indexBuy.close),
                          1.0 - (indexBuy.low / indexBuy.close),
                          1.0 - (transactionResult.getHighValue() / indexBuy.close),
                          1.0 - (transactionResult.getLowValue() / indexBuy.close) )

        else:
            print str.format( '{:10} no result', transactionResult.indexName )

def showWinners():
    runParameters = dict()

    meanKey = 5
    meanKey2 = 0
    meanKey3 = 0

    maxWin = 0.0
    maxLoss = 0.0001
    maxJump = 0.00
    maxHighJump = 0.00

    runParameters[evalrunner.EvalRunner.startDateKey] = datetime.datetime( 2000, 1, 1)
    #runParameters[evalrunner.EvalRunner.endDateKey] = datetime.datetime( yearStart + period, 1, 1)
    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = False
    #runParameters[evalrunner.EvalRunner.idxDistanceKey] = 10.0

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = False
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = meanKey
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = meanKey2
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = meanKey3

    runParameters[evalcontinously.EvalContinously.maxWinKey] = maxWin
    runParameters[evalcontinously.EvalContinously.maxLossKey] = maxLoss
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = maxJump
    runParameters[evalcontinously.EvalContinously.maxHighJumpKey] = maxHighJump


    descr = str.format("\"Mean {:3} {:3} {:3}\"", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                    runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                    runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)

    runParameters[evalrunner.EvalRunner.resultPrinterKey] = evalrunner.EvalResultPrinterSimple()
    runParameters[evalrunner.EvalRunner.transactionPrinterKey] = DetailedTransactionPrinter()

    evalBuys = test_evalcontinously.TestEvalContinously( runParameters )
    evalBuys.run( descr )

if __name__ == '__main__':
    showWinners()