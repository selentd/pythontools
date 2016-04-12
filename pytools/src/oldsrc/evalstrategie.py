'''
Created on 03.09.2013

@author: selen00r
'''

import collections

from indexdata import IndexData

class EvalStrategie:
    def __init__(self, name, buyStrategieList, sellStrategieList):
        self.name = name
        self.buyStrategieList = list()
        self.buyStrategieList += buyStrategieList
        self.sellStrategieList = list()
        self.sellStrategieList += sellStrategieList
        self.state = 0
        self.indexBuy = IndexData()
        self.indexHistory = collections.deque()

    def evaluateBuy(self, indexData):
        checkBuy = True
        for strategie in self.buyStrategieList:
            checkBuy = checkBuy and strategie.evaluateBuy(indexData)
        return checkBuy

    def evaluateSell(self, indexData):
        checkSell = False
        for strategie in self.sellStrategieList:
            checkSell = checkSell or strategie.evaluateSell(indexData)
        return checkSell

    def evaluateKnockOut(self, indexData):
        checkKnockOut = False
        for strategie in self.sellStrategieList:
            checkKnockOut = checkKnockOut or strategie.evaluateKnockOut(indexData)
        return checkKnockOut

    def evaluate(self, indexData, indexResultHistory ):
        for strategie in self.buyStrategieList:
            strategie.updateState(indexData, self.indexBuy)
        for strategie in self.sellStrategieList:
            strategie.updateState(indexData, self.indexBuy)

        if self.state == 0:
            checkBuy = self.evaluateBuy(indexData)
            if checkBuy == True:
                self.indexHistory = collections.deque()
                self.indexBuy = indexData
                self.state = 1
        else:
            checkSell = self.evaluateSell(indexData)
            checkKnockOut = self.evaluateKnockOut(indexData)
            if checkSell == True or checkKnockOut == True:
                indexResultHistory.addIndexResult( IndexResult( self.indexBuy,
                                                                indexData,
                                                                self.indexHistory,
                                                                checkKnockOut) )
                self.state = 0
            else:
                self.indexHistory.append(indexData)

    def evaluateIndex(self, indexHistory, indexResultHistory):
        for indexData in indexHistory.indexHistory:
            self.evaluate(indexData, indexResultHistory)





