'''
Created on 31.08.2016

@author: SELEN00R
'''

import evalbest

if __name__ == '__main__':

    runParameters = dict()

    runParameters[evalrunner.EvalRunner.startDateKey] = datetime.datetime(2016,1,1)
    runParameters[evalrunner.EvalRunner.endDateKey] = datetime.datetime.now()

    runParameters[evalrunner.EvalRunner.startInvestKey] = 1000.0
    runParameters[evalrunner.EvalRunner.maxInvestKey] = 100000.0
    runParameters[evalrunner.EvalRunner.fixedInvestKey] = False

    evaluation = evalbest.EvalBest(runParameters)
