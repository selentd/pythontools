
import datetime

import pymongo
from pymongo.mongo_client import MongoClient

import indexdata
from indexdata import IndexData

def evalIndex( source, dbName, indexName ):
    client = MongoClient()
    database = client[dbName]
    collection = database[indexName]
    indexData = collection.find( {"date" : { "$gt" : datetime.datetime(2003, 12, 31)} }).sort("date")
    
    indexHistory = indexdata.IndexHistory()
    for indexDictEntry in indexData:
        indexEntry = IndexData().setDictionary(indexDictEntry)
        indexHistory.addIndexData(indexEntry)
       
def evalIndizes():
    indexList = ['dax',
                 'estoxx50',
                 'ftse100',
                 'mdax',
                 'nikkei225',
                 'smi',
                 'sp500']

    evalIndex('../result/estoxx50.csv', 'indexdb', 'estoxx50')
    
    

if __name__ == '__main__':
    evalIndizes() 


