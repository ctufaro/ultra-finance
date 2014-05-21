import sqlite3

class DataPoint:
	def __init__ (self, date, symbol, volume, percent):  
         self.date = date  
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
		cursor = conn.execute("SELECT DISTINCT symbol,time,volume FROM {0} ORDER BY symbol,time".format(tableName))
		
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
				
	def printDataPoints(self):
		for item in self.filteredDataPoints:
			if(item.percent>50):
				print("DATE:{0}, SYMBOL:{1}, VOLUME:{2}, %_DIFF_FROM_PRIOR:{3}".format(item.date,item.symbol,item.volume,item.percent))
		
if __name__ == '__main__':
	stockQueries = StockQueries()
	stockQueries.populateDataPoints("quotes", "~\Projects\ultra-finance\ultrafinance\data\stock.sqlite")
	stockQueries.filterDataPoints()
	stockQueries.printDataPoints()
