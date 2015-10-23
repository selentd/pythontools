'''
Created on 15.02.2015

@author: diesel
'''

import datetime

from pymongo.mongo_client import MongoClient

from indexdata import IndexData, IndexHistory

def _selectTrue( idxData ):
    return True

class FetchData():
    '''
    classdocs
    '''

    def __init__(self, dbName, indexName):
        '''
        Constructor
        '''
        self.dbName = dbName
        self.indexName = indexName
        self.startDate = datetime.datetime(1900, 01, 01)
        self.endDate = datetime.datetime.today()
        self.selectFunc = _selectTrue

    def _fetchData(self, select):
        self.client = MongoClient()
        self.database = self.client[self.dbName]
        self.collection = self.database[self.indexName]
        self.selectFunc = select

        history = IndexHistory()

        for entry in self.collection.find({'date': {'$gte': self.startDate, '$lt': self.endDate} }).sort('date'):
            indexEntry = IndexData()
            indexEntry.setDictionary(entry)
            if self.selectFunc( indexEntry ):
                history.addIndexData(indexEntry)

        return history

    '''
    Get a index history by date.
    '''
    def fetchDataByDate(self, startDate, endDate, select=_selectTrue ):
        self.startDate = startDate
        self.endDate = endDate
        return self._fetchData( select )

    '''
    Get the index history for one month
    '''
    def fetchDataByMonth(self, year, month, select=_selectTrue ):
        self.startDate = datetime.datetime( year, month, 1)
        if month == 12:
            self.endDate = datetime.datetime( year + 1, 1, 1)
        else:
            self.endDate = datetime.datetime( year, month+1, 1)
        return self._fetchData( select )

    '''
    Get a list of monthly index histories
    '''
    def fetchMonthlyHistory(self, startDate, endDate, select=_selectTrue):
        def _getNextMonth(year, month):
            if month == 12:
                year = year + 1
                month = 1
            else:
                month += 1

            return( year, month )

        def _getFirstMonth(startDate):
            return( startDate.year, startDate.month )

        def _isEndOfPeriod(year, month, endDate):
            checkIsEndOfPeriod = False
            checkIsEndOfPeriod = (year >= endDate.year)
            checkIsEndOfPeriod = checkIsEndOfPeriod and (month >= endDate.month)
            return checkIsEndOfPeriod

        # --- start of function ---

        monthlyHistory = list()
        currentPeriod = _getFirstMonth( startDate )

        while not (_isEndOfPeriod(currentPeriod[0], currentPeriod[1], endDate)):
            indexHistory = self.fetchDataByMonth(currentPeriod[0], currentPeriod[1], select)
            if indexHistory.len() > 0:
                monthlyHistory.append( indexHistory )
            currentPeriod = _getNextMonth(currentPeriod[0], currentPeriod[1])

        return monthlyHistory



if __name__ == '__main__':
    start = datetime.datetime(1998, 01, 02, 0, 0);
    end = datetime.datetime(1998, 02, 01, 0, 0)

    fetchData = FetchData('stockdb', 'dax',)
    fetchData.fetchDataByDate( start, end )
