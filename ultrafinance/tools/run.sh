sudo python stockCrawler.py -f /home/pi/Projects/ultra-finance/data/symbols/SPY500.list
sudo python stockQueries.py
sudo python /home/pi/Projects/python-emailer/sendEmail.py SPY500

sudo python stockCrawler.py -f /home/pi/Projects/ultra-finance/data/symbols/technology.list
sudo python stockQueries.py
sudo python /home/pi/Projects/python-emailer/sendEmail.py Technology

sudo python stockCrawler.py -f /home/pi/Projects/ultra-finance/data/symbols/energy.list
sudo python stockQueries.py
sudo python /home/pi/Projects/python-emailer/sendEmail.py Energy

