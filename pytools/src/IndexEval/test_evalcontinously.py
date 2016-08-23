'''
Created on 01.04.2016

@author: selen00r
'''

import evalcontinously
import evalresult
import evalrunner

class TestEvalContinously(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyMean( self.dbName, indexName, self.runParameters )
        return evaluation

class TestEvalContinouslyGrad(evalrunner.EvalRunner):

    def __init__(self, runParameters):
        evalrunner.EvalRunner.__init__(self, runParameters)

    def _createIndexEvaluation(self, indexName):
        evaluation = evalcontinously.EvalContinouslyGrad( self.dbName, indexName, self.runParameters )
        return evaluation

if __name__ == "__main__":
    pass
