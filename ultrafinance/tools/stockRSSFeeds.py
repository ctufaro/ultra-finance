import feedparser
import time
import requests
from ultrafinance.tools.stockNotifier import StockNotifier


keywords = ['announces']

f = open('output/StockNews.html','w')
f.write('<HTML><BODY>')
with open('../../data/symbols/penny.list','r') as r:
    for symbol in r:
        url = 'http://www.google.com/finance/company_news?q=%s&output=RSS' % symbol
        txt = requests.get(url).text
        d = feedparser.parse(txt)
        for i in range(0,len(d.entries)):
            description = d.entries[i].description.encode('utf-8')
            title = d.entries[i].title.encode('utf-8')
            datepublished = d.entries[i].published.encode('utf-8')            
            if any(word in description.lower() for word in keywords):
                #f.write('<h3>[{0}] {1}-{2}</h3>'.format(symbol,title,datepublished))
                f.write('[{0}]{1}'.format(symbol,description))
        #time.sleep(1)
f.write('</BODY></HTML>')
f.close()
r.close()