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
import indexselector


class MultiEvalPrinter(evalresult.TransactionResultPrinter):

    def __init__(self):
        pass

    def _printTransactionHistoryLooser(self, transactionResult):
        count = 0
        for idxData in transactionResult.indexHistory.indexHistory:
            print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d}  {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:3} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                              transactionResult.indexName,
                              idxData.date,
                              idxData.date,
                              idxData.open,
                              idxData.close,
                              idxData.low,
                              idxData.high,
                              count,
                              idxData.close - transactionResult.indexBuy.close,
                              -((idxData.close / transactionResult.indexBuy.close) -1.0),
                              (idxData.close / idxData.mean8)-1.0,
                              (idxData.close / idxData.mean13)-1.0,
                              (idxData.close / idxData.mean21)-1.0 )
            count += 1

    def _printResultLooser(self, transactionResult, result, resultEuro ):
        buy = transactionResult.indexBuy.close

        print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:3} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          transactionResult.indexBuy.date,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          transactionResult.getLowValue(),
                          transactionResult.getHighValue(),
                          transactionResult.indexHistory.len(),
                          resultEuro,
                          result,
                          (buy / transactionResult.indexBuy.mean8)-1.0,
                          (buy / transactionResult.indexBuy.mean13)-1.0,
                          (buy / transactionResult.indexBuy.mean21)-1.0,
                          (buy / transactionResult.indexBuy.mean89)-1.0,
                          (buy / transactionResult.indexBuy.mean200)-1.0,
                          float(transactionResult.idxPositive) / float(transactionResult.idxCount),
                          transactionResult.idxSelect )
        #self._printTransactionHistoryLooser( transactionResult )

    def _printTransactionHistoryWinner(self, transactionResult):
        count = 0
        for idxData in transactionResult.indexHistory.indexHistory:
            print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d}  {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:3} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                              transactionResult.indexName,
                              idxData.date,
                              idxData.date,
                              idxData.open,
                              idxData.close,
                              idxData.low,
                              idxData.high,
                              count,
                              idxData.close - transactionResult.indexBuy.close,
                              -((idxData.close / transactionResult.indexBuy.close) - 1.0),
                              (idxData.close / idxData.mean8)-1.0,
                              (idxData.close / idxData.mean13)-1.0,
                              (idxData.close / idxData.mean21)-1.0 )

            count += 1


    def _printResultWinner(self, transactionResult, result, resultEuro ):
        buy = transactionResult.indexBuy.close

        print str.format( '{:10} {:%Y-%m-%d} {:%Y-%m-%d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:3} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f}',
                          transactionResult.indexName,
                          transactionResult.indexBuy.date,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          transactionResult.getLowValue(),
                          transactionResult.getHighValue(),
                          transactionResult.indexHistory.len(),
                          resultEuro,
                          result,
                          (buy / transactionResult.indexBuy.mean8)-1.0,
                          (buy / transactionResult.indexBuy.mean13)-1.0,
                          (buy / transactionResult.indexBuy.mean21)-1.0,
                          (buy / transactionResult.indexBuy.mean89)-1.0,
                          (buy / transactionResult.indexBuy.mean200)-1.0,
                          float(transactionResult.idxPositive) / float(transactionResult.idxCount),
                          transactionResult.idxSelect )
        #self._printTransactionHistoryWinner(transactionResult)


    def printResult(self, transactionResult, result, resultEuro, hasResult = False ):
        if hasResult:
            if result < 0.0:
                self._printResultLooser( transactionResult, result, resultEuro)
            else:
                self._printResultWinner(transactionResult, result, resultEuro)


class MulitEvalRunner(evalrunner.EvalRunner):
    '''
    classdocs
    '''

<<<<<<< HEAD
    indexSelectorKey = "IndexSelector"
=======
    indexSelectorKey = "indexSelector"
>>>>>>> branch 'devtrial' of https://github.com/selentd/pythontools

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

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

    def _setupEvalResultPrinter(self):
        self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()

    def _setupEvaluationPeriod(self):
        self.periodDays = 1

    def _setupIndexSelector(self):
        if self.runParameters.has_key(self.indexSelectorKey):
            self.indexSelector = self.runParameters[self.indexSelectorKey]
        else:
            self.indexSelector = indexselector.IndexSelectorRSIAvgMonth([1,3,6,12], True)

    def setUp(self):
        evalrunner.EvalRunner.setUp(self)

        self._setupEvaluationPeriod()
        self._setupIndexSelector()

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

            if (len(idxList) > 0) and (idxList[0][1] > 0):
                if currentTransaction0 == None or currentTransaction0.indexSell.date < self.evalStart:
                    currentTransaction0 = self._getNextTransaction( idxList[0][0], self.evalStart, self.evalEnd )
                    if currentTransaction0 != None:
                        currentTransaction0.indexName = idxList[0][0]
                        currentTransaction0.idxCount = len(idxList)
                        currentTransaction0.idxPositive = self._countPositiveIndex( idxList )
                        currentTransaction0.idxSelect = idxList[0][1]
                        self.transactionList0.addTransactionResult(currentTransaction0)

            if (len(idxList) > 1) and (idxList[1][1] > 0):
                if currentTransaction1 == None or currentTransaction1.indexSell.date < self.evalStart:
                    currentTransaction1 = self._getNextTransaction( idxList[1][0], self.evalStart, self.evalEnd )
                    if currentTransaction1 != None:
                        currentTransaction1.indexName = idxList[1][0]
                        currentTransaction1.idxCount = len(idxList)
                        currentTransaction1.idxPositive = self._countPositiveIndex( idxList )
                        currentTransaction1.idxSelect = idxList[1][1]
                        self.transactionList1.addTransactionResult(currentTransaction1)

            if (len(idxList) >2) and (idxList[2][1] > 0):
                if currentTransaction2 == None or currentTransaction2.indexSell.date < self.evalStart:
                    currentTransaction2 = self._getNextTransaction( idxList[2][0], self.evalStart, self.evalEnd )
                    if currentTransaction2 != None:
                        currentTransaction2.indexName = idxList[2][0]
                        currentTransaction2.idxCount = len(idxList)
                        currentTransaction2.idxPositive = self._countPositiveIndex( idxList )
                        currentTransaction2.idxSelect = idxList[2][1]
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
            #if len(idxList) > 0:
                if currentTransaction0 == None or currentTransaction0.indexSell.date < self.evalStart:
                    currentTransaction0 = self._getNextTransaction( idxList[0][0], self.evalStart, self.evalEnd )
                    if currentTransaction0 != None:
                        currentTransaction0.indexName = idxList[0][0]
                        currentTransaction0.idxCount = len(idxList)
                        currentTransaction0.idxPositive = self._countPositiveIndex( idxList )
                        currentTransaction0.idxSelect = idxList[0][1]
                        self.transactionList0.addTransactionResult(currentTransaction0)

            if idxList[1][1] < 0:
            #if len(idxList) > 1:
                if currentTransaction1 == None or currentTransaction1.indexSell.date < self.evalStart:
                    currentTransaction1 = self._getNextTransaction( idxList[1][0], self.evalStart, self.evalEnd )
                    if currentTransaction1 != None:
                        currentTransaction1.indexName = idxList[1][0]
                        currentTransaction1.idxCount = len(idxList)
                        currentTransaction1.idxPositive = self._countPositiveIndex( idxList )
                        currentTransaction1.idxSelect = idxList[1][1]
                        self.transactionList1.addTransactionResult(currentTransaction1)

            if idxList[2][1] < 0:
            #if len(idxList) > 2:
                if currentTransaction2 == None or currentTransaction2.indexSell.date < self.evalStart:
                    currentTransaction2 = self._getNextTransaction( idxList[2][0], self.evalStart, self.evalEnd )
                    if currentTransaction2 != None:
                        currentTransaction2.indexName = idxList[2][0]
                        currentTransaction2.idxCount = len(idxList)
                        currentTransaction2.idxPositive = self._countPositiveIndex( idxList )
                        currentTransaction2.idxSelect = idxList[2][1]
                        self.transactionList2.addTransactionResult(currentTransaction2)
            '''

            if currentTransaction0 == None or currentTransaction0.indexSell.date < self.evalStart:
                currentTransaction0 = self._getNextTransaction( idxList[0][0], self.evalStart, self.evalEnd )
                if currentTransaction0 != None:
                    currentTransaction0.indexName = idxList[0][0]
                    currentTransaction0.idxCount = len(idxList)
                    currentTransaction0.idxPositive = self._countPositiveIndex( idxList )
                    self.transactionList0.addTransactionResult(currentTransaction0)
            else:
                if currentTransaction1 == None or currentTransaction1.indexSell.date < self.evalStart:
                    currentTransaction1 = self._getNextTransaction(idxList[0][0], self.evalStart, self.evalEnd)
                    if currentTransaction1 != None:
                        currentTransaction1.indexName = idxList[0][0]
                        currentTransaction1.idxCount = len(idxList)
                        currentTransaction1.idxPositive = self._countPositiveIndex( idxList )
                        self.transactionList1.addTransactionResult(currentTransaction1)
                else:
                    if currentTransaction2 == None or currentTransaction2.indexSell.date < self.evalStart:
                        currentTransaction2 = self._getNextTransaction(idxList[0][0], self.evalStart, self.evalEnd)
                        if currentTransaction2 != None:
                            currentTransaction2.indexName = idxList[0][0]
                            currentTransaction2.idxCount = len(idxList)
                            currentTransaction2.idxPositive = self._countPositiveIndex( idxList )
                            self.transactionList1.addTransactionResult(currentTransaction1)

            '''

            self.evalStart = self.evalEnd
            self.evalEnd = self._calculateEvalEnd(self.evalStart)

    def runEvaluation(self, descriptionStr, indexList = None):
        if self.isCall == True:
            self._evaluateCall()
        else:
            self._evaluatePut()

        resultEvaluation0 = self._createResultEvaluation("best", descriptionStr)
        self.transactionList0.evaluateResult( resultEvaluation0, self.resultTransactionPrinter )
        self.evaluationResultPrinter.printResult("best", descriptionStr, resultEvaluation0)

        resultEvaluation1 = self._createResultEvaluation("2nd", descriptionStr)
        self.transactionList1.evaluateResult( resultEvaluation1, self.resultTransactionPrinter )
        self.evaluationResultPrinter.printResult("2nd", descriptionStr, resultEvaluation1)

        resultEvaluation2 = self._createResultEvaluation("3rd", descriptionStr)
        self.transactionList2.evaluateResult( resultEvaluation2, self.resultTransactionPrinter )
        self.evaluationResultPrinter.printResult("3rd", descriptionStr, resultEvaluation2)

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
        #self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()
        self.evaluationResultPrinter = evalrunner.EvalResultPrinter()

    def _createIndexEvaluation(self, indexName):
        #evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, 21, 0.0, self.maxWin, self.maxDays, self.maxLoss, self.maxJump )
        evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, self.runParameters )
        return evaluation

class TestEvalMonthly(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _setupEvalResultPrinter(self):
        #self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()
        self.evaluationResultPrinter = evalrunner.EvalResultPrinter()


    def _createIndexEvaluation(self, indexName):
        evaluation = evalmonthly.EvalFirstDays( self.dbName, indexName, self.runParameters )
        return evaluation

class TestEvalContinouslyGrad(evalrunner.EvalRunner):
    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _setupEvalResultPrinter(self):
        #self.evaluationResultPrinter = evalrunner.EvalResultPrinterSimple()
        self.evaluationResultPrinter = evalrunner.EvalResultPrinter()

    def _createIndexEvaluation(self, indexName):
        #evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, 21, 0.0, self.maxWin, self.maxDays, self.maxLoss, self.maxJump )
        evaluation = evalcontinously.EvalContinouslyGrad( self.dbName, indexName, self.runParameters )
        return evaluation

class TotalEvaluationResult:

    def __init__(self):
        self.maxTotalResult1 = 0.0
        self.maxTotalDescr1 = ""
        self.maxTotalResult2 = 0.0
        self.maxTotalDescr2 = ""
        self.maxTotalResult3 = 0.0
        self.maxTotalDescr3 = 0.0

    def updateTotalResult(self, resultEvaluationDict, descr):
        totalCount = 0
        winCount = 0
        lossCount = 0
        winRatio = 0.0
        maxResultLoss = 0.0
        maxResultWin = 0.0
        totalResult = 0.0
        totalResultEuro = 0.0
        totalInvestEuro = 0.0

        for entry in resultEvaluationDict:
            resultEvaluationEntry = resultEvaluationDict[entry]
            totalCount += resultEvaluationEntry.getTotalCount()
            winCount += resultEvaluationEntry.winCount
            lossCount += resultEvaluationEntry.lossCount
            winRatio += resultEvaluationEntry.getWinRatio()

            if (maxResultLoss > resultEvaluationEntry.maxLoss):
                maxResultLoss = resultEvaluationEntry.maxLoss

            if (maxResultWin < resultEvaluationEntry.maxWin):
                maxResultWin = resultEvaluationEntry.maxWin

            totalResult += resultEvaluationEntry.getTotalResult()
            totalResultEuro += resultEvaluationEntry.getTotalResultEuro()
            totalInvestEuro += resultEvaluationEntry.getTotalInvestEuro()

        print str.format( '{:10} {:25} {:>6} {:>6} {:>6} {:>6.2f} {:>6.3f} {:>6.3f} {:>6.3f} {:>10.2f} {:>10.2f} {:>10.2f}',
                      "Total",
                      descr,
                      totalCount,
                      winCount,
                      lossCount,
                      winRatio / len(resultEvaluationDict),
                      maxResultLoss,
                      maxResultWin,
                      totalResult,
                      totalResultEuro,
                      totalInvestEuro,
                      totalResultEuro - totalInvestEuro )

        if (totalResultEuro - totalInvestEuro) > self.maxTotalResult1:
            self.maxTotalResult3 = self.maxTotalResult2
            self.maxTotalDescr3 = self.maxTotalDescr2

            self.maxTotalResult2 = self.maxTotalResult1
            self.maxTotalDescr2 = self.maxTotalDescr1

            self.maxTotalResult1 = (totalResultEuro - totalInvestEuro)
            self.maxTotalDescr1 = descr
        else:
            if (totalResultEuro - totalInvestEuro) > self.maxTotalResult2:
                self.maxTotalResult3 = self.maxTotalResult2
                self.maxTotalDescr3 = self.maxTotalDescr2

                self.maxTotalResult2 = (totalResultEuro - totalInvestEuro)
                self.maxTotalDescr2 = descr
            else:
                if (totalResultEuro - totalInvestEuro) > self.maxTotalResult3:
                    self.maxTotalResult3 = (totalResultEuro - totalInvestEuro)
                    self.maxTotalDescr3 = descr

        #print str.format( '{:10} {:20} {:>10.2f}', "Best", self.maxTotalDescr1, self.maxTotalResult1 )
        #print str.format( '{:10} {:20} {:>10.2f}', "2nd", self.maxTotalDescr2, self.maxTotalResult2 )
        #print str.format( '{:10} {:20} {:>10.2f}', "3rd", self.maxTotalDescr3, self.maxTotalResult3 )

        #print ""

def runPutEvaluations():
    runParameters   = dict()
    totalEvaluationResult = TotalEvaluationResult()

    yearStart = 2000
    period = 9

    maxWin = 0.0
    maxLoss = 0.0001
    maxJump = 0.00
    maxHighJump = 0.00

    runParameters[evalrunner.EvalRunner.startDateKey] = datetime.datetime( 2000, 1, 1)
    #runParameters[evalrunner.EvalRunner.endDateKey] = datetime.datetime( yearStart + period, 1, 1)
    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = False
    #runParameters[evalrunner.EvalRunner.idxDistanceKey] = 10.0

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = False

    runParameters[evalcontinously.EvalContinously.maxWinKey] = maxWin
    runParameters[evalcontinously.EvalContinously.maxLossKey] = maxLoss
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = maxJump
    runParameters[evalcontinously.EvalContinously.maxHighJumpKey] = maxHighJump

    meanKey2 = 0
    meanKey3 = 0

    meanList = (5, 8, 13, 21, 34, 38, 50, 55, 89, 100, 144, 200, 233)

    for meanKey in meanList:
        for endMean in meanList:
            if endMean == meanKey:
                runParameters[evalcontinously.EvalContinouslyMean.meanKey] = meanKey
                runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = meanKey2
                runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = meanKey3
                runParameters[evalcontinously.EvalContinouslyMean.endMeanKey] = endMean

                descr = str.format("\"Mean {:3} {:3} {:3} {:3}\"", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                                runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                                runParameters[evalcontinously.EvalContinouslyMean.mean3Key],
                                                runParameters[evalcontinously.EvalContinouslyMean.endMeanKey])

                runParameters[evalrunner.EvalRunner.transactionPrinterKey] = None

                testEvaluation = TestEvalContinously3( runParameters )
                testEvaluation.run( descr )
                totalEvaluationResult.updateTotalResult( testEvaluation.resultEvaluationDict, descr)

    for meanKey in meanList:
        for meanKey2 in meanList:
            if meanKey2 > meanKey:
                for endMean in meanList:
                    if endMean == meanKey or endMean == meanKey2:
                        runParameters[evalcontinously.EvalContinouslyMean.meanKey] = meanKey
                        runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = meanKey2
                        runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = meanKey3
                        runParameters[evalcontinously.EvalContinouslyMean.endMeanKey] = endMean

                        descr = str.format("\"Mean {:3} {:3} {:3} {:3}\"", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                                runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                                runParameters[evalcontinously.EvalContinouslyMean.mean3Key],
                                                runParameters[evalcontinously.EvalContinouslyMean.endMeanKey])

                        runParameters[evalrunner.EvalRunner.transactionPrinterKey] = None

                        testEvaluation = TestEvalContinously3( runParameters )
                        testEvaluation.run( descr )
                        totalEvaluationResult.updateTotalResult( testEvaluation.resultEvaluationDict, descr)

    for meanKey in meanList:
        for meanKey2 in meanList:
            if meanKey2 > meanKey:
                for meanKey3 in meanList:
                    if (meanKey3 > meanKey2):
                        for endMean in meanList:
                            if endMean == meanKey or endMean == meanKey2 or endMean == meanKey3:
                                runParameters[evalcontinously.EvalContinouslyMean.meanKey] = meanKey
                                runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = meanKey2
                                runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = meanKey3
                                runParameters[evalcontinously.EvalContinouslyMean.endMeanKey] = endMean

                                descr = str.format("\"Mean {:3} {:3} {:3} {:3}\"", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                                runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                                runParameters[evalcontinously.EvalContinouslyMean.mean3Key],
                                                runParameters[evalcontinously.EvalContinouslyMean.endMeanKey])

                                runParameters[evalrunner.EvalRunner.transactionPrinterKey] = None

                                testEvaluation = TestEvalContinously3( runParameters )
                                testEvaluation.run( descr )
                                totalEvaluationResult.updateTotalResult( testEvaluation.resultEvaluationDict, descr)




    print ""
    print str.format( '{:10} {:20} {:>10.2f}', "Best", totalEvaluationResult.maxTotalDescr1, totalEvaluationResult.maxTotalResult1 )
    print str.format( '{:10} {:20} {:>10.2f}', "2nd", totalEvaluationResult.maxTotalDescr2, totalEvaluationResult.maxTotalResult2 )
    print str.format( '{:10} {:20} {:>10.2f}', "3rd", totalEvaluationResult.maxTotalDescr3, totalEvaluationResult.maxTotalResult3 )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    runPutEvaluations()
    '''
    runParameters = dict()

    indexList = [
                  indexdatabase.IndexDatabase.idxATX,
                  indexdatabase.IndexDatabase.idxCAC,
                  indexdatabase.IndexDatabase.idxDax,
                  indexdatabase.IndexDatabase.idxDowJones,
                  indexdatabase.IndexDatabase.idxEStoxx50,
                  indexdatabase.IndexDatabase.idxFTS100,
                  indexdatabase.IndexDatabase.idxFtseMib,
                  indexdatabase.IndexDatabase.idxHangSeng,
                  indexdatabase.IndexDatabase.idxIbex,
                  indexdatabase.IndexDatabase.idxMDax,
                  indexdatabase.IndexDatabase.idxNasdaq100,
                  indexdatabase.IndexDatabase.idxNikkei,
                  indexdatabase.IndexDatabase.idxSDax,
                  indexdatabase.IndexDatabase.idxSMI,
                  indexdatabase.IndexDatabase.idxSP500,
                  indexdatabase.IndexDatabase.idxTecDax
                  #indexdatabase.IndexDatabase.idxGold,
                  #indexdatabase.IndexDatabase.idxBrent
                ]

    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = False

    runParameters[evalcontinously.EvalContinously.maxDaysKey] = 0
    runParameters[evalcontinously.EvalContinously.maxWinKey] = 0.0

    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = True
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = 200
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = 200
    runParameters[evalcontinously.EvalContinouslyMean.startOffsetKey] = 0.0
    runParameters[evalcontinously.EvalContinouslyMean.endOffsetKey] = 0.0


    descr = str.format("Mean {:3} {:3} {:3}", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)

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

    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 8.0

    maxLoss = 0.0   # -0.01
    maxJump = 0.0   # -0.02
    runParameters[evalcontinously.EvalContinously.maxDaysKey] = 0
    runParameters[evalcontinously.EvalContinously.maxWinKey] = 0.02
    runParameters[evalcontinously.EvalContinously.maxLossKey] = maxLoss
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = maxJump
    #runParameters[evalcontinously.EvalContinously.maxHighJumpKey] = -0.02


    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = 21
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = 200
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = 200

    #runParameters[evalcontinously.EvalContinouslyMean.gradKey] = 21
    #runParameters[evalcontinously.EvalContinouslyMean.minGradKey] = 0.04

    descr = str.format("\"Mean {:3} {:3} {:3}\"", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                              runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)

    testEvaluation = TestEvalContinously3( runParameters )
    #testEvaluation = TestEvalContinouslyGrad( runParameters )
    testEvaluation.run( descr, indexList )

    descr = str.format("\"mL {:3.2f} mJ {:3.2f}\"", maxLoss, maxJump)
    #runParameters[evalrunner.EvalRunner.transactionPrinterKey] = MultiEvalPrinter()

    multiTestEvaluation = MulitEvalRunner( runParameters )
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run( descr )

    print ""

    runParameters[evalrunner.EvalRunner.idxDistanceKey] = 10.0

    #for maxWin in (0.00, -0.01, -0.02, -0.03, -0.04, -0.05, -0.06):
    #for meanKey1 in (8,13, 21, 34, 55, 89, 144):
    meanKey = 5
    meanKey1 = 8
    maxLoss = 0.05
    maxJump = 0.00
    maxWin = 0.00
    runParameters[evalcontinously.EvalContinouslyMean.isCallKey] = False
    runParameters[evalcontinously.EvalContinouslyMean.meanKey] = meanKey
    runParameters[evalcontinously.EvalContinouslyMean.mean2Key] = meanKey1
    runParameters[evalcontinously.EvalContinouslyMean.mean3Key] = 200

    #for maxJump in (0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06):
    #for maxJump in (0.05, 0.01, 0.00):
        #maxLoss = 0.00
    runParameters[evalcontinously.EvalContinously.maxWinKey] = maxWin
    runParameters[evalcontinously.EvalContinously.maxLossKey] = maxLoss
    runParameters[evalcontinously.EvalContinously.maxJumpKey] = maxJump
    runParameters[evalcontinously.EvalContinously.maxHighJumpKey] = 0.0

    descr = str.format("\"Mean {:3} {:3} {:3}\"", runParameters[evalcontinously.EvalContinouslyMean.meanKey],
                                            runParameters[evalcontinously.EvalContinouslyMean.mean2Key],
                                            runParameters[evalcontinously.EvalContinouslyMean.mean3Key],)

    runParameters[evalrunner.EvalRunner.transactionPrinterKey] = None

    testEvaluation = TestEvalContinously3( runParameters )
    testEvaluation.run( descr, indexList )
    #print ""

    #runParameters[evalrunner.EvalRunner.transactionPrinterKey] = MultiEvalPrinter()

    descr = str.format("\"mL {:3.2f} mJ {:3.2f}\"", maxLoss, maxJump)
    multiTestEvaluation = MulitEvalRunner( runParameters )
    multiTestEvaluation.setTransactionListDict(testEvaluation.transactionListDict)
    multiTestEvaluation.run( descr )

    print ""
    '''
