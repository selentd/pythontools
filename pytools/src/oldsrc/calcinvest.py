

import evalmean
import evalmeangradient
import evalmeanorder
import evalwin
import pymongo
import csv

from indexdata import IndexHistory
from evalstrategie import EvalStrategie
from evalresult import EvalResultCall
from evalresult import EvalResultPut
from resultdata import IndexResultHistory

def evalFinalPut( index, resultFile ):
    maxLoss = -1.0
    evalStrategies = list()    

    evalStrategies.append(EvalStrategie('Mean38_89Put/Grad13-89-sell89or200',
                                        [evalmean.EvalMean38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMeanGradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))

    evalStrategies.append(EvalStrategie('Mean38_89Put/Grad13-89Mean-sell89or200',
                                        [evalmean.EvalMean38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMean89GradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))

    evalStrategies.append(EvalStrategie('Mean38_89Put/Grad13-89Mean38-sell89or200',
                                        [evalmean.EvalMean38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMean89GradientPutBuy(89, 38)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    
    evalStrategies.append(EvalStrategie('Mean38_89Put/Grad13-89Mean-sell38or89or200',
                                        [evalmean.EvalMean38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMean89GradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean38PutSell(),
                                         evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))

    evalStrategies.append(EvalStrategie('Mean13_38_89Put/Grad13-89-sell89or200',
                                        [evalmean.EvalMean13_38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMeanGradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))

    evalStrategies.append(EvalStrategie('Mean13_38_89Put/Grad13-89Mean-sell89or200',
                                        [evalmean.EvalMean13_38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMean89GradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))

    evalStrategies.append(EvalStrategie('Mean13_38_89Put/Grad13-89Mean38-sell89or200',
                                        [evalmean.EvalMean13_38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMean89GradientPutBuy(89, 38)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))

    evalStrategies.append(EvalStrategie('Mean13_38_89Put/Grad13-89Mean-sell38or89or200',
                                        [evalmean.EvalMean13_38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(13, 13),
                                         evalmeangradient.EvalMean89GradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean38PutSell(),
                                         evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))

    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultPut(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print str.format('{:45} {:>4} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>10.2f}', 
                   resultData.name,
                   resultData.getTotalCount(),
                   resultData.getWinRatio(),
                   resultData.maxWin,
                   resultData.maxLoss,
                   resultData.getMeanWin(),
                   resultData.getMeanLoss(),
                   resultData.sumWin+resultData.sumLoss,
                   resultData.sumWinEuro+resultData.sumLossEuro)

        with open(resultFile, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            csvWrite.writerow( (resultData.name,
                                resultData.getTotalCount(),
                                resultData.getWinRatio(),
                                resultData.maxWin,
                                resultData.maxLoss,
                                resultData.getMeanWin(),
                                resultData.getMeanLoss(),
                                resultData.sumWin+resultData.sumLoss,
                                resultData.sumWinEuro+resultData.sumLossEuro) )

def evalFinalCall( index, resultFile ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Buy',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean38_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))

    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Buy-strict',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeanorder.EvalMeanOrder38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean38_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))

    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell89',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))

    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell89-strict',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeanorder.EvalMeanOrder38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))

    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultCall(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print str.format('{:35} {:>4} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>10.2f}', 
                   resultData.name,
                   resultData.getTotalCount(),
                   resultData.getWinRatio(),
                   resultData.maxWin,
                   resultData.maxLoss,
                   resultData.getMeanWin(),
                   resultData.getMeanLoss(),
                   resultData.sumWin+resultData.sumLoss,
                   resultData.sumWinEuro+resultData.sumLossEuro)

        with open(resultFile, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            csvWrite.writerow( (resultData.name,
                                resultData.getTotalCount(),
                                resultData.getWinRatio(),
                                resultData.maxWin,
                                resultData.maxLoss,
                                resultData.getMeanWin(),
                                resultData.getMeanLoss(),
                                resultData.sumWin+resultData.sumLoss,
                                resultData.sumWinEuro+resultData.sumLossEuro) )
    
def evaluateMean89_Put( index, resultFile ):
    maxLoss = -1.0
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean89Put',
                                        [evalmean.EvalMean89PutBuy()], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    evalStrategies.append(EvalStrategie('Mean89Put/Grad89',
                                        [evalmean.EvalMean89PutBuy(),
                                         evalmeangradient.EvalMeanGradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    evalStrategies.append(EvalStrategie('Mean89_200Put',
                                        [evalmean.EvalMean89_200PutBuy()], 
                                        [evalmean.EvalMean89_200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    evalStrategies.append(EvalStrategie('Mean89_200Put/Grad89',
                                        [evalmean.EvalMean89_200PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89_200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    evalStrategies.append(EvalStrategie('Mean89_200Put-sell89or200',
                                        [evalmean.EvalMean89_200PutBuy()], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    evalStrategies.append(EvalStrategie('Mean89_200Put/Grad89-sell89or200',
                                        [evalmean.EvalMean89_200PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    evalStrategies.append(EvalStrategie('Mean13_38_89Put-Sell89_200',
                                        [evalmean.EvalMean13_38_89PutBuy()], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    evalStrategies.append(EvalStrategie('Mean13_38_89Put/Grad89',
                                        [evalmean.EvalMean13_38_89PutBuy(), 
                                         evalmeangradient.EvalMeanGradientPutBuy(89, 89)], 
                                        [evalmean.EvalMean89PutSell(),
                                         evalmean.EvalMean200PutSell(),
                                         evalwin.EvalWinSellPut(maxLoss)]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultPut(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print str.format('{:35} {:>4} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>10.2f}', 
                   resultData.name,
                   resultData.getTotalCount(),
                   resultData.getWinRatio(),
                   resultData.maxWin,
                   resultData.maxLoss,
                   resultData.getMeanWin(),
                   resultData.getMeanLoss(),
                   resultData.sumWin+resultData.sumLoss,
                   resultData.sumWinEuro+resultData.sumLossEuro)

        with open(resultFile, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            csvWrite.writerow( (resultData.name,
                                resultData.getTotalCount(),
                                resultData.getWinRatio(),
                                resultData.maxWin,
                                resultData.maxLoss,
                                resultData.getMeanWin(),
                                resultData.getMeanLoss(),
                                resultData.sumWin+resultData.sumLoss,
                                resultData.sumWinEuro+resultData.sumLossEuro) )

    
def evaluateMean38Single( index, resultFile ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Buy',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean38_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell13',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean13CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell38',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean38CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell89',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell38or89',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean38CallSell(),
                                         evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell13or38',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean13CallSell(),
                                         evalmean.EvalMean38CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell13or89',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean13CallSell(),
                                         evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89-Sell38or89',
                                        [evalmean.EvalMean38_89CallBuy()], 
                                        [evalmean.EvalMean38CallSell(),
                                         evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Sell13or89',
                                        [evalmean.EvalMean38_89CallBuy()], 
                                        [evalmean.EvalMean13CallSell(),
                                         evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultCall(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print str.format('{:35} {:>4} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>10.2f}', 
                   resultData.name,
                   resultData.getTotalCount(),
                   resultData.getWinRatio(),
                   resultData.maxWin,
                   resultData.maxLoss,
                   resultData.getMeanWin(),
                   resultData.getMeanLoss(),
                   resultData.sumWin+resultData.sumLoss,
                   resultData.sumWinEuro+resultData.sumLossEuro)

        with open(resultFile, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            csvWrite.writerow( (resultData.name,
                                resultData.getTotalCount(),
                                resultData.getWinRatio(),
                                resultData.maxWin,
                                resultData.maxLoss,
                                resultData.getMeanWin(),
                                resultData.getMeanLoss(),
                                resultData.sumWin+resultData.sumLoss,
                                resultData.sumWinEuro+resultData.sumLossEuro) )

def evaluateMean38( index ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean38',
                                        [evalmean.EvalMean38CallBuy()], 
                                        [evalmean.EvalMean38CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38/Gradient3-Buy',
                                        [evalmean.EvalMean38CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(3, 3)], 
                                        [evalmean.EvalMean38CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38/Gradient5-Buy',
                                        [evalmean.EvalMean38CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(5, 5)], 
                                        [evalmean.EvalMean38CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient5-Buy',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(5, 5)], 
                                        [evalmean.EvalMean38_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Buy',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean38_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Buy-Sell13_89',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean13_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89',
                                        [evalmean.EvalMean38_89CallBuy()], 
                                        [evalmean.EvalMean38_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/13_89',
                                        [evalmean.EvalMean38_89CallBuy()], 
                                        [evalmean.EvalMean13_89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    evalStrategies.append(EvalStrategie('Mean38_89/13_38/Gradient13-Buy',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean13_38CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultCall(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print str.format('{:35} {:>4} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>10.2f}', 
                   resultData.name,
                   resultData.getTotalCount(),
                   resultData.getWinRatio(),
                   resultData.maxWin,
                   resultData.maxLoss,
                   resultData.getMeanWin(),
                   resultData.getMeanLoss(),
                   resultData.sumWin+resultData.sumLoss,
                   resultData.sumWinEuro+resultData.sumLossEuro)
        
        #print  , resultData.sumWin+resultData.sumLoss

def evaluateMean13( index ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean13',
                                        [evalmean.EvalMean13CallBuy()], 
                                        [evalmean.EvalMean13CallSell()]))
    evalStrategies.append(EvalStrategie('Mean13/Gradient5-Buy',
                                        [evalmean.EvalMean13CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(5, 5)], 
                                        [evalmean.EvalMean13CallSell()]))
    evalStrategies.append(EvalStrategie('Mean13/Gradient13-Buy',
                                        [evalmean.EvalMean13CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean13CallSell()]))
    evalStrategies.append(EvalStrategie('Mean13/Gradient13-Sell',
                                        [evalmean.EvalMean13CallBuy()], 
                                        [evalmean.EvalMean13CallSell(),
                                         evalmeangradient.EvalMeanGradientCallSell(13, 13)]))
    evalStrategies.append(EvalStrategie('Mean13/Gradient13/5-Sell',
                                        [evalmean.EvalMean13CallBuy()], 
                                        [evalmean.EvalMean13CallSell(),
                                         evalmeangradient.EvalMeanGradientCallSell(5, 5)]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultCall(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print resultData.name, resultData.getTotalCount(), resultData.getWinRatio(), resultData.maxWin, resultData.maxLoss, resultData.getMeanWin(), resultData.getMeanLoss(), resultData.sumWin+resultData.sumLoss

def evaluateMean5( index ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean5',
                                        [evalmean.EvalMean5CallBuy()], 
                                        [evalmean.EvalMean5CallSell()]))
    evalStrategies.append(EvalStrategie('Mean5/Gradient5-Buy',
                                        [evalmean.EvalMean5CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(5, 5)], 
                                        [evalmean.EvalMean5CallSell()]))
    evalStrategies.append(EvalStrategie('Mean5/Gradient5-Sell',
                                        [evalmean.EvalMean5CallBuy()], 
                                        [evalmean.EvalMean5CallSell(),
                                         evalmeangradient.EvalMeanGradientCallSell(5, 5)]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultCall(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print resultData.name, resultData.getTotalCount(), resultData.getWinRatio(), resultData.maxWin, resultData.maxLoss, resultData.getMeanWin(), resultData.getMeanLoss(), resultData.sumWin+resultData.sumLoss

def evaluateMean5_200( index ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean5_200',
                                        [evalmean.EvalMean5_200CallBuy()], 
                                        [evalmean.EvalMean5_200CallSell()]))
    evalStrategies.append(EvalStrategie('Mean5_200/Gradient5-Buy',
                                        [evalmean.EvalMean5_200CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(5, 5)], 
                                        [evalmean.EvalMean5_200CallSell()]))
    evalStrategies.append(EvalStrategie('Mean5_200/Gradient5-Sell',
                                        [evalmean.EvalMean5_200CallBuy()], 
                                        [evalmean.EvalMean5_200CallSell(),
                                         evalmeangradient.EvalMeanGradientCallSell(5, 5)]))
    evalStrategies.append(EvalStrategie('Mean5_200/Gradient5-Buy-Sell',
                                        [evalmean.EvalMean5_200CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(5, 5)], 
                                        [evalmean.EvalMean5_200CallSell(),
                                         evalmeangradient.EvalMeanGradientCallSell(5, 5)]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultCall(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print resultData.name, resultData.getTotalCount(), resultData.getWinRatio(), resultData.maxWin, resultData.maxLoss, resultData.getMeanWin(), resultData.getMeanLoss(), resultData.sumWin+resultData.sumLoss
    
def evaluateSimpleCall( index ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean5',
                                        [evalmean.EvalMean5CallBuy()], 
                                        [evalmean.EvalMean5CallSell()]))
    evalStrategies.append(EvalStrategie('Mean13',
                                        [evalmean.EvalMean13CallBuy()], 
                                        [evalmean.EvalMean13CallSell()]))
    evalStrategies.append(EvalStrategie('Mean38',
                                        [evalmean.EvalMean38CallBuy()], 
                                        [evalmean.EvalMean38CallSell()]))
    evalStrategies.append(EvalStrategie('Mean89',
                                        [evalmean.EvalMean89CallBuy()], 
                                        [evalmean.EvalMean89CallSell()]))
    evalStrategies.append(EvalStrategie('Mean200',
                                        [evalmean.EvalMean200CallBuy()], 
                                        [evalmean.EvalMean200CallSell()]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultCall(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print resultData.name, resultData.getTotalCount(), resultData.getWinRatio(), resultData.maxWin, resultData.maxLoss, resultData.getMeanWin(), resultData.getMeanLoss(), resultData.sumWin+resultData.sumLoss
        
def evaluateSimplePut( index ):
    evalStrategies = list()    
    evalStrategies.append(EvalStrategie('Mean5',
                                        [evalmean.EvalMean5PutBuy()], 
                                        [evalmean.EvalMean5PutSell()]))
    evalStrategies.append(EvalStrategie('Mean13',
                                        [evalmean.EvalMean13PutBuy()], 
                                        [evalmean.EvalMean13PutSell()]))
    evalStrategies.append(EvalStrategie('Mean38',
                                        [evalmean.EvalMean38PutBuy()], 
                                        [evalmean.EvalMean38PutSell()]))
    evalStrategies.append(EvalStrategie('Mean89',
                                        [evalmean.EvalMean89PutBuy()], 
                                        [evalmean.EvalMean89PutSell()]))
    evalStrategies.append(EvalStrategie('Mean200',
                                        [evalmean.EvalMean200PutBuy()], 
                                        [evalmean.EvalMean200PutSell()]))
    
    for strategie in evalStrategies:
        resultHistory = IndexResultHistory()
        resultData = EvalResultPut(strategie.name)
        
        strategie.evaluateIndex(index, resultHistory)
        resultHistory.evaluateResult(resultData)
        print str.format('{:35} {:>4} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f}', 
                   resultData.name,
                   resultData.getTotalCount(),
                   resultData.getWinRatio(),
                   resultData.maxWin,
                   resultData.maxLoss,
                   resultData.getMeanWin(),
                   resultData.getMeanLoss(),
                   resultData.sumWin+resultData.sumLoss)
            
def evaluateIndex( sourceFile, resultFile):
    for source in sourceFile:
        index = IndexHistory( source, 260*10)                  
        index.readIndex()
        print source, 'index days:', len(index.indexHistory)
        #evaluateMean89_Put( index, resultFile )
        
        with open(resultFile, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            csvWrite.writerow( (source, 0, 0, 0, 0, 0, 0, 0, 0) )
        
        #evaluateSimplePut( index )
        #evalFinalCall( index, resultFile )
        evalFinalPut( index, resultFile )
    
def evaluateIndizes():
    indexList = ['/home/dieter/Dokumente/Finanzen/Indizes/cac.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/dax.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/estoxx50.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/ftse100.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/ftsemib.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/hangseng.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/kospi.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/mdax.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/nasdaq100.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/nikkei.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/smi.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/sp500.csv',
                 '/home/dieter/Dokumente/Finanzen/Indizes/tecdax.csv']
    evaluateIndex( indexList, '../data/result.csv')
    
if __name__ == '__main__':
    evaluateIndizes() 