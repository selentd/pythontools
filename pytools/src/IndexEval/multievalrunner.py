'''
Created on 27.04.2016

@author: selen00r
'''

import datetime

import evalcontinously
import evalrunner
import evalresult
import fetchdata
import indexdata
import indexdatabase

class IndexSelector:

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

class IndexSelectorRaise12M(IndexSelector):

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart != None:
            diffDate = self._calcMonthDiff(startDate, 12)
            idxData12M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
            if idxData12M != None:
                hasResult = True
                result = (idxData12M.close / idxDataStart.close) - 1.0

        return (hasResult, result)

class IndexSelectorRaise1M(IndexSelector):

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart != None:
            diffDate = self._calcMonthDiff(startDate, 1)
            idxData12M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
            if idxData12M != None:
                hasResult = True
                result = (idxData12M.close / idxDataStart.close) - 1.0

        return (hasResult, result)

class IndexSelectorRaise3M(IndexSelector):

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart != None:
            diffDate = self._calcMonthDiff(startDate, 3)
            idxData12M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
            if idxData12M != None:
                hasResult = True
                result = (idxData12M.close / idxDataStart.close) - 1.0

        return (hasResult, result)

class IndexSelectorRaise6M(IndexSelector):

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart != None:
            diffDate = self._calcMonthDiff(startDate, 6)
            idxData12M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
            if idxData12M != None:
                hasResult = True
                result = (idxData12M.close / idxDataStart.close) - 1.0

        return (hasResult, result)

class IndexSelectorRaiseAvg12M(IndexSelector):

    def _calcIndexValue(self, idxName, startDate, endDate ):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        diffDate = self._calcMonthDiff(startDate, 12)
        idxData12M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
        diffDate = self._calcMonthDiff(startDate, 6 )
        idxData6M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
        diffDate = self._calcMonthDiff(startDate, 3 )
        idxData3M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )
        diffDate = self._calcMonthDiff(startDate, 1 )
        idxData1M = fetch.fetchHistoryValue( diffDate.year, diffDate.month, diffDate.day )

        hasResult = (idxDataStart != None and idxData12M != None and idxData6M != None and idxData3M != None and idxData1M != None)
        if hasResult:
            result = (idxDataStart.close / idxData12M.close) - 1.0
            result += (idxDataStart.close / idxData6M.close) - 1.0
            result += (idxDataStart.close / idxData3M.close) - 1.0
            result += (idxDataStart.close / idxData1M.close) - 1.0
            result /= 4.0

        return (hasResult, result)

class MultiEvalPrinter(evalresult.TransactionResultPrinter):

    def __init__(self):
        pass


    def _printResultLooser(self, transactionResult, result, resultEuro ):
        buy = transactionResult.indexBuy.close

        print str.format( '{:10} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          transactionResult.getLowValue(),
                          transactionResult.getHighValue(),
                          result,
                          (buy / transactionResult.indexBuy.mean8)-1.0,
                          (buy / transactionResult.indexBuy.mean13)-1.0,
                          (buy / transactionResult.indexBuy.mean21)-1.0,
                          (buy / transactionResult.indexBuy.mean89)-1.0,
                          (buy / transactionResult.indexBuy.mean200)-1.0,
                          float(transactionResult.idxPositive) / float(transactionResult.idxCount) )


    def _printResultWinner(self, transactionResult, result, resultEuro ):
        buy = transactionResult.indexBuy.close

        print str.format( '{:10} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          transactionResult.getLowValue(),
                          transactionResult.getHighValue(),
                          result,
                          (buy / transactionResult.indexBuy.mean8)-1.0,
                          (buy / transactionResult.indexBuy.mean13)-1.0,
                          (buy / transactionResult.indexBuy.mean21)-1.0,
                          (buy / transactionResult.indexBuy.mean89)-1.0,
                          (buy / transactionResult.indexBuy.mean200)-1.0,
                          float(transactionResult.idxPositive) / float(transactionResult.idxCount) )

    def printResult(self, transactionResult, result, resultEuro, hasResult = False ):
        if hasResult:
            if result < 0.0:
                self._printResultLooser( transactionResult, result, resultEuro)
            else:
                self._printResultWinner(transactionResult, result, resultEuro)


class MulitEvalRunner:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

        self.periodDays = 0
        self.periodMonths = 0
        self.periodYears = 0
        self.transactionListDict = dict()
        self.transactionList0 = indexdata.TransactionResultHistory()
        self.transactionList1 = indexdata.TransactionResultHistory()
        self.transactionList2 = indexdata.TransactionResultHistory()

    def _calculateEvalEnd(self, evalStart ):
        evalEnd = evalStart
        if self.periodDays > 0:
            evalEnd = evalEnd + datetime.timedelta( self.periodDays )

        if self.periodMonths > 0:
            months = self.periodMonths
            while months >= 12:
                evalEnd.year +=1
                months -= 12

            if months > 0:
                if (evalEnd.month + months) >= 12:
                    evalEnd.year += 1
                    months = (evalEnd.month + months) - 12

                if months > 0:
                    evalEnd.month += months

        if self.periodYears > 0:
            evalEnd.year += self.periodYears

        return evalEnd

    def _getNextTransaction(self, idxName, evalStart, evalEnd):
        nextTransaction = None
        if self.transactionListDict == None:
            return None
        else:
            if self.transactionListDict.has_key(idxName):
                transactionList = self.transactionListDict[idxName]
                for transaction in transactionList.resultHistory:
                    if transaction.indexBuy.date >= evalEnd:
                        break

                    if transaction.indexBuy.date >= evalStart:
                        nextTransaction = transaction
                        break

        return nextTransaction


    def _setupStartEndTime(self):
        self.startDate = datetime.datetime( 2000, 1, 1 )
        self.endDate = datetime.datetime( 2016, 1, 1 )

    def _setupEvaluationPeriod(self):
        self.periodDays = 7

    def _setupIndexSelector(self):
        self.indexSelector = IndexSelectorRaiseAvg12M()
        #self.indexSelector = IndexSelectorRaise1M()
        #self.indexSelector = IndexSelectorRaise3M()
        #self.indexSelector = IndexSelectorRaise6M()
        #self.indexSelector = IndexSelectorRaise12M()

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = False
        self.resultCalculator = evalresult.ResultCalculator()
        #self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 8.0, self.startInvest, self.fixedInvest )

    def _setupResultExcludeChecker(self):
        self.excludeChecker = evalresult.ExcludeTransaction()

    def _setupTransactionPrinter(self):
        #self.resultTransactionPrinter = MultiEvalPrinter()
        self.resultTransactionPrinter = evalresult.TransactionResultPrinter()

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createResultEvaluation(self, indexName, descriptionStr):
        self.resultCalculator.reset()
        self.resultCalculatorEuro.reset()

        resultEvaluation = evalresult.EvalResultCall( indexName + " " + descriptionStr, self.startInvest, self.fixedInvest )
        resultEvaluation.setExcludeChecker( self.excludeChecker )
        resultEvaluation.setResultCalculator(self.resultCalculator )
        resultEvaluation.setResultCalculatorEuro(self.resultCalculatorEuro)
        return resultEvaluation

    def setup(self):
        self._setupStartEndTime()
        self._setupEvaluationPeriod()
        self._setupIndexSelector()
        self._setupResultCalculator()
        self._setupResultExcludeChecker()
        self._setupTransactionPrinter()
        self._setupEvalResultPrinter()

    def tearDown(self):
        pass

    def _countPositiveIndex(self, idxList):
        counter = 0
        for idx in idxList:
            if idx[1] > 0:
                counter += 1
        return counter

    def evaluate(self):
        self.evalStart = self.startDate
        self.evalEnd = self._calculateEvalEnd( self.evalStart )
        currentTransaction0 = None
        currentTransaction1 = None
        currentTransaction2 = None

        while self.evalStart < self.endDate:
            idxList = self.indexSelector.select( self.evalStart, self.evalEnd )

            if idxList[0][1] > 0:
                if currentTransaction0 == None or currentTransaction0.indexSell.date < self.evalStart:
                    currentTransaction0 = self._getNextTransaction( idxList[0][0], self.evalStart, self.evalEnd )
                    if currentTransaction0 != None:
                        currentTransaction0.indexName = idxList[0][0]
                        currentTransaction0.idxCount = len(idxList)
                        currentTransaction0.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList0.addTransactionResult(currentTransaction0)

            if idxList[1][1] > 0:
                if currentTransaction1 == None or currentTransaction1.indexSell.date < self.evalStart:
                    currentTransaction1 = self._getNextTransaction( idxList[1][0], self.evalStart, self.evalEnd )
                    if currentTransaction1 != None:
                        currentTransaction1.indexName = idxList[1][0]
                        currentTransaction1.idxCount = len(idxList)
                        currentTransaction1.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList1.addTransactionResult(currentTransaction1)

            if idxList[2][1] > 0:
                if currentTransaction2 == None or currentTransaction2.indexSell.date < self.evalStart:
                    currentTransaction2 = self._getNextTransaction( idxList[2][0], self.evalStart, self.evalEnd )
                    if currentTransaction2 != None:
                        currentTransaction2.indexName = idxList[1][0]
                        currentTransaction2.idxCount = len(idxList)
                        currentTransaction2.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList2.addTransactionResult(currentTransaction2)

            self.evalStart = self.evalEnd
            self.evalEnd = self._calculateEvalEnd(self.evalStart)

        resultEvaluation0 = self._createResultEvaluation("best", "avg12")
        self.transactionList0.evaluateResult( resultEvaluation0, self.resultTransactionPrinter )
        self.evaluationResultPrinter.printResult("best", "avg12", resultEvaluation0)

        resultEvaluation1 = self._createResultEvaluation("2nd", "avg12")
        self.transactionList1.evaluateResult( resultEvaluation1, self.resultTransactionPrinter )
        self.evaluationResultPrinter.printResult("2nd", "avg12", resultEvaluation1)

        resultEvaluation2 = self._createResultEvaluation("3rd", "avg12")
        self.transactionList2.evaluateResult( resultEvaluation2, self.resultTransactionPrinter )
        self.evaluationResultPrinter.printResult("3rd", "avg12", resultEvaluation2)


    def run(self):
        self.setup()
        self.evaluate()
        self.tearDown()

    def setTransactionListDict(self, transactionLists ):
        self.transactionListDict = transactionLists

class TestEvalContinously3(evalrunner.EvalRunner):

    def __init__(self, mean1, mean2, mean3, maxWin = 0.0, maxDays=0, maxLoss = 0.0, maxJump = 0.0):
        evalrunner.EvalRunner.__init__(self)
        self.mean1 = mean1
        self.mean2 = mean2
        self.mean3 = mean3
        self.maxDays = maxDays
        self.maxLoss = maxLoss
        self.maxJump = maxJump
        self.maxWin = maxWin

    def _setupResultCalculator(self):
        self.startInvest = 1000.0
        self.fixedInvest = False
        self.resultCalculator = evalresult.ResultCalculator()
        #self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest)
        self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( 8.0, self.startInvest, self.fixedInvest )

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        #evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, 21, 0.0, self.maxWin, self.maxDays, self.maxLoss, self.maxJump )
        evaluation = evalcontinously.EvalContinouslyMean3( self.dbName, indexName, self.mean1, self.mean2, self.mean3, self.maxWin, self.maxDays, self.maxLoss, self.maxJump )
        return evaluation

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    mean = 21
    mean2 = 89
    mean3 = 200
    offset = 0.01
    maxDays = 100
    maxLoss = -0.02
    maxJump = -0.02
    maxWin = 0.0
    descr = str.format("Mean {:3} {:3} {:3}", mean, mean2, mean3)

    '''
    testEvaluation = TestEvalContinously3( mean, mean2, mean3, maxWin )
    testEvaluation.run( descr )

    multiTestEvaluation = MulitEvalRunner()
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run()
    print ""

    testEvaluation = TestEvalContinously3( mean, mean2, mean3, maxWin, maxDays, maxLoss )
    testEvaluation.run( descr )

    multiTestEvaluation = MulitEvalRunner()
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run()
    print ""
    '''
    testEvaluation = TestEvalContinously3( mean, mean2, mean3, maxWin, maxDays, maxLoss, maxJump )
    testEvaluation.run( descr )
    multiTestEvaluation = MulitEvalRunner()
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run()
    print ""

