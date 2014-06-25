sudo python stockCrawler.py -f /home/pi/Projects/ultra-finance/data/symbols/penny.list -d penny -t tick -p 15 -c true
sudo python stockQueries.py -r volume -d penny -t ticks
sudo python /home/pi/Projects/python-emailer/sendEmail.py Penny

