'''
Created on 13.12.2014

@author: diesel
'''

from evalindexdata import EvalIndexDataBuy
from evalindexdata import EvalIndexDataSell

class EvalCallMW200MeanBuy( EvalIndexDataBuy ):
    def updateState(self, indexData, lastBuy):
        pass        

class EvalCallMW200MeanMeanSell( EvalIndexDataSell ):
    def updateState(self, indexData, lastBuy):
        pass

