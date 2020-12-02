from tkinter import *
from tkinter import ttk
from collections import OrderedDict
import serial
#
serial_port = "/dev/serial0"
ser = serial.Serial(serial_port)


# speed constants
# bits      76
uart_parity = OrderedDict([
    ("8N1" , "00"),  # default
     ("8O1" , "01"),
      ("8E1" , "10")])

#bits                 543
uart_baudrate = OrderedDict([
    ("1200" , "000"),
     ("2400" , "001"),
      ("4800" , "010"),
       ("9600" , "011"),# default
        ("19200" , "100"),
         ("38400" , "101"),
          ("57600" , "110"),
           ("115200" , "111")])

#bits               210
air_baudrate = OrderedDict([
    ("300" , "000"),
     ("1200" , "001"),
      ("2400" , "010"), # default
       ("4800" , "011"),
        ("9600" , "100"),
         ("19200" , "101")])

# options constants
# bits                      7
transmission_type = OrderedDict([
    ("TRANSP" , "0"),
     ("FIXED" , "1")])    # default
# bits            6
resistence_type = OrderedDict([
    ("WITH" , "1"),  # default
                  ("WHITHOUT" , "0")])
#bits            543
wake_time = OrderedDict([
    ("250ms" , "000" ), # default
     ("500ms" , "001"),
      ("1000ms" , "010"),
       ("1250ms" , "100"),
        ("1750ms" , "101"),
         ("2000ms" , "111")])
#bits            2
fec_switch = OrderedDict([
    ("ON" , "1"),  # default
     ("OFF" , "0")])
#bits                   10
power = OrderedDict([
    ("30dbi" , "00"), # default
     ("27dbi" , "01"),
      ("24dbi" , "10"),
       ("21dbi" , "11")])

def send_hex(h):
    ser.write(h)
    print("Sending to uart: ", end="")
    for i in h:
        print("{:02X}".format(i), end=" ")
    print("")


"""def get_hex(l):
    while True:
        x = ser.read(l)
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
            print("Invalid Input!")"""
def get_hex(l):
    x = ser.read(l)
    print("Receiving from uart: ", end="")
    for i in x:
        print("{:02X}".format(i), end=" ")
    print("")
    return x



class Speed:
    def __init__(self):
        self.air_baud_rate = air_baudrate["2400"]
        self.uart_baud_rate = uart_baudrate["9600"]
        self.uart_parity_bit = uart_parity["8N1"]

    def to_bytes(self):
        # al reves pues son little endian
        binary_string = self.uart_parity_bit + self.uart_baud_rate + self.air_baud_rate
        #binary_string = binary_string[::-1]
        b = bytes([int(binary_string, 2)])
        return b

    def from_bytes(self, bArray):
        bString = "{0:0>8b}".format(bArray)
        # bString = bString[::-1]
        self.uart_parity_bit = bString[0:2]
        self.uart_baud_rate = bString[2:5]
        self.air_baud_rate = bString[5:8]


class Option:
    def __init__(self):
        self.fixed_transmission_enbled = transmission_type["TRANSP"]
        self.io_resistences = resistence_type["WITH"]
        self.wake_time = wake_time["250ms"]
        self.fec_switch = fec_switch["ON"]
        self.transmission_power = power["30dbi"]

    def to_bytes(self):
        # al reves pues son little endian
        binary_string = self.fixed_transmission_enbled + self.io_resistences + self.wake_time + self.fec_switch + self.transmission_power
        # binary_string = binary_string[::-1]
        b = bytes([int(binary_string, 2)])
        return b

    def from_bytes(self, bArray):
        bString = "{0:0>8b}".format(bArray)
        # bString = bString[::-1]
        self.fixed_transmission_enbled = bString[0]
        self.io_resistences = bString[1]
        self.wake_time = bString[2:5]
        self.fec_switch = bString[5]
        self.transmission_power = bString[6:8]


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
        self.txt = StringVar()
        Frame.__init__(self, parent)

        vcmd = (parent.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.l = Label(self, text=text, justify=LEFT, width=10).grid(sticky = W, column=0, row=0)
        self.e =Entry(self, width=10, textvariable=self.txt, validate="key", validatecommand=vcmd)
        self.e.grid(sticky = E, column=1, row=0)

    def setText(self, txt):
        self.txt.set(txt)

    def getText(self):
        return self.e.get()

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        #print(value_if_allowed)
        if value_if_allowed[:2] == "0x":
            try:
                x = int(value_if_allowed[2:], 16)
                if x > 0xFF:
                    return False
            except ValueError:
                return False
            return True
        else:
            return False



class LabeledLabel(Frame):
    def __init__(self, parent, *args, **kargs):
        text = kargs.pop("text")
        self.text2 = StringVar()
        Frame.__init__(self, parent)
        self.l1 = Label(self, text=text, justify=LEFT).grid(sticky=W, column=0, row=0)
        self.l2 = Label(self, textvariable=self.text2).grid(sticky=E, column=1, row=0)

    def settext(self, s):
        self.text2.set(str(s))


class LabeledComboBox(Frame):
    def __init__(self, parent, *args, **kargs):
        text = kargs.pop("text")
        val = kargs.pop("values")
        Frame.__init__(self, parent)
        self.l = Label(self, text=text, justify=LEFT, width=15)
        self.l.grid(sticky = W, column=0, row=0)
        self.c =ttk.Combobox(self,values=val,state="readonly",width=15)
        self.c.grid(sticky = E, column=1, row=0)

    def current(self, cur):
        self.c.current(cur)

    def get_current(self):
        return self.c.get()


class Config_view(Frame):
    def __init__(self, parent, configOBJ, *args, **kwags):
        self.config = configOBJ
        Frame.__init__(self, parent)
        self.head = LabeledComboBox(self, text="HEAD: ", values=["0xC0"])
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
        self.uartBr = LabeledComboBox(self, text="uartBR: ", values=list(uart_baudrate))
        self.uartBr.grid(row=1, column=1)
        self.parity = LabeledComboBox(self, text="uartParity: ", values=list(uart_parity))
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

    def updateGUI(self):  # put info from config object to view
        self.head.current(0)  # CONSTANT

        addh = self.config.addh
        self.addh.setText("0x{:0>2X}".format(addh))

        addl = self.config.addl
        self.addl.setText("0x{:0>2X}".format(addl))

        chan = self.config.chan
        self.chan.setText("0x{:0>2X}".format(chan))

        # sped
        i = self.getIndexFromValue(air_baudrate, self.config.sped.air_baud_rate)
        self.airBr.current(i)

        i = self.getIndexFromValue(uart_baudrate, self.config.sped.uart_baud_rate)
        self.uartBr.current(i)

        i = self.getIndexFromValue(uart_parity, self.config.sped.uart_parity_bit)
        self.parity.current(i)

        #options
        i = self.getIndexFromValue(transmission_type, self.config.option.fixed_transmission_enbled)
        self.fixed_transmission_enbled.current(i)

        i = self.getIndexFromValue(resistence_type, self.config.option.io_resistences)
        self.io_resistences.current(i)

        i = self.getIndexFromValue(wake_time, self.config.option.wake_time)
        self.wake_time.current(i)

        i = self.getIndexFromValue(fec_switch, self.config.option.fec_switch)
        self.fec_switch.current(i)

        i = self.getIndexFromValue(power, self.config.option.transmission_power)
        self.transmission_power.current(i)

    def getIndexFromValue(self, oDict, val):
        r = 0
        for k, v in oDict.items():
            if v == val:
                return r
            r += 1
        return None

    def readGUI(self): # read info from view and put it in config object

        addh = self.addh.getText()[2:]
        self.config.addh = int(addh, 16)

        addl = self.addl.getText()[2:]
        self.config.addl = int(addl, 16)

        chan = self.chan.getText()[2:]
        self.config.chan = int(chan, 16)

        # Speed
        i = self.airBr.get_current()
        self.config.sped.air_baud_rate = air_baudrate[i]

        i = self.uartBr.get_current()
        self.config.sped.uart_baud_rate = uart_baudrate[i]

        i = self.parity.get_current()
        self.config.sped.uart_parity_bit = uart_parity[i]

        # Options
        i = self.fixed_transmission_enbled.get_current()
        self.config.option.fixed_transmission_enbled = transmission_type[i]

        i = self.io_resistences.get_current()
        self.config.option.io_resistences = resistence_type[i]

        i = self.wake_time.get_current()
        self.config.option.wake_time = wake_time[i]

        i = self.fec_switch.get_current()
        self.config.option.fec_switch = fec_switch[i]

        i = self.transmission_power.get_current()
        self.config.option.transmission_power = power[i]


    def SendData(self):
        self.readGUI()
        x = self.config.to_bytes()
        send_hex(x)








# config the window
gui = Tk()
gui.title("Config EBYTE E32 LoRa")
gui.geometry("700x350")

config = Configuration()

# reset command
def reset_command():
    send_hex(bytes([0xc4]*3))


# btn reset command
btn_rst = Button(gui, text="Reset module", command=reset_command)
btn_rst.grid(row=0, column=0, sticky=E+W)


def read_version_command():
    send_hex(bytes([0xc3]*3))
    x = get_hex(4)
    r = [int(i) for i in x]

    freq = r[1]
    if freq == 0x32:
        freq_txt = "433 Mhz"
    elif freq == 0x38:
        freq_txt = "470 Mhz"
    elif freq == 0x45:
        freq_txt = "868 Mhz"
    elif freq == 0x44:
        freq_txt = "915 Mhz"
    elif freq == 0x46:
        freq_txt = "170 Mhz"
    else:
        freq_txt = hex(freq)

    version_number = r[2]
    module_freatures = r[3]
    txt = "{}, version:{}, freatures: {}".format(freq_txt, hex(version_number), hex(module_freatures))
    vsnTXT.settext(txt)


# display version number
vsnTXT = LabeledLabel(gui, text="Freq:")
vsnTXT.grid(row=1, column=1, sticky=E+W)


# btn read version number
btn_vn = Button(gui, text="Read version number", command=read_version_command)
btn_vn.grid(row=1, column=0, sticky=E+W)


vGUI = Config_view(gui, config)
vGUI.grid(row=3, column=0, sticky=E+W, columnspan=5)

# btn read operating parameters
btn_op = Button(gui, text="Read Operating Parameters", command=vGUI.ReadData)
btn_op.grid(row=2, column=0, sticky=E+W)

# btn send operating parameters

btn_snd = Button(gui, text="Send Operation Parameters", command=vGUI.SendData)
btn_snd.grid(row=4, column=0, sticky=E+W)


gui.mainloop()
