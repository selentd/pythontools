'''
Created on 27.04.2016

@author: selen00r
'''

from pymongo.mongo_client import MongoClient

class IndexDatabase:
    '''
    classdocs
    '''
    dbName = "stockdb"
    dbIP   = "192.168.81.147"
    #dbIP    = "127.0.0.1"

    idxATX         = "atx"
    idxCAC         = "cac"
    idxDax         = "dax"
    idxDowJones    = "dowjones"
    idxEStoxx50    = "estoxx50"
    idxFTS100      = "ftse100"
    idxFtseMib     = "ftsemib"
    idxHangSeng    = "hangseng"
    idxIbex        = "ibex"
    idxMDax        = "mdax"
    idxNasdaq100   = "nasdaq100"
    idxNikkei      = "nikkei"
    idxSDax        = "sdax"
    idxSMI         = "smi"
    idxSP500       = "sp500"
    idxTecDax      = "tecdax"

    idxGold        = "gold"
    idxBrent       = "brent"

    allIndices = [idxATX, idxCAC, idxDax, idxDowJones, idxEStoxx50,
                  idxFTS100, idxFtseMib, idxHangSeng, idxIbex, idxMDax,
                  idxNasdaq100, idxNikkei, idxSDax, idxSMI, idxSP500, idxTecDax,
                  idxGold, idxBrent]



    def __init__(self):
        '''
        Constructor
        '''

        self._mongoClient = MongoClient(self.dbIP)
        self._database = self._mongoClient[self.dbName]

    def getIndexCollection(self, idxName):
        return self._database[idxName]


_indexDB = IndexDatabase()

def getIndexDatabase():
    return _indexDB
