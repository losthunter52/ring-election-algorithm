import ast
import socket
import time
from . import Settings
from threading import Thread

# ---------------------------------------------------------------------------
# Master Processor Class
# ---------------------------------------------------------------------------

class Processor(Thread):
    # init method
    def __init__(self, database):
        # initializes the communication receiver module
        Thread.__init__(self)
        self.node = {'ID': Settings.SELF_ID, 'IP': Settings.SELF_IP, 'PORT': Settings.SELF_PORT}
        self.initial_node = {}
        self.master = {}
        self.database = database
        self.neighbor = Settings.NEIGHBOR
        self.is_participant = False
        self.is_master = False
    
    # send method
    def send(self, object, destiny_ip, destiny_port):
        # sends a object to a destinatary
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        success = False
        try:
            sock.connect((destiny_ip, destiny_port))
            sock.sendall(bytes(str(object), encoding="utf-8"))
            success = True
        except:
            success = False
        finally:
            sock.close()
        return success

    # start_sync method
    def start_sync(self):
        # starts a syncronization with the other nodes
        print('Start Syncing')
        package = {
            'TYPE': 'SYNCRONIZE',
            'MESSAGE': self.initial_node,
        }
        destiny_ip = self.neighbor['IP']
        destiny_port = self.neighbor['PORT']
        print('Try Syncing')
        while(True):
            self.send(package, destiny_ip, destiny_port)
            response = self.database.getJson()
            if response != 'NULL':
                if response['TYPE'] == 'SYNCRONIZE' and response['MESSAGE'] == self.initial_node:
                    break
        print('Sync Sucess! Running Election')
        self.start_election()

    # start_election method
    def start_election(self):
        # start a election with the other nodes
        package = {
            'TYPE': 'ELECTION_START',
            'MESSAGE': self.node,  
        }
        self.is_participant = True
        destiny_ip = self.neighbor['IP']
        destiny_port = self.neighbor['PORT']
        self.send(package, destiny_ip, destiny_port)
        while(True):
            response = self.database.getJson()
            if response != 'NULL':
                node = response['MESSAGE']
                if response['TYPE'] == 'ELECTION_START':
                    self.master = node
                    break
        print('Sync Sucess! Ending Election')
        self.end_election()
    
    # end_election method
    def end_election(self):
        # define a new master to all the nodes
        package = {
            'TYPE': 'ELECTION_END',
            'MESSAGE': self.master,  
        }
        destiny_ip = self.neighbor['IP']
        destiny_port = self.neighbor['PORT']
        self.send(package, destiny_ip, destiny_port)
        while(True):
            response = self.database.getJson()
            if response != 'NULL':
                node = response['MESSAGE']
                if response['TYPE'] == 'ELECTION_END':
                    self.is_participant = False
                    break
        print('Election Sucess! Running App')

    # consume_sync method
    def consume_sync(self):
        # consume a syncronization request
        count = 0
        while(True):
            json = self.database.getJson()
            if json != 'NULL':
                count = 0
                if json['TYPE'] == 'SYNCRONIZE':
                    self.initial_node = json['MESSAGE']
                    destiny_ip = self.neighbor['IP']
                    destiny_port = self.neighbor['PORT']
                    send = self.send(json, destiny_ip, destiny_port)
                    if send == False:
                        self.neighbor = self.initial_node
                        destiny_ip = self.neighbor['IP']
                        destiny_port = self.neighbor['PORT']
                        send = self.send(json, destiny_ip, destiny_port)
                    print('Node Sincronized!')
                    break
            if count > 5:
                break
            count += 1
        if count > 5:
            self.start_sync()
        else:
            self.consume_election()

    # consume_election method
    def consume_election(self):
        # consume a election request
        while(True):
            json = self.database.getJson()
            if json != 'NULL':
                if json['TYPE'] == 'ELECTION_START':
                    self.is_participant = True
                    participant = json['MESSAGE']
                    if participant['ID'] < self.master['ID']:
                        json['MESSAGE'] = self.master
                    destiny_ip = self.neighbor['IP']
                    destiny_port = self.neighbor['PORT']
                    self.send(json, destiny_ip, destiny_port)
                    print('Node Voted')
                    break
        self.consume_decision()

    # consume_decision method
    def consume_decision(self):
        # sets a new master to the node 
        while(True):
            json = self.database.getJson()
            if json != 'NULL':
                if json['TYPE'] == 'ELECTION_END':
                    self.is_participant = False
                    self.master = json['MESSAGE']
                    if self.master == self.node:
                        self.is_master = True
                    destiny_ip = self.neighbor['IP']
                    destiny_port = self.neighbor['PORT']
                    self.send(json, destiny_ip, destiny_port)
                    print('Election Success!')
                    print('Node Updated')
                    break

    # dispatcher method
    def dispatcher(self):
        # try an connection with the master, if it fails restarts the thread
        package = {
            'TYPE': 'COMMUNICATION',
            'MESSAGE': 'REQUEST_CONNECTION',
            'SENDER_IP': self.node['IP'],
            'SENDER_PORT': self.node['PORT'], 
        }
        destiny_ip = self.master['IP']
        destiny_port = self.master['PORT']
        while(True):
            send = self.send(package, destiny_ip, destiny_port)
            count = 0
            while(True):
                time.sleep(1)
                json = self.database.getJson()
                if json != 'NULL':
                    count = 0
                    if json['TYPE'] == 'COMMUNICATION' and json['MESSAGE'] == 'CONNECTION_OK':
                        print('Connection OK')
                        send = True
                        break
                count += 1
                if count > 5:
                    send = False
                    break
            if send == False:
                self.database.clearList()
                print('Starting a new Election')
                break
            
    # master_dispatcher method
    def master_dispatcher(self):
        # make the thread act as master
        package = {
            'TYPE': 'COMMUNICATION',
            'MESSAGE': 'CONNECTION_OK',
            'SENDER_IP': self.node['IP'],
            'SENDER_PORT': self.node['PORT'], 
        }
        while(True):
            json = self.database.getJson()
            if json != 'NULL':
                if json['TYPE'] == 'COMMUNICATION' and json['MESSAGE'] == 'REQUEST_CONNECTION':
                    response = 'Sender: '
                    response += str(json['SENDER_IP'])
                    response += ':' + str(json['SENDER_PORT'])
                    response += ' Requested Connection'
                    print(response)
                    self.send(package, json['SENDER_IP'], json['SENDER_PORT'])

    # run method
    def run(self):
        # start the Processor Core thread
        print("Core Actived")
        while(True):
            time.sleep(Settings.SELF_ID)
            self.initial_node = self.node
            self.master = self.node
            self.consume_sync()
            if self.is_master:
                print('Master')
                self.master_dispatcher()
            else:
                print('Client')
                time.sleep(3)
                self.dispatcher()