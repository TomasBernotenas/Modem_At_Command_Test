import paramiko
import serial
import time

from serial.serialutil import SerialException

# Connection module

class ssh_con:
    
    __shell=None
    __client_pre=None
    __Outstring=""

    ## Opens ssh shell

    def connectionPort(self,args):

        try:
            self.__client_pre = paramiko.SSHClient()
            self.__client_pre.load_system_host_keys()
            self.__client_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__client_pre.connect(args.a,args.p,args.ln,args.lp,look_for_keys=False, allow_agent=False)
            self.__shell=self.__client_pre.invoke_shell()

        except Exception as e:
            print(e)
            print("Failed to connect to SSH client")

    ## Starts gsmd service

    def gsmd_start(self, command, param):
        self.__shell.send(command) 
        time.sleep(0.2)
        self.__shell.send(param + "\r")

    ## Executes command and reads output

    def exec_command(self, command, param):
        try:
            self.__shell.send(command) 
            time.sleep(0.2)
            self.__shell.send(param + "\r")
            time.sleep(0.2)
            self.read_out()

            if "> " in self.__Outstring:
                self.__shell.send(bytes([26]))
                self.read_out()

            return self.__Outstring

        except Exception as e:
            print(e)
            print("Failed to execute command")

    ## Reads output of shell

    def read_out(self):
        try:
            while not self.__shell.recv_ready(): 
                time.sleep(0.5)
            self.__Outstring = self.__shell.recv(9999).decode("ascii").splitlines()
        except Exception as e:
            print(e)
            print("Failed to read output")
   
   
    ## Closes ssh connections

    def close_connections(self):
        if self.__shell:
            self.__shell.close() 
        if self.__client_pre:
            self.__client_pre.close()
        

class serial_con:

    __shell=None
    
    ## Opens serial port and clears input buffer

    def connectionPort(self,args):
        try:
            self.__shell = serial.Serial(args.a, timeout=5)
            self.__shell.reset_input_buffer()
  
        except SerialException:
            print("Device or resource busy")
        except FileNotFoundError:
            print("Port is not connected")

    ## Executes command and reads output

    def exec_command(self, args, command, param):
        try:
            self.connectionPort(args)
            self.__shell.write((command + '\r').encode()) 
            time.sleep(0.5)
            self.__shell.write(((param + "\r").encode()))
            self.__shell.write(bytes([26]))
            Outstring=self.__shell.readlines()
            self.close_connections()
            return Outstring
        except Exception as e:
            print(e)
            print("Failed to execute command")

    ## Closes serial port

    def close_connections(self):
        if self.__shell:
            self.__shell.close()