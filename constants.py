# ALL

# speed constants
# bits      76
UART_8N1 = "00"  # default
UART_8O1 = "01"
UART_8E1 = "10"
#bits                 543
UART_BAUDRATE_1200 = "000"
UART_BAUDRATE_2400 = "001"
UART_BAUDRATE_4800 = "010"
UART_BAUDRATE_9600 = "011"  # default
UART_BAUDRATE_19200 = "100"
UART_BAUDRATE_38400 = "101"
UART_BAUDRATE_57600 = "110"
UART_BAUDRATE_115200 = "111"

#bits               210
AIR_BAUDRATE_300 = "000"
AIR_BAUDRATE_1200 = "001"
AIR_BAUDRATE_2400 = "010"  # default
AIR_BAUDRATE_4800 = "011"
AIR_BAUDRATE_9600 = "100"
AIR_BAUDRATE_19200 = "101"

# options constants
# bits                      7
TRANSPARENT_TRANSMISSION = "0"
FIXED_TRANSMISSION = "1"    # default
# bits            6
IO_RESISTENCES = "1"  # default
IO_WITHOUT_RESISTENCES = "0"
#bits            543
WAKE_TIME_250 = "000"  # default
WAKE_TIME_500 = "001"
WAKE_TIME_1000 = "010"
WAKE_TIME_1250 = "100"
WAKE_TIME_1750 = "101"
WAKE_TIME_2000 = "111"
#bits            2
FEC_SWITCH_ON = "1"  # default
FEC_SWITCH_OFF = "0"
#bits                   10
TRANSMISION_POWER_30 = "00"  # default
TRANSMISION_POWER_27 = "01"
TRANSMISION_POWER_24 = "10"
TRANSMISION_POWER_21 = "11"


class Speed:
    def __init__(self):
        self.air_baud_rate = AIR_BAUDRATE_2400
        self.uart_baud_rate = UART_BAUDRATE_9600
        self.uart_parity_bit = UART_8N1

    def to_bytes(self):
        # al reves pues son little endian
        binary_string = self.air_baud_rate + self.uart_baud_rate + self.uart_parity_bit
        binary_string = binary_string[::-1]
        b = bytes([int(binary_string, 2)])
        return b

    def from_bytes(self, bArray):
        bString = "{0:0>8b}".format(bArray)
        bString = bString[::-1]
        self.air_baud_rate = bString[0:3]
        self.uart_baud_rate = bString[3:6]
        self.uart_parity_bit = bString[6:8]



class Option:
    def __init__(self):
        self.fixed_transmission_enbled = TRANSPARENT_TRANSMISSION
        self.io_resistences = IO_RESISTENCES
        self.wake_time = WAKE_TIME_250
        self.fec_switch = FEC_SWITCH_ON
        self.transmission_power = TRANSMISION_POWER_30

    def to_bytes(self):
        # al reves pues son little endian
        binary_string = self.transmission_power + self.fec_switch + self.wake_time + self.io_resistences + self.fixed_transmission_enbled
        binary_string = binary_string[::-1]
        b = bytes([int(binary_string, 2)])
        return b

    def from_bytes(self, bArray):
        bString = "{0:0>8b}".format(bArray)
        bString = bString[::-1]
        self.transmission_power = bString[0:2]
        self.fec_switch = bString[2]
        self.wake_time = bString[3:6]
        self.io_resistences = bString[6]
        self.fixed_transmission_enbled = bString[7]


class Configuration:
    def __init__(self):
        self.head = 0xC0
        self.addh = 0x00
        self.addl = 0x00

        self.sped = Speed()
        self.chan = 0x17  # entre 0 y 1f
        self.option = Option()

    def to_bytes(self):
        bArray = bytearray([self.head, self.addh, self.addl, self.sped.to_bytes()[0], self.chan, self.option.to_bytes()[0]])
        return bArray

    def from_bytes(self, bArray):
        self.head = int(bArray[0])
        self.addh = int(bArray[1])
        self.addl = int(bArray[2])
        self.sped.from_bytes(bArray[3])
        self.chan = int(bArray[4])
        self.option.from_bytes(bArray[5])


