import smtplib
import ConfigParser

class StockNotifier(object):

    def __init__(self):    
        configSection = "EmailSettings"
        self.config = self.initConfig()        
        self.username = self.configSectionMap(configSection)['username']
        self.password = self.configSectionMap(configSection)['password']
        self.fromaddr = self.configSectionMap(configSection)['fromaddr']
        self.highpriorityemailaddr = self.configSectionMap(configSection)['highpriorityemailaddr']
        self.normalpriorityemailaddr = self.configSectionMap(configSection)['normalpriorityemailaddr']
        self.normalpriorityemailaddr = self.configSectionMap(configSection)['normalpriorityemailaddr']
        self.enablesending = self.configSectionMap(configSection)['enablesending']
        
    def initConfig(self):
        Config = ConfigParser.ConfigParser()
        Config.read("settings.ini")
        return Config
    
    def sendNotification(self, priority, msg):
        if(priority == 'HIGH'):
            self.smtpMail(self.highpriorityemailaddr, msg)
        elif(priority == 'NORMAL'):
            self.smtpMail(self.normalpriorityemailaddr, msg)
            
    def configSectionMap(self,section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1            
                
    def smtpMail(self, to, msg):         
        formattedMessage = '\n'.join(msg)
        if self.enablesending == True:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(self.username,self.password)
            server.sendmail(self.fromaddr, to, formattedMessage)
            server.quit()
        else:
            print formattedMessage