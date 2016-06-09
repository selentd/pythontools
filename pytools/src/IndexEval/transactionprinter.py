'''
Created on 11.12.2015

@author: diesel
'''

import evalresult
import indexdata

class TransactionPrinter:

    def printTransaction(self, TransactionResult, hasResult = True):
        pass

    def printTransactionResult(self, transactionResult, result, resultEuro, hasResult = True):
        pass

class TransactionPrinterPutWinner(TransactionPrinter):

    def printTransaction(self, transactionResult, hasResult=True):
        indexBuy = transactionResult.indexBuy
        indexSell = transactionResult.indexSell

        if indexBuy.close > indexSell.close:

            print str.format( "{10} {:%Y-%m-%d} {:%Y-%m-%d} {:10.2f} {:10.2f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {: 2.4f} {:3}",
                          transactionResult.indexName,
                          transactionResult.indexBuy.date,
                          transactionResult.indexSell.date,
                          transactionResult.indexBuy.close,
                          transactionResult.indexSell.close,
                          1.0 - (indexBuy.low / indexBuy.open),
                          1.0 - (indexBuy.high / indexBuy.open),
                          1.0 - (indexSell.close / indexBuy.close),
                          1.0 - (transactionResult.getLowValue() / indexBuy.close),
                          1.0 - (transactionResult.getHighValue() / indexBuy.close),
                          transactionResult.indexHistory.len() )
