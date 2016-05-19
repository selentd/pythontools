'''
Created on 19.05.2016

@author: dieter
'''

import datetime

class MultiResultEvaluation:

    startDateKey = "startDate"
    endDateKey   = "endDate"

    def __init__(self, runParameters=None):

        self.runParameters = runParameters
        self.transactionResultList = list()

    def _setupStartEndTime(self):
        if self.runParameters.hasKey( self.startDateKey ):
            self.startDate = self.runParameters[self.startDateKey]
        else:
            self.startDate = datetime.datetime.today()
            startDateList = list()
            for transactionList in self.transactionListDict:
                if len(transactionList.resultHistory) > 0:
                    startDateList.append(transactionList.resultHistory[0].indexBuy.date)

            if len(startDateList) > 0:
                startDateList.sort()
                self.startDate = startDateList[0]

        if self.runParameters.hasKey( self.endDateKey ):
            self.endDate = self.runParameters[self.endDateKey]
        else:
            self.endDate = datetime.datetime.today()

    def _setupExcludeChecker(self):
        pass

    def _createTransactionResult(self):
        pass

    def setUp(self):
        self._setupStartEndTime()
        self._setupExcludeChecker()

    def tearDown(self):
        pass

    def evaluate(self, transactionListDict):
        self.transactionListDict = transactionListDict
        self.setUp()
        self._createTransactionResult()
        self.tearDown()
        return self.transactionResultList
