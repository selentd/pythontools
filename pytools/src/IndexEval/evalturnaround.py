'''
Created on 06.04.2016

@author: selen00r
'''

import datetime

import fetchdata
import indexdata
import transactionchecker


class EvalTurnaround:
    '''
    classdocs
    '''


    def __init__(self, dbName, idxName):

        self.dbName = dbName
        self.idxName = idxName

    def loadIndexHistory(self, startDate, endDate = datetime.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate

        self.meandHistory = fetchdata.FetchData( self.dbName, self.idxName ).fetchSelectedHistory(self.startDate, self.endDate, self.selectFunc)

