'''
Created on 15.02.2015

@author: diesel
'''

import datetime
import csv
import collections

import pymongo
from pymongo.mongo_client import MongoClient

from indexdata import IndexData, IndexHistory

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

    def fetchData(self):
        self.client = MongoClient()
        self.database = self.client[self.dbName]
        self.collection = self.database[self.indexName]
        history = IndexHistory()

        for entry in self.collection.find({'date': {'$gte': self.startDate, '$lt': self.endDate} }).sort('date'):
            indexEntry = IndexData()
            indexEntry.setDictionary(entry)
            history.addIndexData(indexEntry)

        return history

    def fetchDataByDate(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        return self.fetchData()

if __name__ == '__main__':
    start = datetime.datetime(1998, 01, 02, 0, 0);
    end = datetime.datetime(1998, 02, 01, 0, 0)

    fetchData = FetchData('stockdb', 'dax',)
    fetchData.fetchDataByDate( start, end )
