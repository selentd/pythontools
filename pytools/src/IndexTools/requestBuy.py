'''
Created on 22.04.2016

@author: selen00r
'''

import datetime

from pymongo.mongo_client import MongoClient

import indexdata

class IndexDatabase:

    def __init__(self):
        '''
        Constructor
        '''
        self.dbName = "stockdb"

        self.idxATX         = "atx"
        self.idxCAC         = "cac"
        self.idxDax         = "dax"
        self.idxDowJones    = "dowjones"
        self.idxEStoxx50    = "estoxx50"
        self.idxFTS100      = "ftse100"
        self.idxFtseMib     = "ftsemib"
        self.idxHangSeng    = "hangseng"
        self.idxIbex        = "ibex"
        self.idxMDax        = "mdax"
        self.idxNasdaq100   = "nasdaq100"
        self.idxNikkei      = "nikkei"
        self.idxSDax        = "sdax"
        self.idxSMI         = "smi"
        self.idxSP500       = "sp500"
        self.idxTecDax      = "tecdax"

        self.allIndices = [self.idxATX, self.idxCAC, self.idxDax, self.idxDowJones, self.idxEStoxx50,
                           self.idxFTS100, self.idxFtseMib, self.idxHangSeng, self.idxIbex, self.idxMDax,
                           self.idxNasdaq100, self.idxNikkei, self.idxSDax, self.idxSMI, self.idxSP500, self.idxTecDax]

        self.mongoClient = MongoClient()
        self.database = self.mongoClient[self.dbName]

    def getEndOfMonthValue( self, indexName, year, month ):
        idxCollection = self.database[indexName]
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month+1


        searchDate = datetime.datetime( year, month, 1 )
        startDate = searchDate
        startDate = startDate + datetime.timedelta(-1)
        entry = None
        while entry == None:
            entry = idxCollection.find_one({'date': {'$gte': startDate, '$lt': searchDate} })
            if entry == None:
                startDate = startDate + datetime.timedelta(-1)

        idxEntry = indexdata.IndexData()
        idxEntry.setDictionary(entry)
        return idxEntry

    def getHistoryValue(self, indexName, year, month, day):
        idxCollection = self.database[indexName]

        searchDate = datetime.datetime( year, month, day )
        startDate = searchDate
        startDate = startDate + datetime.timedelta(-1)
        entry = None
        while entry == None:
            entry = idxCollection.find_one({'date': {'$gte': startDate, '$lt': searchDate} })
            if entry == None:
                startDate = startDate + datetime.timedelta(-1)

        idxEntry = indexdata.IndexData()
        idxEntry.setDictionary(entry)
        return idxEntry

def requestBuy():
    indexDatabase = IndexDatabase()
    print "End of month values:"
    for idxName in indexDatabase.allIndices:
        idxData0 = indexDatabase.getEndOfMonthValue( idxName, 2016, 4)
        idxData1 = indexDatabase.getEndOfMonthValue( idxName, 2016, 3)
        idxData2 = indexDatabase.getEndOfMonthValue( idxName, 2016, 1)
        idxData3 = indexDatabase.getEndOfMonthValue( idxName, 2015, 10)
        idxData4 = indexDatabase.getEndOfMonthValue( idxName, 2015, 4)
        print str.format( '{:10} {:> 6.3f} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10}',
                          idxName, ((idxData0.close / idxData0.mean200)-1.0),
                          idxData0.date.year, idxData0.date.month, idxData0.date.day, idxData0.close,
                          idxData1.date.year, idxData1.date.month, idxData1.date.day, idxData1.close,
                          idxData2.date.year, idxData2.date.month, idxData2.date.day, idxData2.close,
                          idxData3.date.year, idxData3.date.month, idxData3.date.day, idxData3.close,
                          idxData4.date.year, idxData4.date.month, idxData4.date.day, idxData4.close )

    print "History values:"
    for idxName in indexDatabase.allIndices:
        idxData0 = indexDatabase.getHistoryValue( idxName, 2016, 4, 27)
        idxData1 = indexDatabase.getHistoryValue( idxName, 2016, 3, 27)
        idxData2 = indexDatabase.getHistoryValue( idxName, 2016, 1, 27)
        idxData3 = indexDatabase.getHistoryValue( idxName, 2015, 10, 27)
        idxData4 = indexDatabase.getHistoryValue( idxName, 2015, 4, 27)

        print str.format( '{:10} {:> 6.3f} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10}',
                          idxName, ((idxData0.close / idxData0.mean200)-1.0),
                          idxData0.date.year, idxData0.date.month, idxData0.date.day, idxData0.close,
                          idxData1.date.year, idxData1.date.month, idxData1.date.day, idxData1.close,
                          idxData2.date.year, idxData2.date.month, idxData2.date.day, idxData2.close,
                          idxData3.date.year, idxData3.date.month, idxData3.date.day, idxData3.close,
                          idxData4.date.year, idxData4.date.month, idxData4.date.day, idxData4.close )

if __name__ == '__main__':
    requestBuy()