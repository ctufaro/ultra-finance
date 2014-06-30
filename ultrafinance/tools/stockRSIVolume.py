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

    def getPreviousDayPriceData(self,dates,close):
        count = 0
        firstBusinessDay = dates[0].split(' ')[0]
        currentBusinessDay = dates[-1].split(' ')[0]
        previousBusinessDay = None
        previousClose = None
        for d in reversed(dates):
            if currentBusinessDay.split(' ')[0] != d.split(' ')[0]:
                previousBusinessDay = d.split(' ')[0]
                previousClose = close[::-1][count] #reversed closed prices
                break
            count += 1
        return firstBusinessDay,previousBusinessDay,currentBusinessDay,previousClose
        
    def getVolume(self, dates, volume, currentDay, previousDay):
        volume = volume[::-1]
        currentVolume = 0
        previousVolume = 0
        count = 0
        for d in reversed(dates):
            if currentDay == d.split(' ')[0]:
                currentVolume += int(volume[count])          
            elif previousDay == d.split(' ')[0]:
                previousVolume += int(volume[count]) 
            count += 1
        return previousVolume,currentVolume
    
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
    f = open('crap.csv','w')
    #stockRSIVolume.getCurrentPositions()
    stockData = stockRSIVolume.getStockData()
    f.write("symbol,rsi,prev_close,current_close,change_in_close,business_date,volume\n")
    for key in stockData:
        pennyData = stockData[key]
        fbd,pbd,cbd,pclose = stockRSIVolume.getPreviousDayPriceData(pennyData.time,pennyData.close)
        previousVolume,currentVolume = stockRSIVolume.getVolume(pennyData.time,pennyData.volume,cbd,pbd)    
        rsi = stockRSIVolume.getRSI(pennyData.close)[-1]
        #symbol, currentRSI, previousclose, currentClose, changeInClose, currentDate, currentVolume
        f.write("{0},{1},{2},{3},{4},{5},{6}\n".format(pennyData.symbol, rsi, pclose, pennyData.close[-1],  ((pennyData.close[-1] - pclose)/pclose)*100, cbd, currentVolume))
    f.close()