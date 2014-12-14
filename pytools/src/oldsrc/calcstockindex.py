'''
Created on 13.12.2014

@author: diesel
'''

import datetime
import csv

import pymongo
from pymongo.mongo_client import MongoClient

from resultdata import IndexResultHistory
from evalstrategie import EvalStrategie
from evalresult import EvalResultCall

from indexdata import IndexData

import evalcallmw200

def evalStockIndex( collection, strategie, startDate ):
    resultHistory = IndexResultHistory()
    for entry in collection.find( {'date': {'$gt': startDate, '$lt' : startDate.replace(startDate.year+30)}}).sort('date'):    
        indexEntry = IndexData()
        indexEntry.set(entry['date'], entry['open'], entry['close'], entry['high'], entry['low'])
        indexEntry.setMeanValues(entry['mean5'], entry['mean13'],entry['mean38'], entry['mean89'], entry['mean200'])
        
        strategie.evaluate( indexEntry, resultHistory )
        
    return resultHistory


def calcStockIndex( dbName, indexName, strategieList, startDate):
    client = MongoClient()
    database = client[dbName]
    collection = database[indexName]
    
    resultList = list()
    for strategie in strategieList:
        resultList.append( evalStockIndex( collection, strategie, startDate ) )
        
    for resultHistory in resultList:
        resultData = EvalResultCall('result', 1000, 1000, 10)
        resultHistory.evaluateResult(resultData)
        print str.format('{:35} {:>4} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} {:>10.2f}', 
                   resultData.name+' '+str(startDate),
                   resultData.getTotalCount(),
                   resultData.getWinRatio(),
                   resultData.maxWin,
                   resultData.maxLoss,
                   resultData.getMeanWin(),
                   resultData.getMeanLoss(),
                   resultData.sumWin+resultData.sumLoss,
                   resultData.sumWinEuro+resultData.sumLossEuro)
        
def getEvalDatesMonth( year ):
    dateList = list()
    dateList.append(datetime.datetime(year, 1, 1))
    dateList.append(datetime.datetime(year, 2, 1))
    dateList.append(datetime.datetime(year, 3, 1))
    dateList.append(datetime.datetime(year, 4, 1))
    dateList.append(datetime.datetime(year, 5, 1))
    dateList.append(datetime.datetime(year, 6, 1))
    dateList.append(datetime.datetime(year, 7, 1))
    dateList.append(datetime.datetime(year, 8, 1))
    dateList.append(datetime.datetime(year, 9, 1))
    dateList.append(datetime.datetime(year, 10, 1))
    dateList.append(datetime.datetime(year, 11, 1))
    dateList.append(datetime.datetime(year, 12, 1))
    return dateList
    
        
def getEvalDates():
    dateList = list()
    dateList += getEvalDatesMonth(1993)
    dateList += getEvalDatesMonth(1994)
    dateList += getEvalDatesMonth(1995)
    dateList += getEvalDatesMonth(1996)
    dateList += getEvalDatesMonth(1997)
    dateList += getEvalDatesMonth(1998)
    dateList += getEvalDatesMonth(1999)
    dateList += getEvalDatesMonth(2000)
    dateList += getEvalDatesMonth(2001)
    dateList += getEvalDatesMonth(2002)
    dateList += getEvalDatesMonth(2003)
    dateList += getEvalDatesMonth(2004)
    dateList += getEvalDatesMonth(2005)
    dateList += getEvalDatesMonth(2006)
    dateList += getEvalDatesMonth(2007)
    dateList += getEvalDatesMonth(2008)
    dateList += getEvalDatesMonth(2009)
    dateList += getEvalDatesMonth(2010)
    dateList += getEvalDatesMonth(2011)
    dateList += getEvalDatesMonth(2012)
    dateList += getEvalDatesMonth(2013)
    dateList.append(datetime.datetime(2014, 01, 01))
    return dateList
    
    
def getFirstStartDate( index ):

    if index == 'dax':
        return datetime.datetime(1991, 9, 17)    
        
    if index == 'estoxx50':
        return datetime.datetime(2003, 3, 13)
    
    if index == 'mdax':
        return datetime.datetime(1991, 7, 26)
        
    if index == 'nasdaq100':
        return datetime.datetime(1986, 7, 17)
        
    if index == 'nikkei':
        return datetime.datetime(1984,10, 18)
        
    if index == 'smi':
        return datetime.datetime(1991, 9, 2)
        
    if index == 'sp500':
        return datetime.datetime(1950, 10, 19)
        
    if index == 'tecdax':
        return datetime.datetime(2001, 10, 26)
    
            
    return datetime.datetime.today()

def getStrategieList():
    strategieList = list()    
    strategieList.append(EvalStrategie('Call MW200 + 1% / Sell MW200 - 3%',
                                        [evalcallmw200.EvalCallMW200MeanBuy( 1.0 )], 
                                        [evalcallmw200.EvalCallMW200MeanSell( -3.0 )]))
    return strategieList
            
def calcStockIndizes():
    evalDates = getEvalDates()
#    startDate = datetime.datetime(2005, 1, 1)
#    calcStockIndex('stockdb', 'dax', strategieList, startDate)
    for startDate in evalDates:
        calcStockIndex( 'stockdb', 'sp500', getStrategieList(), startDate)
    
if __name__ == '__main__':
    calcStockIndizes()