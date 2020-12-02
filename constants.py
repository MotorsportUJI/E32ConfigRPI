from tkinter import *
from tkinter import ttk
# ALL

# speed constants
# bits      76
uart_parity = {
"UART_8N1" : "00",  # default
"UART_8O1" : "01",
"UART_8E1" : "10"}

#bits                 543
uart_baudrate = {
"UART_BAUDRATE_1200" : "000",
"UART_BAUDRATE_2400" : "001",
"UART_BAUDRATE_4800" : "010",
"UART_BAUDRATE_9600" : "011"  ,# default
"UART_BAUDRATE_19200" : "100",
"UART_BAUDRATE_38400" : "101",
"UART_BAUDRATE_57600" : "110",
"UART_BAUDRATE_115200" : "111"}

#bits               210
air_baudrate = {
"AIR_BAUDRATE_300" : "000",
"AIR_BAUDRATE_1200" : "001",
"AIR_BAUDRATE_2400" : "010", # default
"AIR_BAUDRATE_4800" : "011",
"AIR_BAUDRATE_9600" : "100",
"AIR_BAUDRATE_19200" : "101"}

# options constants
# bits                      7
transmission_type = {
"TRANSPARENT_TRANSMISSION" : "0",
"FIXED_TRANSMISSION" : "1"}    # default
# bits            6
resistence_type = {
"IO_RESISTENCES" : "1",  # default
"IO_WITHOUT_RESISTENCES" : "0"}
#bits            543
wake_time = {
"WAKE_TIME_250" : "000" , # default
"WAKE_TIME_500" : "001",
"WAKE_TIME_1000" : "010",
"WAKE_TIME_1250" : "100",
"WAKE_TIME_1750" : "101",
"WAKE_TIME_2000" : "111"}
#bits            2
fec_switch = {
"FEC_SWITCH_ON" : "1",  # default
"FEC_SWITCH_OFF" : "0"}
#bits                   10
power = {
"TRANSMISION_POWER_30" : "00", # default
"TRANSMISION_POWER_27" : "01",
"TRANSMISION_POWER_24" : "10",
"TRANSMISION_POWER_21" : "11"}

def send_hex(h):
    print("Sending to uart: ", end="")
    for i in h:
        print("{:02X}".format(i), end=" ")
    print("")


def get_hex(l):
    while True:
        x = input("Getting data from uart: ")
        result = []
        try:
            for i in x.split():
                if len(i) != 2:
                    raise ValueError
                else:
                    n = int(i, 16)
                    result.append(n)
            result_b = bytearray(result)
            return result_b
        except ValueError:
            print("Invalid Input!")


class Speed:
    def __init__(self):
        self.air_baud_rate = air_baudrate["AIR_BAUDRATE_2400"]
        self.uart_baud_rate = uart_baudrate["UART_BAUDRATE_9600"]
        self.uart_parity_bit = uart_parity["UART_8N1"]

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
        self.fixed_transmission_enbled = transmission_type["TRANSPARENT_TRANSMISSION"]
        self.io_resistences = resistence_type["IO_RESISTENCES"]
        self.wake_time = wake_time["WAKE_TIME_250"]
        self.fec_switch = fec_switch["FEC_SWITCH_ON"]
        self.transmission_power = power["TRANSMISION_POWER_30"]

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


class LabeledEntry(Frame):
    def __init__(self, parent, *args, **kargs):
        text = kargs.pop("text")
        Frame.__init__(self, parent)
        self.l = Label(self, text=text, justify=LEFT).grid(sticky = W, column=0, row=0)
        self.e =Entry(self, *args, **kargs).grid(sticky = E, column=1, row=0)


class LabeledLabel(Frame):
    def __init__(self, parent, *args, **kargs):
        text = kargs.pop("text")
        self.text2 = StringVar()
        Frame.__init__(self, parent)
        self.l1 = Label(self, text=text, justify=LEFT).grid(sticky=W, column=0, row=0)
        self.l2 = Label(self, textvariable=self.text2,*args, **kargs).grid(sticky=E, column=1, row=0)

    def settext(self, s):
        self.text2.set(str(s))


class LabeledComboBox(Frame):
    def __init__(self, parent, *args, **kargs):
        text = kargs.pop("text")
        val = kargs.pop("values")
        Frame.__init__(self, parent)
        self.l = Label(self, text=text, justify=LEFT).grid(sticky = W, column=0, row=0)
        self.c =ttk.Combobox(self,values=val,state="readonly", *args, **kargs).grid(sticky = E, column=1, row=0)

class Config_view(Frame):
    def __init__(self, parent, configOBJ, *args, **kwags):
        self.config = configOBJ
        Frame.__init__(self, parent)
        self.head = LabeledComboBox(self, text="HEAD: ", values=["0xC0","0xC2"])
        #self.head.pack(side = LEFT)
        self.head.grid(row=0, column=0)

        self.addh = LabeledEntry(self, text="ADDH: ")
        #self.addh.pack(side = LEFT)
        self.addh.grid(row=0, column=1)

        self.addl = LabeledEntry(self, text="ADDL: ")
        #self.addl.pack(side = LEFT)
        self.addl.grid(row=0, column=2)
        # sped
        self.airBr = LabeledComboBox(self, text="AirBR: ", values=list(air_baudrate))
        self.airBr.grid(row=1, column=0)
        self.uartBr = LabeledComboBox(self, text="uartBR", values=list(uart_baudrate))
        self.uartBr.grid(row=1, column=1)
        self.parity = LabeledComboBox(self, text="uartParity", values=list(uart_parity))
        self.parity.grid(row=1, column=2)
        self.chan = LabeledEntry(self, text="CHAN: ")
        # self.chan.pack()
        self.chan.grid(row=2, column=0)

        # option
        self.transmission_power = LabeledComboBox(self, text="Tpower: ", values=list(power))
        self.transmission_power.grid(row=3, column=0)
        self.fec_switch = LabeledComboBox(self, text="Fec: ", values=list(fec_switch))
        self.fec_switch.grid(row=3,column=1)
        self.wake_time =LabeledComboBox(self, text="WakeT: ", values=list(wake_time))
        self.wake_time.grid(row=3, column=2)
        self.io_resistences = LabeledComboBox(self, text="Resistences: ", values=list(resistence_type))
        self.io_resistences.grid(row=4, column=0)
        self.fixed_transmission_enbled =LabeledComboBox(self, text = "TMode: ", values=list(transmission_type))
        self.fixed_transmission_enbled.grid(row=4,column=1)


    def ReadData(self):
        send_hex(bytes([0xc1] * 3))
        x = get_hex(6)
        self.config.from_bytes(x)
        self.updateGUI()

#    def writeGUI(self): # put info from config object to view


#    def readGUI(self): # read info from view and put it in config object

    def SendData(self):
        self.readGUI()
        x = self.config.to_bytes()
        send_hex(x)

