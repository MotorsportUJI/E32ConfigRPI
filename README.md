# E32ConfigRPI
Config your EBYTE E32 LoRa module with a raspberry pi  
Connections:  
M0 --> 3.3v  
M1 --> 3.3v  
Rx --> gpio14(Txd)  
Tx --> gpio15(Rxd)  
AUX --> disconnected  
Vcc --> 3.3  
Gnd --> Gnd  
Remember to set up the serial port so it is not being used by the system:  
The primary uart https://www.raspberrypi.org/documentation/configuration/uart.md

# Usage
Execute main.py to execute the program, SerialBin.py is a helper script for sending raw commands to the serial device,
to change the serial device modify the variable serial_port
