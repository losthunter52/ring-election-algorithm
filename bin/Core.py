import ast
import socket
from .Sender import Sender
from . import Settings
from threading import Thread

# ---------------------------------------------------------------------------
# Master Receiver Class
# ---------------------------------------------------------------------------

class Processor(Thread):
    # init method
    def __init__(self, database):
        # initializes the communication receiver module
        Thread.__init__(self)
        self.database = database
        self.is_master = False
        self.connection = True

    def apply(self, json):
        x = 1

    def election(self, json):
        if json['MESSAGE'] == 'PARTICIPANT':
            x=1
        elif json['MESSAGE'] == 'ELECTED':
            x=1
    
    def communicate(self):
        x =1 
        self.connection = False

    def communication(self, json):
        if json['MESSAGE'] == 'REQUEST':
            destiny_ip = json['SENDER_IP']
            destiny_port = json['SENDER_PORT']
            json = {
                'TYPE': 'COMMUNICATION',
                'MESSAGE': 'RESPONSE',
                'SENDER_IP': Settings.SELF_IP,
                'SENDER_PORT': Settings.SELF_PORT, 
            }
            send = Sender(json, destiny_ip, destiny_port)
            send.start()
            send.join()
        elif json['MESSAGE'] == 'RESPONSE':
            self.connection = True

    def caller(self):
        json = self.database.getJson()
        if json['TYPE'] == 'COMMUNICATION':
            self.communication(json)
        elif json['TYPE'] == 'ELECTION':
            self.election(json)

    def management(self):
        timeout = Settings.COMMUNICATION_TIMEOUT
        self.communicate()
        while(True):
            self.caller()
            if self.connection == True:
                break
            timeout -= 1
            if timeout < 0:
                self.apply()
        

    # run method
    def run(self):
        # start the MasterReceiver master thread
        print("Core Actived")
        while(True):
            self.management()