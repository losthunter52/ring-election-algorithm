PID = 1
SELF_IP = '192.168.3.12'
SELF_PORT = 61666
NEIGHBOR = {'IP': '192.168.3.12', 'PORT': 61666}
COMMUNICATION_TIMEOUT = 5

JSON_11 = {
    'TYPE': 'COMMUNICATION',
    'MESSAGE': 'REQUEST',
    'SENDER_IP': '192.168.3.12',
    'SENDER_PORT': 61665,    
}

JSON_12 = {
    'TYPE': 'COMMUNICATION',
    'MESSAGE': 'RESPONSE',
    'SENDER_IP': '192.168.3.12',
    'SENDER_PORT': 61666,    
}

JSON_21 = {
    'TYPE': 'ELECTION',
    'PID': 1,
    'MESSAGE': 'PARTICIPANT',
    'SENDER_IP': '192.168.3.12',
    'SENDER_PORT': 61665,    
}

JSON_22 = {
    'TYPE': 'ELECTION',
    'PID': 7,
    'MESSAGE': 'ELECTED',
    'MASTER_IP': '192.168.3.12',
    'MASTER_PORT': 61666,
    'SENDER_IP': '192.168.3.12',
    'SENDER_PORT': 61665,    
}