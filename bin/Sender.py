import socket
from threading import Thread

# ---------------------------------------------------------------------------
# Sender Class
# ---------------------------------------------------------------------------

class Sender(Thread):
    # init method
    def __init__(self, object, DESTINY_HOST, DESTINY_PORT):
        # initializes the sender
        Thread.__init__(self)
        self.object = str(object)
        self.DESTINY_HOST = DESTINY_HOST
        self.DESTINY_PORT = DESTINY_PORT

    # send method
    def send(self):
        # sends stored information to a defined destination
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.DESTINY_HOST, self.DESTINY_PORT))
            sock.sendall(bytes(self.object, encoding="utf-8"))
        finally:
            sock.close()

    # run method
    def run(self):
        # start the Sender thread
        self.send()