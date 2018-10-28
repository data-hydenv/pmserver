import serial, struct, platform


class Sensor:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud

        # last values
        self.pm10 = None
        self.pm25 = None

        # all measurements
        self.pm10list = []
        self.pm25list = []

        # try one measurement
        self.measure()

    @staticmethod
    def devices():
        # get the correct device path
        system = platform.system()
        if system.lower() == 'windows':
            devpath = 'COM%d'
        elif system.lower() == 'linux':
            devpath = '/dev/ttyUSB%d'
        else:
            print('System %s not supported yet' % system)
            devpath = '/dev/ttyUSB%d'

        # try all paths
        devices = []
        for i in range(100):
            try:
                serial.Serial(devpath % i, 9600)
                devices.append(devpath % i)
            except serial.SerialException:
                continue

        return devices

    @property
    def connected(self):
        s = self.get_com()
        return s is not None

    def get_com(self):
        try:
            ser = serial.Serial(self.port, self.baud)
            return ser
        except serial.SerialException:
            return None

    def measure(self):
        if not self.connected:
            print('Not connected')
            return None, None
        else:
            ser = self.get_com()

        # store the actual and last byte
        lastbyte, byte = b'\x00', 'b\x00'

        # read bytes until message start byte is found
        while True:
            lastbyte = byte
            byte = ser.read(1)

            # start byte
            if lastbyte == b'\xAA' and byte == b'\xC0':
                # read the whole 8 byte block
                block = ser.read(8)

                # it's little endian bytes: low < high
                msg = struct.unpack('<hhxxcc', block)

                # get the values
                self.pm25 = msg[0] / 10.0
                self.pm10 = msg[1] / 10.0

                # append
                self.pm10list.append(self.pm10)
                self.pm25list.append(self.pm25)

                return self.pm10, self.pm25

    def to_dict(self):
        return dict(
            connected=self.connected,
            baudrate=self.baud,
            port=self.port,
            last_values=dict(PM10=self.pm10, PM25=self.pm25)
        )
