'''
Created on 19.05.2016

@author: dieter
'''
import datetime

import indexdatabase
import fetchdata

class IndexSelector:

    def __init__(self):
        pass

    def _calcMonthDiff( self, startDate, monthDiff ):
        year = startDate.year
        month = startDate.month
        day = startDate.day
        if monthDiff < 12:
            if ( month - monthDiff ) <= 0:
                year -= 1
                month += (12 - monthDiff)
            else:
                month -= monthDiff
        else:
            year -= 1

        if day > 28:
            if month == 2:
                day = 28
            if day > 30:
                if month == 4 or month == 6 or month == 9 or month == 11:
                    day = 30

        return datetime.datetime( year, month, day )

    def _calcIndexValue(self, idxName, startDate, endDate ):
        pass

    def select(self, startDate, endDate):
        indexDict = dict()

        for idxName in indexdatabase.IndexDatabase.allIndices:
            idxResult = self._calcIndexValue(idxName, startDate, endDate )
            if idxResult[0] == True:
                indexDict[idxName] = idxResult[1]

        indexList = indexDict.items()
        indexList = sorted(indexList, key=lambda idx: idx[1], reverse=True)

        return indexList

class IndexSelectorRSIMonth(IndexSelector):

    def __init__(self, nrOfMonths = 12):
        IndexSelector.__init__(self)

        self.nrOfMonths = nrOfMonths

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart != None:
            diffDate = self._calcMonthDiff(startDate, self.nrOfMonths)
            idxData12M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
            if idxData12M != None:
                hasResult = True
                result = (idxData12M.close / idxDataStart.close) - 1.0

        return (hasResult, result)

class IndexSelectorRSIAvgMonth(IndexSelector):

    def __init__(self, monthList = None, useWeight = False):
        IndexSelector.__init__(self)

        if monthList != None:
            self.monthList = monthList
        else:
            self.monthList = [1, 3, 6, 12]

        self.useWeight = useWeight

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0
        idxDataList = list()

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart:
            hasResult = True
            for useMonth in self.monthList:
                diffDate = self._calcMonthDiff(startDate, useMonth)
                idxDataList.append(fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day ))

            for idxData in idxDataList:
                hasResult = hasResult and (idxData != None)

            if hasResult:
                if self.useWeight:
                    count = float(len(idxDataList))
                    divisor = 0.0
                    for idxData in idxDataList:
                        result += ((idxDataStart.close / idxData.close) - 1.0) * count
                        divisor += count
                        count -= 1.0
                    result /= divisor

                else:
                    for idxData in idxDataList:
                        result += (idxDataStart.close / idxData.close) - 1.0

                        result /= len(idxDataList)

        return (hasResult, result)

class IndexSelectorRSIGrad(IndexSelector):

    def __init__(self, grad = 200):
        IndexSelector.__init__(self)

        self.useGrad = grad

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart:
            grad = idxDataStart.getGradValue( self.useGrad )
            hasResult = (grad != 0.0)

        return (hasResult, result)

class IndexSelectorRSIAvgGrad(IndexSelector):

    def __init__(self, gradList = None, useWeight = False):
        IndexSelector.__init__(self)

        if gradList != None:
            self.gradList = gradList
        else:
            self.gradList = [21, 34, 89, 200]

        self.useWeight = useWeight

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0
        useGradList = list()

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart:
            hasResult = True
            for useGrad in self.gradList:
                useGradList.append(idxDataStart.getGradValue(useGrad))

            for grad in useGradList:
                if grad == 0.0:
                    hasResult = False

            if hasResult:
                if self.useWeight:
                    count = float(len(useGradList))
                    divisor = 0.0
                    for grad in useGradList:
                        result += (grad * count)
                        divisor += count
                        count -= 1.0
                    result /= divisor

                else:
                    for grad in useGradList:
                        result += grad

                    result /= len(useGradList)

        return (hasResult, result)

class IndexSelectorIdxData(IndexSelector):

    class TransactionDay():

        def __init__(self, transactionDate):
            self.transactionDate = transactionDate
            self.indexList = list()

    def __init__(self):
        IndexSelector.__init__(self)
        self.allTransactions = list()

    def setupIdxData(self, transactionListDict, startDate, endDate):

        currentDate = startDate
        while currentDate < endDate:
            transactionDay = IndexSelectorIdxData.TransactionDay( currentDate )

            for idxName in transactionListDict:
                for transaction in transactionListDict[idxName].resultHistory:
                    if transaction.indexBuy.date == currentDate:
                        transaction.indexName = idxName
                        transactionDay.indexList.append( transaction )
                        break
                    if transaction.indexBuy.date > currentDate:
                        break

            if len(transactionDay.indexList) > 0:
                self.allTransactions.append(transactionDay)

            currentDate += datetime.timedelta( 1 )



