import sqlite3
import optparse

class DataPoint:
    def __init__ (self, date, symbol, volume, percent):  
         self.date = date
         self.optiondate = None
         self.database = None
         self.symbol = symbol  
         self.volume = volume  
         self.percent = percent

class StockQueries():
    def __init__(self):
        ''' constructor '''
        self.message = "Successfully Initialized StockQueries Class"
        self.visitedDataPoints = []
        self.filteredDataPoints = []
        print(self.message)
        
    def populateDataPoints(self, tableName, sqlLitePath):
        conn = sqlite3.connect(sqlLitePath)
        
        visitedSymbols = []
        sql = "SELECT DISTINCT symbol,time,volume FROM {0} where time like '%{1}%' ORDER BY symbol,time".format(tableName,self.optiondate)
        print sql
        cursor = conn.execute(sql)
        
        for row in cursor:
            symbol = row[0]            
            time = row[1]
            curVolume = float(row[2])
            
            if symbol not in visitedSymbols:
                visitedSymbols.append(symbol)
                prevVolume = 0
            
            if prevVolume != 0:
                percent = (round((curVolume - prevVolume)/prevVolume,5)) * 100                
                prevVolume = float(row[2])
                dp = DataPoint(time,symbol,curVolume,percent)

            else:                
                dp = DataPoint(time,symbol,curVolume,0)
                prevVolume = float(row[2])
                
            self.visitedDataPoints.append(dp)

        conn.close()
        
    def filterDataPoints(self):
        for index in range(len(self.visitedDataPoints)):
            item = self.visitedDataPoints[index]
            if(index == len(self.visitedDataPoints)-1):
                dp = DataPoint(item.date,item.symbol,item.volume,item.percent)
                self.filteredDataPoints.append(dp)
            elif(item.symbol != self.visitedDataPoints[index+1].symbol):
                dp = DataPoint(item.date,item.symbol,item.volume,item.percent)
                self.filteredDataPoints.append(dp)
                
    def printDataPointsToFile(self):
        f = open('output/export','w')
        f.write("DATE,SYMBOL,VOLUME,%_DIFF_FROM_PRIOR\n")
        for item in sorted(self.filteredDataPoints, key=lambda datapoint: datapoint.percent):
            if(item.percent>50 or item.percent<-50):
                f.write("{0},{1},{2},{3}\n".format(item.date,item.symbol,item.volume,item.percent))
        f.close()
        
    def getOptions(self):
        ''' crawling data and save to hbase '''
        parser = optparse.OptionParser("Usage: %prog [options]")
        parser.add_option("-t", "--date", dest = "date", type = "string",
                          help = "write help here")
        parser.add_option("-d", "--database", dest = "database", type = "string",
                          help = "write help here")                          
        (options, _) = parser.parse_args()

        # get symbols
        if options.date is None:
            print("Please provide valid date yyyy-mm-dd: %s" % options.date)
            exit(4)
        else:
            self.optiondate = options.date
            
        if options.database is None:
            print("Please provide a valid datebase: %s" % options.database)
            exit(4)
        else:
            self.database = options.database            

if __name__ == '__main__':
    stockQueries = StockQueries()
    stockQueries.getOptions()
    stockQueries.populateDataPoints("ticks", ("{0}.sqlite").format(stockQueries.database))
    stockQueries.filterDataPoints()
    stockQueries.printDataPointsToFile()
