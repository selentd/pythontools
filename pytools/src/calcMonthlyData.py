'''
Created on 15.02.2015

@author: diesel
'''

import datetime

from IndexEval.fetchdata import FetchData
from IndexEval.indexdata import IndexData 
from IndexEval.indexrangedata import IndexRangeData

def getNextMonth(startDate):
    if startDate.month < 12:
        return datetime.datetime(startDate.year, startDate.month+1, startDate.day)
    else:
        return datetime.datetime(startDate.year+1, 1, startDate.day)
    
def getIndexMonthlyData( dbName, index, startDate, endDate):
    indexRangeList = list()
    fetchData = FetchData(dbName, index)
    nextDate = getNextMonth(startDate)
    
    while startDate < endDate:
        rangeData = IndexRangeData()
        
        resultList = fetchData.fetchDataByDate(startDate, nextDate)
        rangeData.setData(resultList)
        indexRangeList.append(rangeData)
        startDate=nextDate
        nextDate = getNextMonth(startDate)
        
    return indexRangeList
    
def exportMonthlyData( dbName, indexList, startDate, endDate):
    indexResultList = list()
    
    for index in indexList:
        indexResultList.append(getIndexMonthlyData(dbName, index, startDate, endDate))

if __name__ == '__main__':
    databaseName = 'stockdb'
    indexList = ['dax',
                 'estoxx50',
                 'mdax',
                 'nasdaq100'
                 'nikkei',
                 'smi',
                 'sp500',
                 'tecdax']
    startDate = datetime.datetime(1998, 01, 01)
    endDate = datetime.datetime.today()
    
    exportMonthlyData(databaseName, indexList, startDate, endDate)
    
    
    