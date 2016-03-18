
import datetime

import pymongo
from pymongo.mongo_client import MongoClient

import indexdata

def getIndexEntry( indexData ):
    return indexData.getDictionary()

def getIndexDateEntry( indexData ):
    return { "date": datetime.datetime(indexData.date.year,
                                       indexData.date.month,
                                       indexData.date.day,
                                       0,
                                       0)
            }

def getIndexHistory( source, size = 1000000 ):
    indexHistory = indexdata.IndexHistory(source, size)
    indexHistory.readIndex()
    return indexHistory

def addIndex( source, dbName, indexName ):
    client = MongoClient()
    database = client[dbName]
    collection = database[indexName]
    collection.create_index([("date", pymongo.ASCENDING)],
                            name="date",
                            unique=True)
    indexHistory = getIndexHistory(source)
    for indexData in indexHistory.indexHistory:
        indexEntry = getIndexEntry(indexData)
        indexDate = getIndexDateEntry(indexData)
        if collection.find_one(indexDate) == None:
            collection.insert(indexEntry)

def addIndizes():
    '''
    addIndex('../../data/smi.csv', 'stockdb', 'smi')
    '''
    indexList = ['atx',
                 'cac',
                 'dax',
                 'dowjones',
                 'estoxx50',
                 'ftse100',
                 'ftsemib',
                 'hangseng',
                 'ibex',
                 'mdax',
                 'nasdaq100',
                 'nikkei',
                 'sdax',
                 'smi',
                 'sp500',
                 'tecdax']

    for index in indexList:
        print '../../data/'+index+'.csv'
        addIndex('../../data/'+index+'.csv', 'stockdb', index)



if __name__ == '__main__':
    addIndizes()


