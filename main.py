from tkinter import *
from constants import *
import struct


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


def read_operating_parameters():
    send_hex(bytes([0xc1]*3))
    x = get_hex(6)
    config.from_bytes(x)
    send_hex(config.to_bytes())


# btn read operating parameters
btn_op = Button(gui, text="Read Operating Parameters", command=read_operating_parameters)
btn_op.grid(row=2, column=0, sticky=E+W)


gui.mainloop()
