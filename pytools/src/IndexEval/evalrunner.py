'''
Created on 04.11.2015

@author: selen00r
'''

import datetime

from pymongo.mongo_client import MongoClient

import evalresult

class EvalRunner(object):
    '''
    Base class to run an evaluation of an index.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.dbName = "indexdb"

        self.idxDax         = "dax"
        self.idxMDax        = "mdax"
        self.idxTecDax      = "tecdax"
        self.idxSP500       = "sp500"
        self.idxNasdaq100   = "nasdaq100"
        self.idxEStoxx50    = "estoxx50"
        self.idxNikkei      = "nikkei"
        self.idxSMI         = "smi"
        self.idxATX         = "atx"
        self.idxCAC         = "cac"
        self.idxDowJones    = "dowjones"
        self.idxFTS100      = "fts100"
        self.idxFtseMib     = "ftsemib"
        self.idxHangSeng    = "hangseng"
        self.idxIbex        = "ibex"

        self.allIndices = [self.idxATX, self.idxCAC, self.idxDax, self.idxDowJones, self.idxEStoxx50,
                           self.idxFTS100, self.idxFtseMib, self.idxHangSeng, self.idxIbex, self.idxMDax,
                           self.idxNasdaq100, self.idxNikkei, self.idxSMI, self.idxTecDax]

    def setUp(self):
        self.mongoClient = MongoClient()
        self.database = self.mongoClient[self.dbName]
        self.startDate = datetime.datetime( 2000, 1, 1 )
        self.endDate = datetime.datetime( 2015, 10, 1 )

        self.startInvest = 1000.0
        self.fixedInvest = True
        self.excludeChecker = evalresult.ExcludeTransaction()
        self.resultCalculator = evalresult.ResultCalculator()
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)


    def tearDown(self):
        pass