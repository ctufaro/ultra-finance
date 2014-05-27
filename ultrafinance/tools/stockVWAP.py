import sqlite3

class DataPoint:
	def __init__ (self, date, symbol, volume, percent):  
         self.date = date  
         self.symbol = symbol  
         self.volume = volume  
         self.percent = percent

class VWAP():
	def __init__(self):
		''' constructor '''
		self.message = "Successfully Initialized VWAP Class"
		print(self.message)
	
	def populateDataPoints(self, tableName, sqlLitePath):
		conn = sqlite3.connect(sqlLitePath)
		
		totalVP = 0
		totalV = 0
		count = 0
		
		totalVPList = []
		totalVList = []
		
		start = False
		
		cursor = conn.execute("SELECT * FROM %s where symbol = 'AMZN' AND time >= '2014-05-23 09:30:00' AND time < '2014-05-23 09:35:00' order by time" % tableName)
		
		for row in cursor:	
		
			symbol = row[1]
			time = row[2]
			price = row[6]
			volume = float(row[7])
			vp = float(volume)*float(price)
			
			if start == False:
				totalVPList.append(vp)
				totalVList.append(volume)
				totalV = volume
				totalVP = vp
				start = True
			else:
				totalVP = vp + totalVPList[count-1]
				totalV = volume + totalVList[count-1]
				totalVList.append(totalV)
				totalVPList.append(totalVP)
				
			vwap = totalVP/totalV		
				
		
			print "Symbol:%s Time:%s Price:%s Volume:%s VP:%s TotalVP:%s TotalV:%s VWAP:%s" % (symbol,time,price,volume,vp,totalVP,totalV,vwap)
			
			count = count + 1

		conn.close()		

if __name__ == '__main__':
	vwap = VWAP()
	vwap.populateDataPoints("ticks","stock.sqlite")
