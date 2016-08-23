'''
Created on 15.02.2015

@author: diesel
'''

import datetime

from indexdata import IndexData, IndexHistory

import indexdatabase

def _selectTrue( idxData ):
    return True

class FetchData():
    '''
    classdocs
    '''

    def __init__(self, indexName):
        '''
        Constructor
        '''
        self.indexName = indexName
        self.startDate = datetime.datetime(1900, 01, 01)
        self.endDate = datetime.datetime.today()
        self.selectFunc = _selectTrue

        self.indexDB = indexdatabase.getIndexDatabase()
        self.collection = self.indexDB.getIndexCollection(self.indexName)
        self.selectFunc = _selectTrue

    def _fetchData(self, select):
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

    def fetchSelectedHistory(self, startDate, endDate, startFunc, endFunc):
        isInTransaction = False
        meanHistoryList = list()
        idxHistory = IndexHistory()

        for idxData in self.collection.find({'date': {'$gte': self.startDate, '$lt': self.endDate} }).sort('date'):
            if isInTransaction:
                if endFunc.checkEndTransaction( idxData, idxHistory.len() ):
                    meanHistoryList.append( idxHistory )
                    isInTransaction = False
                else:
                    idxHistory.addIndexData( idxData )


            if not isInTransaction:
                if startFunc.checkStartTransaction( idxData ):
                    isInTransaction = True
                    idxHistory = IndexHistory()
                    idxHistory.addIndexData( idxData )
                    endFunc.reset( idxData )

        if isInTransaction:
            meanHistoryList.append( idxHistory )

        return meanHistoryList

    def fetchHistoryValue(self, year, month, day):
        searchDate = datetime.datetime( year, month, day )
        startDate = searchDate
        startDate = startDate + datetime.timedelta(-1)
        hasEntry = False
        idxEntry = IndexData()

        '''
        if self.collection.find_one({'date': {'$lt': searchDate} }) != None:
            entry = None
            while entry == None:
                entry = self.collection.find_one({'date': {'$gte': startDate, '$lt': searchDate} })
                if entry == None:
                    startDate = startDate + datetime.timedelta(-1)

            idxEntry = IndexData()
            idxEntry.setDictionary(entry)
            return idxEntry
        else:
            return None
        '''
        for entry in self.collection.find({'date' : {'$lt': searchDate}}).sort('date', -1).limit(1):
            idxEntry.setDictionary(entry)
            hasEntry = True

        if hasEntry:
            return idxEntry
        else:
            return None

    def fetchLastDayOfMonth(self, year, month):
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month+1

        return self.fetchHistoryValue( year, month, 1)

if __name__ == '__main__':
    start = datetime.datetime(1998, 01, 02, 0, 0);
    end = datetime.datetime(1998, 02, 01, 0, 0)

    fetchData = FetchData( 'dax',)
    fetchData.fetchDataByDate( start, end )
