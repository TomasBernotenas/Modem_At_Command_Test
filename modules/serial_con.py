import serial
import time
from serial.serialutil import SerialException

# Serial connection module

class serial_con:

    ## Opens serial port and clears input buffer

    def connectionPort(self,args):
        try:
            __shell = serial.Serial(args.a, timeout=5)
            __shell.reset_input_buffer()
            return __shell
  
        except SerialException:
            print("Device or resource busy")
        except FileNotFoundError:
            print("Port is not connected")

              



    