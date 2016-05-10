'''
Created on 22.04.2016

@author: selen00r
'''

import fetchdata
import indexdatabase


def requestBuy():
    indexDB = indexdatabase.getIndexDatabase()

    print "End of month values:"
    for idxName in indexDB.allIndices:
        fetch = fetchdata.FetchData( idxName )

        idxData0 = fetch.fetchLastDayOfMonth( 2016, 4)
        idxData1 = fetch.fetchLastDayOfMonth( 2016, 3)
        idxData2 = fetch.fetchLastDayOfMonth( 2016, 1)
        idxData3 = fetch.fetchLastDayOfMonth( 2015, 10)
        idxData4 = fetch.fetchLastDayOfMonth( 2015, 4)
        print str.format( '{:10} {:> 6.3f} {:> 6.3f} {:> 6.3f} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10}',
                          idxName,
                          ((idxData0.close / idxData0.mean13)-1.0), ((idxData0.close / idxData0.mean21)-1.0), ((idxData0.close / idxData0.mean200)-1.0),
                          idxData0.date.year, idxData0.date.month, idxData0.date.day, idxData0.close,
                          idxData1.date.year, idxData1.date.month, idxData1.date.day, idxData1.close,
                          idxData2.date.year, idxData2.date.month, idxData2.date.day, idxData2.close,
                          idxData3.date.year, idxData3.date.month, idxData3.date.day, idxData3.close,
                          idxData4.date.year, idxData4.date.month, idxData4.date.day, idxData4.close )

    print "History values:"
    for idxName in indexDB.allIndices:
        fetch = fetchdata.FetchData( idxName )

        idxData0 = fetch.fetchHistoryValue( 2016, 5, 10)
        idxData1 = fetch.fetchHistoryValue( 2016, 4, 10)
        idxData2 = fetch.fetchHistoryValue( 2016, 2, 10)
        idxData3 = fetch.fetchHistoryValue( 2015, 11, 10)
        idxData4 = fetch.fetchHistoryValue( 2015, 5, 10)

        print str.format( '{:10} {:> 6.3f} {:> 6.3f} {:> 6.3f} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10} {:4}-{:02}-{:02} {:>10}',
                          idxName,
                          ((idxData0.close / idxData0.mean13)-1.0), ((idxData0.close / idxData0.mean21)-1.0), ((idxData0.close / idxData0.mean200)-1.0),
                          idxData0.date.year, idxData0.date.month, idxData0.date.day, idxData0.close,
                          idxData1.date.year, idxData1.date.month, idxData1.date.day, idxData1.close,
                          idxData2.date.year, idxData2.date.month, idxData2.date.day, idxData2.close,
                          idxData3.date.year, idxData3.date.month, idxData3.date.day, idxData3.close,
                          idxData4.date.year, idxData4.date.month, idxData4.date.day, idxData4.close )

if __name__ == '__main__':
    requestBuy()