import serial

class UartComm():

    def __init__(self, device='/dev/ttyUSB0', baudrate=115200):
        self.dev = device
        self.baud = baudrate
        self.conn = None

    def connect(self):
        self.conn = serial.Serial(self.dev,self.baud)
        self.conn.close()
        self.conn.open()

    def close(self):
        self.conn.close()
        self.conn = None

    def isOpen(self):
        return (self.conn != None)


    def read(self, count):
        if self.isOpen():
            return self.conn.read(count)

    def write(self, data):
        if self.isOpen():
            return self.conn.write(data)


    def flush(self):
        if self.isOpen():
            self.conn.flush()


