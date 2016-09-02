'''
Created on 31.08.2016

@author: SELEN00R
'''

import datetime

import evalbase
import evalbest
import evalresult
import evalrunner
import indexdatabase
import transactionchecker

class EvalBestTransactionPrinter( evalrunner.EvalResultPrinter):
    
    def printResult(self, transactionResult, result, resultEuro, hasResult = False ):
        if hasResult:
            print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:3} {:10.2f} {: 2.4f}',
                              transactionResult.indexName,
                              transactionResult.indexBuy.date,
                              transactionResult.indexSell.date,
                              transactionResult.indexBuy.close,
                              transactionResult.indexSell.close,
                              transactionResult.getLowValue(),
                              transactionResult.getHighValue(),
                              transactionResult.indexHistory.len(),
                              resultEuro,
                              result )    
    
if __name__ == '__main__':

    runParameters = dict()

    runParameters[evalrunner.EvalRunner.startDateKey] = datetime.datetime(2000,1,1)
    runParameters[evalrunner.EvalRunner.endDateKey] = datetime.datetime.now()

    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = True
    
    #runParameters[evalbase.EvalBase.maxLossKey] = -0.04
    runParameters[evalbase.EvalBase.endTransactionCalcKey] = transactionchecker.EndTransactionCheckerMulit( -0.04, 0.5, 5, True)
    runParameters[evalrunner.EvalRunner.transactionPrinterKey] = EvalBestTransactionPrinter()
    runParameters[evalrunner.EvalRunner.resultPrinterKey] = evalrunner.EvalResultPrinterSimple()   

    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 12

    evaluation = evalbest.EvalBestRunner(runParameters)
    evaluation.run( "evaluate best", indexdatabase.IndexDatabase.allIndices )
