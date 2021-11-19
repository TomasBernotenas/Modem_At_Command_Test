from serial import Serial,SerialException
from time import sleep

class serial_con:

    __shell=None

    
    ## Opens serial port and clears input buffer

    def connectionPort(self,args):
        try:
            self.__shell = Serial(args.a, timeout=5)
            self.__shell.reset_input_buffer()
            return self.__shell
  
        except SerialException:
            print("Device or resource busy")
        except FileNotFoundError:
            print("Port is not connected")
        except Exception as e:
            print(e)
            exit()


    ## Executes command and reads output

    def exec_command(self, command, param):
        try:
            self.__shell.write((command + '\r').encode()) 
            sleep(0.5)
            self.__shell.write(((param + "\r").encode()))
            self.__shell.write(bytes([26]))

            Outstring=self.__shell.readlines()
            return Outstring
        except Exception as e:
            print("\n\n\n\n"+str(e))
            exit()

    ## Closes serial port

    def close_connections(self):
        if self.__shell:
            self.__shell.close()

            