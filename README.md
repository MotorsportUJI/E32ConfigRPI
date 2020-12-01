# E32ConfigRPI
Config your EBYTE E32 LoRa module with a raspberry pi
\newline
Connections:
\newline
M0 --> 3.3v
\newline
M1 --> 3.3v
\newline
Rx --> gpio14(Txd)
\newline
Tx --> gpio15(Rxd)
\newline
AUX --> disconnected
\newline
Vcc --> 3.3
\newline
Gnd --> Gnd
\newline

Remember to set up the serial port so it is not being used by the system: The primary uart
https://www.raspberrypi.org/documentation/configuration/uart.md
