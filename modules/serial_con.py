import serial
import time
from serial.serialutil import SerialException

# Serial connection module

class serial_con:

    __passed=0
    __failed=0
    __shell=None
    __device=None
    __Outstring=None
    __list=[]

    ## Opens serial port and clears input buffer

    def serial(self,args):
        try:
            self.__shell = serial.Serial(args.a, timeout=5)
            self.__shell.reset_input_buffer()
  
        except SerialException:
            print("Device or resource busy")
        except FileNotFoundError:
            print("Port is not connected")

    ## Closes serial port

    def close_connections(self):
        if self.__shell:
            self.__shell.close() 

    ## Modifies and executes commands

    def user_commands(self,device):
        
        try:

            self.__shell.write((device["command"].replace("'",'"') + '\r').encode())  
            time.sleep(0.5)
            self.__shell.write(((device["param"]) + "\r").encode())
            self.__shell.write(bytes([26]))
            self.__Outstring=self.__shell.readlines()
            self.spc_del()
            self.res_check(device)

        except Exception as e:
            print(e)    

        return device

    ## Checks the output and adds to command object 

    def res_check(self,command):

        sk=0

        for line in self.__list:
            if "OK" in line: 
                command["res"]="Passed"
                command["res_param"]=self.__list[1:]
                sk+=1
                self.__passed+=1

        if sk==0:
            command["res"]="Failed"
            command["res_param"]=self.__list[1:]
            self.__failed+=1 

    ## Prints output to terminal

    def term_print(self,device,size):
        CRED = '\033[91m'
        CGREEN  = '\33[32m'
        CEND = '\033[0m'
        back = "\033[F"

        print("Device: "+ self.__device + "         \r")
        print(device["command"] + ": Running             \r" )
        print("Command count: " + str(size) + "\r")
        print(CGREEN+"Passed: "+CEND + str(self.__passed) + CRED +"  Failed: " + CEND + str(self.__failed)+ (back*4) +"\r")
            
        if size == self.__passed+self.__failed:
            print("\n\n\n")

    ## Adds non empty fileds to list and decode them

    def spc_del(self):
        self.__list=[]
        for item in self.__Outstring:
            if item.decode().replace("\r\n","")!="":
                self.__list.append(item.decode('utf-8').replace("\r\n","")) 
    
    ## Gets modem info

    def modem_inf(self):
        self.__shell.write(("ATI\r").encode())
        self.__shell.write(bytes([26]))

        self.__Outstring=self.__shell.readlines()

        self.spc_del()
        self.__shell.reset_input_buffer()
        modem_inf=self.__list
        return modem_inf[1:]    

    ## Main function that controls the flow of the module

    def commands(self,device,args):
        try:
            self.serial(args)
            
            size=len(device["commands"])
            self.__device=device["device"]
            modem_inf=self.modem_inf()

            for com in device["commands"]:
                self.term_print(com,size)
                com=self.user_commands(com) 
                self.term_print(com,size)

        except Exception as e:
            print(e)
        finally:
            self.close_connections() 

        return device , modem_inf[:3]          



    