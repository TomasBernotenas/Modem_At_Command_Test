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

    ## Executes command and reads output

    def exec_command(self, command, param):
        try:
            self.__shell.write((command + '\r').encode()) 
            sleep(0.5)
            self.__shell.write(((param + "\r").encode()))
            self.__shell.write(bytes([26]))
            # rl = ReadLine(self.__shell)
            # while True:
            #     rl.readline()

            Outstring=self.__shell.readlines()
            return Outstring
        except Exception as e:
            print(e)
            print("Failed to execute command")

    ## Closes serial port

    def close_connections(self):
        if self.__shell:
            self.__shell.close()

                
# class ReadLine:
#     def __init__(self, s):
#         self.buf = bytearray()
#         self.s = s
    
#     def readline(self):
#         i = self.buf.find(b"\n")
#         if i >= 0:
#             r = self.buf[:i+1]
#             self.buf = self.buf[i+1:]
#             return r
#         while True:
#             i = max(1, min(2048, self.s.in_waiting))
#             data = self.s.read(i)
#             i = data.find(b"\n")
#             if i >= 0:
#                 r = self.buf + data[:i+1]
#                 self.buf[0:] = data[i+1:]
#                 return r
#             else:
#                 self.buf.extend(data)