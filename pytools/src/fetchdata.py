'''
Created on 15.02.2015

@author: diesel
'''

import datetime
import csv
import collections

import pymongo
from pymongo.mongo_client import MongoClient

from IndexEval.indexdata import IndexData

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
        resultHistory = collections.deque()
        
        for entry in self.collection.find({'date': {'$gte': self.startDate, '$lt': self.endDate} }).sort('date'):    
            indexEntry = IndexData()
            indexEntry.set(entry['date'], entry['open'], entry['close'], entry['high'], entry['low'])
            indexEntry.setMeanValues(entry['mean5'], entry['mean13'],entry['mean38'], entry['mean89'], entry['mean200'])
            resultHistory.append(indexEntry)
         
        return resultHistory
    
    def fetchDataByDate(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        return fetchData

if __name__ == '__main__':
    start = datetime.datetime(1998, 01, 02, 0, 0);
    end = datetime.datetime(1998, 02, 01, 0, 0)
                                       
    fetchData = FetchData('stockdb', 'dax',)
    fetchData.fetchDataByDate( start, end ) 
           