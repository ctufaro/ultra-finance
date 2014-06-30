import urllib2
import sqlite3
import numpy as np

class Positions():
    def __init__ (self, symbol, quantity, date):  
         self.symbol = symbol  
         self.quantity = quantity  
         self.date = date
         
class RSIVolume():
    def __init__ (self):  
         self.symbol = []  
         self.time = []  
         self.close = []
         self.volume = []           
         
class StockRSIVolume():

    def __init__(self):
        self.currentPositions = []    
        self.currentRSIVolumeCalulations = []
        
    def getCurrentPositions(self):
        gitAddress = 'https://raw.githubusercontent.com/ctufaro/ultra-finance/master/ultrafinance/tools/input/positions.txt'
        f = urllib2.urlopen(gitAddress)
        for line in f:
            splitArray = line.split(',')
            self.currentPositions.append(Positions(splitArray[0],splitArray[1],splitArray[2]))
        f.close()
        
    def getRSI(self, prices, n=10):
        deltas = np.diff(prices)
        seed = deltas[:n+1]
        up = seed[seed>=0].sum()/n
        down = -seed[seed<0].sum()/n
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100./(1.+rs)

        for i in range(n, len(prices)):
            delta = deltas[i-1] # cause the diff is 1 shorter

            if delta>0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(n-1) + upval)/n
            down = (down*(n-1) + downval)/n

            rs = up/down
            rsi[i] = 100. - 100./(1.+rs)
        return rsi         

    def getStockData(self):
        stockData = {}
        conn = sqlite3.connect('penny.sqlite')        
        selectSQL = "SELECT symbol,time,close,volume FROM ticks order by symbol,time"
        cursor = conn.execute(selectSQL)
        listOfRSIVolume = None
        for row in cursor:               
            if row[0] not in stockData:
                listOfRSIVolume = RSIVolume()
                listOfRSIVolume.symbol = row[0]
            listOfRSIVolume.time.append(row[1])
            listOfRSIVolume.close.append(row[2])
            listOfRSIVolume.volume.append(int(row[3]))
            stockData[row[0]] = listOfRSIVolume
        conn.close()
        return stockData

if __name__ == '__main__':
    stockRSIVolume = StockRSIVolume()
    #stockRSIVolume.getCurrentPositions()
    stockData = stockRSIVolume.getStockData()
    for key in stockData:
        sd = stockData[key]
        rsi = stockRSIVolume.getRSI(sd.close)[-1]
        #symbol, currentRSI, currentClose, changeInClose, currentDate, currentVolume, changeInVolume
        #print sd.symbol,rsi,sd.close[-1],sd.time[-1],sd.time[0]    
