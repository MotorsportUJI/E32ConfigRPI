import serial
import threading
import time


class Fore:
    MAGENTA = "\033[35m"
    red = "\033[31m"
    reset = "\033[m"


class Receive(threading.Thread):
    def __init__(self, ser):
        super().__init__()
        self.serial = ser
        self.cont = True

    def stop(self):
        self.cont = False

    def run(self):
        actual_ms = int(time.time() * 1000)
        received = True
        while self.cont:

            if self.serial.in_waiting > 0:
                byte_received = bytes(self.serial.read())
                x = int.from_bytes(byte_received, byteorder="big")
                print(Fore.MAGENTA + "{:02X}".format(x) + Fore.reset, end=" ", flush=True)
                received = True
            elif (int(time.time() * 1000) - actual_ms) > 1000 and received:
                print("")
                received = False


class Send(threading.Thread):
    def __init__(self, ser):
        super().__init__()
        self.serial = ser
        self.cont = True

    def stop(self):
        self.cont = False

    def run(self):
        while self.cont:
            numbers = input("")
            number_list = numbers.split(" ")
            ind = []
            try:
                for n in number_list:
                    if len(n) != 2:
                        raise ValueError
                    n = int(n, 16)
                    ind.append(n)
                ind_b = bytearray(ind)
                self.serial.write(ind_b)
            except ValueError:
                print(Fore.red + "Invalid input!" + Fore.reset)


s = serial.Serial("/dev/serial0")
s.baudrate = 9600
# s.timeout = 1

send_thread = Send(s)
receive_thread = Receive(s)

send_thread.start()
receive_thread.start()
try:
    send_thread.join()
    receive_thread.join()

except KeyboardInterrupt:
    send_thread.stop()
    receive_thread.stop()
