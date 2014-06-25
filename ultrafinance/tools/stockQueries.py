import sqlite3
import optparse

class DataPoint:
    def __init__ (self, date, symbol, volume, percent, close):  
         self.date = date  
         self.symbol = symbol  
         self.volume = volume  
         self.percent = percent
         self.close = close
         self.request = None
         self.databaseFile = None
         self.table = None

class StockQueries():
    def __init__(self):
        ''' constructor '''
        self.message = "Successfully Initialized StockQueries Class"
        self.visitedDataPoints = []
        self.filteredDataPoints = []
        print(self.message)
        
    def getOptions(self):
        parser = optparse.OptionParser("Usage: %prog [options]")
        parser.add_option("-r", "--request", dest = "request", type = "string",
                          help = "query request")
        parser.add_option("-d", "--databaseFile", dest = "databaseFile", type = "string",
                          help = "database name")
        parser.add_option("-t", "--table", dest = "table", type = "string",
                          help = "table name actually")
        (options, _) = parser.parse_args()

        if options.request is None:
            print("Please provide a request -r: %s" % options.request)
            exit(4)
        else:
            self.request = options.request
            
        if options.databaseFile is None:
            print("Please provide a database name -d: %s" % options.databaseFile)
            exit(4)
        else:
            self.databaseFile = options.databaseFile            

        if options.table is None:
            print("Please provide a type -t: %s" % options.table)
            exit(4)
        else:
            self.table = options.table            
        
    def populateDataPoints(self):
        tableName = self.table
        sqlLitePath = "{0}.sqlite".format(self.databaseFile)        
        conn = sqlite3.connect(sqlLitePath)        
        visitedSymbols = []
        selectSQL = "SELECT distinct symbol, SUBSTR(time,0,11) [time], sum(volume) [volume], close from {0} GROUP BY symbol,SUBSTR(time,0,11) ORDER BY id,symbol,SUBSTR(time,0,11)".format(tableName)
        cursor = conn.execute(selectSQL)
        
        for row in cursor:
            symbol = row[0]            
            time = row[1]
            curVolume = float(row[2])
            close = float(row[3])
            
            if symbol not in visitedSymbols:
                visitedSymbols.append(symbol)
                prevVolume = 0
            
            if prevVolume != 0:
                percent = (round((curVolume - prevVolume)/prevVolume,5)) * 100                
                prevVolume = float(row[2])
                dp = DataPoint(time,symbol,curVolume,percent,close)

            else:                
                dp = DataPoint(time,symbol,curVolume,0,close)
                prevVolume = float(row[2])
                
            self.visitedDataPoints.append(dp)        

        conn.close()
        
    def filterDataPoints(self):
        for index in range(len(self.visitedDataPoints)):
            item = self.visitedDataPoints[index]
            if(index == len(self.visitedDataPoints)-1):
                dp = DataPoint(item.date,item.symbol,item.volume,item.percent,item.close)
                self.filteredDataPoints.append(dp)
            elif(item.symbol != self.visitedDataPoints[index+1].symbol):
                dp = DataPoint(item.date,item.symbol,item.volume,item.percent,item.close)
                self.filteredDataPoints.append(dp)
                
    def printDataPointsToFile(self):
        f = open('output/export.csv','w')
        f.write("DATE,SYMBOL,VOLUME,%_DIFF_FROM_PRIOR,CLOSE\n")
        for item in sorted(self.filteredDataPoints, key=lambda datapoint: (datapoint.volume,datapoint.percent), reverse=True):
            textToWrite = "{0},{1},{2},{3},{4}\n".format(item.date,item.symbol,item.volume,item.percent,item.close)
            f.write(textToWrite)
        f.close()
        
    def dropDatabase(self, tableName, sqlLitePath):
        conn = sqlite3.connect(sqlLitePath)        
        conn.execute("DROP TABLE %s" % tableName)
        conn.close()
        print("Successfully Dropped Table")

if __name__ == '__main__':
    stockQueries = StockQueries()
    stockQueries.getOptions()
    stockQueries.populateDataPoints()
    stockQueries.filterDataPoints()
    stockQueries.printDataPointsToFile()
