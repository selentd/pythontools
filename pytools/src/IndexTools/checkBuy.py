'''
Created on 30.08.2016

@author: SELEN00R
'''

import datetime

import indexdatabase
import indexselector

def checkBuy():
    startDate = datetime.datetime( 2016, 1, 1)
    endDate = datetime.datetime.today()

    selector = indexselector.IndexSelectorRSIAvgMonth([1,3,6,12], True)
    while startDate < endDate:
        idxList = selector.select( startDate, startDate + datetime.timedelta(1) )
        print str.format( '{:%Y-%m-%d} {:10} {: 2.4f} {:10} {: 2.4f} {:10} {: 2.4f} {:10} {: 2.4f} {:10} {: 2.4f}',
                          startDate,
                          idxList[0][0], idxList[0][1],
                          idxList[1][0], idxList[1][1],
                          idxList[2][0], idxList[2][1],
                          idxList[3][0], idxList[3][1],
                          idxList[4][0], idxList[4][1]
                        )
        startDate = startDate + datetime.timedelta( 1 )


if __name__ == '__main__':
    checkBuy()