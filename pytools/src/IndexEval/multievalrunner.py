'''
Created on 27.04.2016

@author: selen00r
'''

import datetime

import evalcontinously
import evalmonthly

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
            result += ((idxDataStart.close / idxData6M.close) - 1.0)
            result += ((idxDataStart.close / idxData3M.close) - 1.0)
            result += ((idxDataStart.close / idxData1M.close) - 1.0)
            result /= 4.0

        return (hasResult, result)

class IndexSelectorRaiseAvg12MWeighted(IndexSelector):

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
            result += ((idxDataStart.close / idxData6M.close) - 1.0)*2.0
            result += ((idxDataStart.close / idxData3M.close) - 1.0)*3.0
            result += ((idxDataStart.close / idxData1M.close) - 1.0)*4.0
            result /= (1.0 + 2.0 + 3.0 + 4.0)

        return (hasResult, result)

class IndexSelectorRsiGrad( IndexSelector ):

    def _calcIndexValue(self, idxName, startDate, endDate):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart:
            #21 34 89 200
            #13 21 89 200
            #21 34 89 233
            #21 34 144 233 !
            grad1 = idxDataStart.getGradValue( 21 )
            grad2 = idxDataStart.getGradValue( 55 )
            grad3 = idxDataStart.getGradValue( 144 )
            grad4 = idxDataStart.getGradValue( 233 )

            hasResult = (grad1 != 0.0 and grad2 != 0.0 and grad3 != 0.0 and grad4 != 0.0)
            if hasResult:
                result = grad1
                result += grad2
                result += grad3
                result += grad4
                result /= 4.0

        return (hasResult, result)

class IndexSelectorRsiGradWeighted( IndexSelector ):

    def _calcIndexValue(self, idxName, startDate, endDate):
        hasResult = False
        result = 0.0

        fetch = fetchdata.FetchData( idxName )
        idxDataStart = fetch.fetchHistoryValue( startDate.year, startDate.month, startDate.day)

        if idxDataStart:
            grad1 = idxDataStart.getGradValue( 13 )
            grad2 = idxDataStart.getGradValue( 21 )
            grad3 = idxDataStart.getGradValue( 89 )
            grad4 = idxDataStart.getGradValue( 200 )

            hasResult = (grad1 != 0.0 and grad2 != 0.0 and grad3 != 0.0 and grad4 != 0.0)
            if hasResult:
                result = (grad1 * 4.0)
                result += (grad2 * 3.0)
                result += (grad3 * 2.0)
                result += (grad4 * 1.0)
                result /= (1.0 + 2.0 + 3.0 + 4.0)

        return (hasResult, result)



class MultiEvalPrinter(evalresult.TransactionResultPrinter):

    def __init__(self):
        pass


    def _printResultLooser(self, transactionResult, result, resultEuro ):
        buy = transactionResult.indexBuy.close

        print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          transactionResult.indexBuy.date,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          transactionResult.getLowValue(),
                          transactionResult.getHighValue(),
                          resultEuro,
                          result,
                          (buy / transactionResult.indexBuy.mean8)-1.0,
                          (buy / transactionResult.indexBuy.mean13)-1.0,
                          (buy / transactionResult.indexBuy.mean21)-1.0,
                          (buy / transactionResult.indexBuy.mean89)-1.0,
                          (buy / transactionResult.indexBuy.mean200)-1.0,
                          float(transactionResult.idxPositive) / float(transactionResult.idxCount) )


    def _printResultWinner(self, transactionResult, result, resultEuro ):
        buy = transactionResult.indexBuy.close

        print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          transactionResult.indexBuy.date,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          transactionResult.getLowValue(),
                          transactionResult.getHighValue(),
                          resultEuro,
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


    def __init__(self, runParameters):
        '''
        Constructor
        '''

        self.runParameters = runParameters
        self.periodDays = 0
        self.periodMonths = 0
        self.periodYears = 0
        self.transactionListDict = dict()
        self.transactionList0 = indexdata.TransactionResultHistory()
        self.transactionList1 = indexdata.TransactionResultHistory()
        self.transactionList2 = indexdata.TransactionResultHistory()

        if self.runParameters.has_key(evalrunner.EvalRunner.isCallKey):
            self.isCall = self.runParameters[evalrunner.EvalRunner.isCallKey]
        else:
            self.isCall = True

    def _calculateEvalEnd_(self, evalStart):
        evalEnd = evalStart
        day = evalEnd.day
        month = evalEnd.month
        year = evalEnd.year

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        return datetime.datetime( year, month, day )

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
        self.endDate = datetime.datetime.today()
        #self.endDate = datetime.datetime(2013, 1, 1)

    def _setupEvaluationPeriod(self):
        self.periodDays = 1

    def _setupIndexSelector(self):
        if self.isCall:
            #self.indexSelector = IndexSelectorRaiseAvg12M()
            self.indexSelector = IndexSelectorRsiGrad()
        else:
            #self.indexSelector = IndexSelectorRaiseAvg12MWeighted()
            self.indexSelector = IndexSelectorRsiGradWeighted()
        #self.indexSelector = IndexSelectorRaise1M()
        #self.indexSelector = IndexSelectorRaise3M()
        #self.indexSelector = IndexSelectorRaise6M()
        #self.indexSelector = IndexSelectorRaise12M()

    def _setupResultCalculator(self):
        self.startInvest = self.runParameters[evalrunner.EvalRunner.startInvestKey]
        self.fixedInvest = self.runParameters[evalrunner.EvalRunner.fixedInvestKey]
        self.maxInvest = self.runParameters[evalrunner.EvalRunner.maxInvestKey]
        self.idxDistance = self.runParameters[evalrunner.EvalRunner.idxDistanceKey]
        if self.isCall:
            self.resultCalculator = evalresult.ResultCalculator()
        else:
            self.resultCalculator = evalresult.ResultCalculatorPut()

        if self.runParameters.has_key(evalrunner.EvalRunner.idxDistanceKey):
            if self.isCall:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeverage( self.runParameters[evalrunner.EvalRunner.idxDistanceKey],
                                                                                     self.startInvest,
                                                                                     self.fixedInvest,
                                                                                     self.maxInvest )
            else:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuroLeveragePut( self.runParameters[evalrunner.EvalRunner.idxDistanceKey],
                                                                                        self.startInvest,
                                                                                        self.fixedInvest,
                                                                                        self.maxInvest )

        else:
            if self.isCall:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuro(self.startInvest, self.fixedInvest, self.maxInvest)
            else:
                self.resultCalculatorEuro = evalresult.ResultCalculatorEuroPut(self.startInvest, self.fixedInvest, self.maxInvest)

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

        resultEvaluation = evalresult.EvalResult( indexName + " " + descriptionStr, self.startInvest, self.fixedInvest )
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

    def _evaluateCall(self):
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
                        currentTransaction2.indexName = idxList[2][0]
                        currentTransaction2.idxCount = len(idxList)
                        currentTransaction2.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList2.addTransactionResult(currentTransaction2)

            self.evalStart = self.evalEnd
            self.evalEnd = self._calculateEvalEnd(self.evalStart)

    def _evaluatePut(self):
        self.evalStart = self.startDate
        self.evalEnd = self._calculateEvalEnd( self.evalStart )
        currentTransaction0 = None
        currentTransaction1 = None
        currentTransaction2 = None

        while self.evalStart < self.endDate:
            idxList = self.indexSelector.select( self.evalStart, self.evalEnd )
            idxList.reverse()

            if idxList[0][1] < 0:
                if currentTransaction0 == None or currentTransaction0.indexSell.date < self.evalStart:
                    currentTransaction0 = self._getNextTransaction( idxList[0][0], self.evalStart, self.evalEnd )
                    if currentTransaction0 != None:
                        currentTransaction0.indexName = idxList[0][0]
                        currentTransaction0.idxCount = len(idxList)
                        currentTransaction0.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList0.addTransactionResult(currentTransaction0)

            if idxList[1][1] < 0:
                if currentTransaction1 == None or currentTransaction1.indexSell.date < self.evalStart:
                    currentTransaction1 = self._getNextTransaction( idxList[1][0], self.evalStart, self.evalEnd )
                    if currentTransaction1 != None:
                        currentTransaction1.indexName = idxList[1][0]
                        currentTransaction1.idxCount = len(idxList)
                        currentTransaction1.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList1.addTransactionResult(currentTransaction1)

            if idxList[2][1] < 0:
                if currentTransaction2 == None or currentTransaction2.indexSell.date < self.evalStart:
                    currentTransaction2 = self._getNextTransaction( idxList[2][0], self.evalStart, self.evalEnd )
                    if currentTransaction2 != None:
                        currentTransaction2.indexName = idxList[2][0]
                        currentTransaction2.idxCount = len(idxList)
                        currentTransaction2.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList2.addTransactionResult(currentTransaction2)

            self.evalStart = self.evalEnd
            self.evalEnd = self._calculateEvalEnd(self.evalStart)

    def evaluate(self):
        if self.isCall == True:
            self._evaluateCall()
        else:
            self._evaluatePut()

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

class TestEvalContinously(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, self.runParameters )
        return evaluation

class TestEvalContinously3(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        #evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, 21, 0.0, self.maxWin, self.maxDays, self.maxLoss, self.maxJump )
        evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, self.runParameters )
        return evaluation

class TestEvalMonthly(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _createIndexEvaluation(self, indexName):
        evaluation = evalmonthly.EvalFirstDays( self.dbName, indexName, self.runParameters )
        return evaluation

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    runParameters = dict()

    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = False

    runParameters[evalcontinously.EvalContinously.maxDaysKey] = 0
    runParameters[evalcontinously.EvalContinously.maxWinKey] = 0.0

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = True
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = 200
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = 21
    runParameters[evalcontinously.EvalContinouslyMean.startOffsetKey] = 0.0
    runParameters[evalcontinously.EvalContinouslyMean.endOffsetKey] = 0.0


    descr = str.format("Mean {:3} {:3} {:3}", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)
    '''
    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 6.0

    runParameters[evalcontinously.EvalContinously.maxDaysKey] = 4
    runParameters[evalcontinously.EvalContinously.maxLossKey] = -0.01
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = -0.04

    testEvaluation = TestEvalMonthly( runParameters )
    testEvaluation.run( descr )

    multiTestEvaluation = MulitEvalRunner( runParameters )
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run()

    print ""
    '''
    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 8.0

    runParameters[evalcontinously.EvalContinously.maxDaysKey] = 100
    runParameters[evalcontinously.EvalContinously.maxLossKey] = -0.01
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = -0.02

    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = 21

    descr = str.format("Mean {:3} {:3} {:3}", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)

    testEvaluation = TestEvalContinously3( runParameters )
    testEvaluation.run( descr )

    multiTestEvaluation = MulitEvalRunner( runParameters )
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run()

    print ""

    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 10.0

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = False
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = 13
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = 21

    runParameters[evalcontinously.EvalContinously.maxLossKey] = 0.0
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = 0.0

    descr = str.format("Mean {:3} {:3} {:3}", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)

    '''
    testEvaluation = TestEvalContinously3( runParameters )
    testEvaluation.run( descr )

    multiTestEvaluation = MulitEvalRunner( runParameters )
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run()
    '''
    print ""
