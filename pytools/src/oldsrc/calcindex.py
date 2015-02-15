'''
Created on 26.01.2014

@author: dieter
'''

import datetime
import csv

import pymongo
from pymongo.mongo_client import MongoClient

import evalmean
import evalmeangradient
import evalmeanorder
import evalwin

from indexdata import IndexData
from resultdata import IndexResultHistory
from evalstrategie import EvalStrategie
from evalresult import EvalResultCall, EvalResultPut

import evalcallmw200

def writeIndex( csvWrite, entry):
    dateString = entry['date'].strftime("%d.%m.%y")
    csvWrite.writerow( (dateString,
                        entry['close']) )
    
def evalIndex( collection, strategie, startDate ):

    resultHistory = IndexResultHistory()
#    for entry in collection.find().sort('date'):    
    for entry in collection.find({'date': {'$gt': startDate}}).sort('date'):    
        indexEntry = IndexData()
        indexEntry.set(entry['date'], entry['open'], entry['close'], entry['high'], entry['low'])
        indexEntry.setMeanValues(entry['mean5'], entry['mean13'],entry['mean38'], entry['mean89'], entry['mean200'])
        
        strategie.evaluate( indexEntry, resultHistory )
        
    return resultHistory
        
def getStrategieList():
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
    return evalStrategies

def getStrategieListSingle():
    evalStrategies = list()
#   Basic    
    evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell89-strict',
                                        [evalmean.EvalMean38_89CallBuy(),
                                         evalmeanorder.EvalMeanOrder38_89CallBuy(),
                                         evalmeangradient.EvalMeanGradientCallBuy(13, 13)], 
                                        [evalmean.EvalMean89CallSell(),
                                         evalwin.EvalWinSellCall(-2.0)]))      
#   Strict
    #evalStrategies.append(EvalStrategie('Mean38_89/Gradient13-Sell89-strict',
    #                                    [evalmean.EvalMean89_200CallBuy()],
    #                                    [evalmean.EvalMean89CallSell(),
    #                                     evalmean.EvalMean89_200CallSell(),
    #                                     evalwin.EvalWinSellCall(-2.0)]))      

    
    return evalStrategies

def exportResult( indexResult, writer ):  
    #writer.writerow(('Type', 'Date', 'Low', 'Close', 'Mean5', 'Mean13', 'Mean38', 'Mean89', 'Mean200'))
    dateString = indexResult.indexBuy.date.strftime("%d.%m.%y")
    writer.writerow( ('Buy', 
                      dateString,
                      indexResult.indexBuy.low, 
                      indexResult.indexBuy.close,
                      indexResult.indexBuy.mean5,
                      indexResult.indexBuy.mean13,
                      indexResult.indexBuy.mean38,
                      indexResult.indexBuy.mean89,
                      indexResult.indexBuy.mean200) )
    indexBuy = indexResult.indexBuy.close
    indexStart = indexBuy
    
    for indexData in indexResult.indexHistory:
        result = indexData.close / indexBuy
        result -= 1.0
        resultStart = indexData.close / indexStart
        resultStart -= 1.0
        dateString = indexData.date.strftime("%d.%m.%y")
        if result > 0.01:
            win = 1000 * result * 40
            writer.writerow( ('History', 
                              dateString, 
                              indexData.low,
                              indexData.close,
                              indexData.mean5,
                              indexData.mean13,
                              indexData.mean38,
                              indexData.mean89,
                              indexData.mean200) )
            indexBuy = indexData.close
        elif result < -0.02:
            loss = -1000.0            
            writer.writerow( ('History', 
                              dateString, 
                              indexData.low,
                              indexData.close,
                              indexData.mean5,
                              indexData.mean13,
                              indexData.mean38,
                              indexData.mean89,
                              indexData.mean200) )
            indexBuy = indexData.close
        else:
            writer.writerow( ('History', 
                              dateString, 
                              indexData.low,
                              indexData.close,
                              indexData.mean5,
                              indexData.mean13,
                              indexData.mean38,
                              indexData.mean89,
                              indexData.mean200) )

    result = indexResult.indexSell.close / indexBuy
    result -= 1.0
    win = 1000 * result * 40
    if win < -1000.0:
        win = -1000.0
    if win < -0.02:
        win = -1000.0
    resultStart = indexResult.indexSell.close / indexStart
    resultStart -= 1.0
        
    dateString = indexResult.indexSell.date.strftime("%d.%m.%y")
    writer.writerow( ('Sell', 
                      dateString, 
                      indexResult.indexSell.low,
                      indexResult.indexSell.close,
                      indexResult.indexSell.mean5,
                      indexResult.indexSell.mean13,
                      indexResult.indexSell.mean38,
                      indexResult.indexSell.mean89,
                      indexResult.indexSell.mean200) )

def calcIndex( destination, dbName, indexName ):
    client = MongoClient()
    database = client[dbName]
    collection = database[indexName]
    
    resultList = list()
    strategieList = getStrategieListSingle()
    for strategie in strategieList:
        resultList.append( evalIndex( collection, strategie ) )
        
    for resultHistory in resultList:
        resultData = EvalResultCall('result')
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
        
        with open(destination, "ab") as ofile:
            csvWrite = csv.writer( ofile )
            resultHistory.exportResult( exportResult, csvWrite )
        
    
def calcIndizes():
    indexList = ['../data/result/dax.csv',
                 '../data/result/estoxx50.csv',
                 '../data/result/ftse100.csv',
                 '../data/result/mdax.csv',
                 '../data/result/nikkei225.csv',
                 '../data/result/smi.csv',
                 '../data/result/sp500.csv']

    calcIndex('../../data/result/dax_basic.csv', 'stockdb', 'dax')
    
    
    
if __name__ == '__main__':
    calcIndizes() 
