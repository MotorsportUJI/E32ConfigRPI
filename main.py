from tkinter import *
from constants import *
import struct






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
