'''
Created on Nov 9, 2011

@author: ppa
'''
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.dam.googleFinance import GoogleFinance

import logging
import sqlite3
LOG = logging.getLogger()

class GoogleDAM(BaseDAM):
    ''' Google DAO '''

    def __init__(self):
        ''' constructor '''
        super(GoogleDAM, self).__init__()
        self.__gf = GoogleFinance()

    def readQuotes(self, start, end):
        ''' read quotes from google Financial'''
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return []

        return self.__gf.getQuotes(self.symbol, start, end)

    def readTicks(self, start, end, existingDB=''):
        ''' read ticks from google Financial'''
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return []
        if len(existingDB)>0:
            try:
                self.populateProcessedTicksFromDB(existingDB)
            except Exception,e:
                print e
           
        return self.__gf.getTicks(self.symbol, start, end)
        
    def populateProcessedTicksFromDB(self, existingDB):
        #this will need to be dynamic or moved somewhere else
        conn = sqlite3.connect("../tools/{0}.sqlite".format(existingDB)) 
        cursor = conn.execute("SELECT symbol,time FROM ticks")
        for row in cursor:
            symbol = row[0]
            time = row[1]
            dataAppended = "{0}&{1}".format(symbol,time)
            self.__gf.processedTicks[dataAppended] = True                
        conn.close()

    def readFundamental(self):
        ''' read fundamental '''
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return {}

        return self.__gf.getFinancials(self.symbol)
