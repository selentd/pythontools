
import collections

from indexdata import IndexData

class IndexResult:
    def __init__(self, indexBuy, indexSell, indexHistory, knockOut ):
        self.indexBuy = indexBuy
        self.indexSell = indexSell
        self.indexHistory = indexHistory
        self.knockOut = knockOut
        
class IndexResultHistory:
    def __init__(self):
        self.resultHistory = collections.deque()
        
    def addIndexResult(self, result):
        self.resultHistory.append(result)
                        
    def evaluateResult(self, result):
        for indexResult in self.resultHistory:
            result.evaluate( indexResult )
            
    def exportResult(self, exportFunc, writer ):
        for indexResult in self.resultHistory:
            exportFunc( indexResult, writer )
