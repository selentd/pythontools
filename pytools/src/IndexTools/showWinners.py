'''
Created on 08.06.2016

@author: selen00r
'''

import datetime

import evalbase
import evalcontinously
import evalresult
import evalrunner
import indexdatabase
import indexselector
import transactionchecker

import test_evalcontinously

class WinLossCounter():
    def __init__(self):
        self.win = 0
        self.loss = 0

    def update(self, result):
        if result < 0.0:
            self.loss += 1
        else:
            self.win += 1

    def total(self):
        return self.loss + self.win

    def winPercentage(self):
        if (self.win + self.loss) > 0:
            return (float(self.win) / float(self.win + self.loss))
        else:
            return 0.0

class DetailedTransactionPrinter(evalresult.TransactionResultPrinter):
    def __init__(self, showAll = False):
        self.showAll = showAll
        self.meanStatisticsLower = dict()
        self.meanStatisticsUpper = dict()
        self.gradStatisticsLower = dict()
        self.gradStatisticsUpper = dict()

        for mean in ("mean5", "mean8", "mean13", "mean21", "mean34", "mean38", "mean50", "mean55", "mean89", "mean100", "mean144", "mean200", "mean233"):
            self.meanStatisticsLower[mean] = WinLossCounter()
            self.meanStatisticsUpper[mean] = WinLossCounter()

        for grad in ("grad5", "grad8", "grad13", "grad21", "grad34", "grad38", "grad50", "grad55", "grad89", "grad100", "grad144", "grad200", "grad233"):
            self.gradStatisticsLower[grad] = WinLossCounter()
            self.gradStatisticsUpper[grad] = WinLossCounter()

    def updateMeanStatistics(self, idxBuy, result):
        if idxBuy.mean5 > 0:
            if ((idxBuy.close / idxBuy.mean5)-1.0) < 0:
                self.meanStatisticsLower["mean5"].update( result )
            else:
                self.meanStatisticsUpper["mean5"].update( result )

        if idxBuy.mean8 > 0:
            if ((idxBuy.close / idxBuy.mean8)-1.0) < 0:
                self.meanStatisticsLower["mean8"].update( result )
            else:
                self.meanStatisticsUpper["mean8"].update( result )

        if idxBuy.mean13 > 0:
            if ((idxBuy.close / idxBuy.mean13)-1.0) < 0:
                self.meanStatisticsLower["mean13"].update( result )
            else:
                self.meanStatisticsUpper["mean13"].update( result )

        if idxBuy.mean21 > 0:
            if ((idxBuy.close / idxBuy.mean21)-1.0) < 0:
                self.meanStatisticsLower["mean21"].update( result )
            else:
                self.meanStatisticsUpper["mean21"].update( result )

        if idxBuy.mean34 > 0:
            if ((idxBuy.close / idxBuy.mean34)-1.0) < 0:
                self.meanStatisticsLower["mean34"].update( result )
            else:
                self.meanStatisticsUpper["mean34"].update( result )

        if idxBuy.mean38 > 0:
            if ((idxBuy.close / idxBuy.mean38)-1.0) < 0:
                self.meanStatisticsLower["mean38"].update( result )
            else:
                self.meanStatisticsUpper["mean38"].update( result )

        if idxBuy.mean50 > 0:
            if ((idxBuy.close / idxBuy.mean50)-1.0) < 0:
                self.meanStatisticsLower["mean50"].update( result )
            else:
                self.meanStatisticsUpper["mean50"].update( result )

        if idxBuy.mean55 > 0:
            if ((idxBuy.close / idxBuy.mean55)-1.0) < 0:
                self.meanStatisticsLower["mean55"].update( result )
            else:
                self.meanStatisticsUpper["mean55"].update( result )

        if idxBuy.mean89 > 0:
            if ((idxBuy.close / idxBuy.mean89)-1.0) < 0:
                self.meanStatisticsLower["mean89"].update( result )
            else:
                self.meanStatisticsUpper["mean89"].update( result )

        if idxBuy.mean100 > 0:
            if ((idxBuy.close / idxBuy.mean100)-1.0) < 0:
                self.meanStatisticsLower["mean100"].update( result )
            else:
                self.meanStatisticsUpper["mean100"].update( result )

        if idxBuy.mean144 > 0:
            if ((idxBuy.close / idxBuy.mean144)-1.0) < 0:
                self.meanStatisticsLower["mean144"].update( result )
            else:
                self.meanStatisticsUpper["mean144"].update( result )

        if idxBuy.mean200 > 0:
            if ((idxBuy.close / idxBuy.mean200)-1.0) < 0:
                self.meanStatisticsLower["mean200"].update( result )
            else:
                self.meanStatisticsUpper["mean200"].update( result )

        if idxBuy.mean233 > 0:
            if ((idxBuy.close / idxBuy.mean233)-1.0) < 0:
                self.meanStatisticsLower["mean233"].update( result )
            else:
                self.meanStatisticsUpper["mean233"].update( result )

    def updateGradStatistics(self, idxBuy, result):
        if idxBuy.grad5 != 0.0:
            if idxBuy.grad5 < 0:
                self.gradStatisticsLower["grad5"].update( result )
            else:
                self.gradStatisticsUpper["grad5"].update( result )

        if idxBuy.grad8 != 0.0:
            if idxBuy.grad8 < 0:
                self.gradStatisticsLower["grad8"].update( result )
            else:
                self.gradStatisticsUpper["grad8"].update( result )

        if idxBuy.grad13 != 0.0:
            if idxBuy.grad13 < 0:
                self.gradStatisticsLower["grad13"].update( result )
            else:
                self.gradStatisticsUpper["grad13"].update( result )

        if idxBuy.grad21 != 0.0:
            if idxBuy.grad21 < 0:
                self.gradStatisticsLower["grad21"].update( result )
            else:
                self.gradStatisticsUpper["grad21"].update( result )

        if idxBuy.grad34 != 0.0:
            if idxBuy.grad34 < 0:
                self.gradStatisticsLower["grad34"].update( result )
            else:
                self.gradStatisticsUpper["grad34"].update( result )

        if idxBuy.grad38 != 0.0:
            if idxBuy.grad38 < 0:
                self.gradStatisticsLower["grad38"].update( result )
            else:
                self.gradStatisticsUpper["grad38"].update( result )

        if idxBuy.grad50 != 0.0:
            if idxBuy.grad50 < 0:
                self.gradStatisticsLower["grad50"].update( result )
            else:
                self.gradStatisticsUpper["grad50"].update( result )

        if idxBuy.grad55 != 0.0:
            if idxBuy.grad55 < 0:
                self.gradStatisticsLower["grad55"].update( result )
            else:
                self.gradStatisticsUpper["grad55"].update( result )

        if idxBuy.grad89 != 0.0:
            if idxBuy.grad89 < 0:
                self.gradStatisticsLower["grad89"].update( result )
            else:
                self.gradStatisticsUpper["grad89"].update( result )

        if idxBuy.grad100 != 0.0:
            if idxBuy.grad100 < 0:
                self.gradStatisticsLower["grad100"].update( result )
            else:
                self.gradStatisticsUpper["grad100"].update( result )

        if idxBuy.grad144 != 0.0:
            if idxBuy.grad144 < 0:
                self.gradStatisticsLower["grad144"].update( result )
            else:
                self.gradStatisticsUpper["grad144"].update( result )

        if idxBuy.grad200 != 0.0:
            if idxBuy.grad200 < 0:
                self.gradStatisticsLower["grad200"].update( result )
            else:
                self.gradStatisticsUpper["grad200"].update( result )

        if idxBuy.grad233 != 0.0:
            if idxBuy.grad233 < 0:
                self.gradStatisticsLower["grad233"].update( result )
            else:
                self.gradStatisticsUpper["grad233"].update( result )

    def calcStatistics(self, idxBuy, result):
        self.updateMeanStatistics( idxBuy, result )
        self.updateGradStatistics( idxBuy, result )

    def printResult(self, transactionResult, result, resultEuro, hasResult = False ):
        if hasResult:
            self.calcStatistics( transactionResult.indexBuy, result )

            showValues = self.showAll

            indexBuy = transactionResult.indexBuy
            indexSell = transactionResult.indexSell
            intraDay = 1.0 - (indexBuy.high / indexBuy.close)
            minCloseValue = transactionResult.getHighClose()
            minClose = 1.0 -(minCloseValue / indexBuy.close)

            if (indexSell.mean21 > indexSell.close):
                showValues = True

            #if (indexBuy.close > indexSell.close) and (minClose >= 0.0):
            if showValues == True:
                print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:3} {:10.2f} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          indexBuy.date,
                          indexSell.date,
                          transactionResult.indexHistory.len(),
                          indexBuy.close,
                          indexSell.close,
                          resultEuro,
                          result,
                          (indexBuy.high / indexBuy.close) -1.0,
                          (indexBuy.low / indexBuy.close) - 1.0,
                          (transactionResult.getHighValue() / indexBuy.close) - 1.0,
                          (transactionResult.getLowValue() / indexBuy.close) - 1.0)

        else:
            print str.format( '{:10} no result', transactionResult.indexName )


def showTransactions( transactionListDict ):
    idxSelector = indexselector.IndexSelectorIdxData()

    idxSelector.setupIdxData(transactionListDict, datetime.datetime( 2000, 1, 1), datetime.datetime.now())

def showTransactionStatistics( transactionPrinter ):
    print
    for mean in ("mean5", "mean8", "mean13", "mean21", "mean34", "mean38", "mean50", "mean55", "mean89", "mean100", "mean144", "mean200", "mean233"):
        print str.format('{:10} Lower: {:4} {:4} {:4} {:4.2f} Upper: {:4} {:4} {:4} {:4.2f}',
                mean,
                transactionPrinter.meanStatisticsLower[mean].total(),
                transactionPrinter.meanStatisticsLower[mean].win,
                transactionPrinter.meanStatisticsLower[mean].loss,
                transactionPrinter.meanStatisticsLower[mean].winPercentage(),
                transactionPrinter.meanStatisticsUpper[mean].total(),
                transactionPrinter.meanStatisticsUpper[mean].win,
                transactionPrinter.meanStatisticsUpper[mean].loss,
                transactionPrinter.meanStatisticsUpper[mean].winPercentage() )
    print
    for grad in ("grad5", "grad8", "grad13", "grad21", "grad34", "grad38", "grad50", "grad55", "grad89", "grad100", "grad144", "grad200", "grad233"):
        print str.format('{:10} Lower: {:4} {:4} {:4} {:4.2f} Upper: {:4} {:4} {:4} {:4.2f}',
                grad,
                transactionPrinter.gradStatisticsLower[grad].total(),
                transactionPrinter.gradStatisticsLower[grad].win,
                transactionPrinter.gradStatisticsLower[grad].loss,
                transactionPrinter.gradStatisticsLower[grad].winPercentage(),
                transactionPrinter.gradStatisticsUpper[grad].total(),
                transactionPrinter.gradStatisticsUpper[grad].win,
                transactionPrinter.gradStatisticsUpper[grad].loss,
                transactionPrinter.gradStatisticsUpper[grad].winPercentage() )


def showWinners():
    runParameters = dict()
    endTransactionCalculator = transactionchecker.EndTransactionCheckerMulti( 0.0, 0.5, 4, True)
    transactionPrinter = DetailedTransactionPrinter()

    meanKey = 55
    meanKey2 = 100
    meanKey3 = 233
    endMeanKey = 100

    maxWin = 0.0
    maxLoss = -0.001
    maxJump = 0.0
    maxHighJump = 0.0
    maxDays = 200
    knockOut = -0.01
    leverage = 4.0

    runParameters[evalrunner.EvalRunner.startDateKey] = datetime.datetime( 2000, 1, 1)
    #runParameters[evalrunner.EvalRunner.endDateKey] = datetime.datetime( yearStart + period, 1, 1)
    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = False
    runParameters[evalrunner.EvalRunner.idxDistanceKey] = leverage

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = True
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = meanKey
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = meanKey2
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = meanKey3
    runParameters[evalcontinously.EvalContinouslyMean.endMeanKey] = endMeanKey

    #runParameters[evalcontinously.EvalContinously.maxDaysKey] = maxDays
    #runParameters[evalcontinously.EvalContinously.maxWinKey] = maxWin
    runParameters[evalcontinously.EvalContinously.maxLossKey] = maxLoss
    #runParameters[evalcontinously.EvalContinously.maxJumpKey] = maxJump
    #runParameters[evalcontinously.EvalContinously.maxHighJumpKey] = maxHighJump
    runParameters[evalbase.EvalBase.knockOutKey] = knockOut
    runParameters[evalbase.EvalBase.endTransactionCalcKey] = endTransactionCalculator

    descr = str.format("\"Mean {:3} {:3} {:3}\"", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                    runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                    runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)

    runParameters[evalrunner.EvalRunner.resultPrinterKey] = evalrunner.EvalResultPrinterSimple()
    #runParameters[evalrunner.EvalRunner.transactionPrinterKey] = transactionPrinter

    evalBuys = test_evalcontinously.TestEvalContinously( runParameters )
    evalBuys.run( descr )

    #runParameters[evalcontinously.EvalContinouslyMean.gradKey] = 5
    #runParameters[evalcontinously.EvalContinouslyMean.minGradKey] = 0.04
    #descr = str.format("\"Grad {:3} {:4.2f}\"", runParameters[evalcontinously.EvalContinouslyMean.gradKey],
    #                                runParameters[evalcontinously.EvalContinouslyMean.minGradKey])

    #evalBuys = test_evalcontinously.TestEvalContinouslyGrad( runParameters )
    #evalBuys.run( descr )

    #showTransactionStatistics( transactionPrinter )
    #showTransactions( evalBuys.transactionListDict )

if __name__ == '__main__':
    showWinners()
