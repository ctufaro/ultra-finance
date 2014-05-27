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
		
		cursor = conn.execute("SELECT * FROM %s order by symbol,time " % tableName)		
		f = open('output/vwap','w')
		f.write("Symbol,Time,Price,Volume,VP,TotalVP,TotalV,VWAP \n")
		
		for row in cursor:	
		
			symbol = row[1]
			time = row[2]
			price = (float(row[4]) + float(row[5]) + float(row[6])) / 3
			volume = float(row[7])
			vp = float(volume)*float(price)
			
			if(time.split( )[1] == '09:30:00'):
				totalVP = 0
				totalV = 0
				start = False
			
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

			f.write("%s,%s,%s,%s,%s,%s,%s,%s \n" % (symbol,time,price,volume,vp,totalVP,totalV,vwap))
			
			count = count + 1

		conn.close()
		f.close()	

if __name__ == '__main__':
	vwap = VWAP()
	vwap.populateDataPoints("ticks","stock.sqlite")
