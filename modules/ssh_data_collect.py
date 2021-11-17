import time

from modules.print_terminal import print_terminal
from modules.connection import ssh_con

# SSH data collection module

class data_collect:

    __shell=None
    __print=None
    __passed=0
    __failed=0
    __Outstring=""
    __list=[]


    ## Checks if the connected device is the sames as the user entered

    def device_check(self,dev_name):
        try:
            found=False
            self.__Outstring=self.__shell.exec_command("uci show system\n"," ")
            if dev_name.upper() in self.__Outstring[8]:
                found=True
            if not found:
                raise
            return found

        except Exception as e:
            print(e)
            print("Wrong device connected")
        

    ## SSH connection configuration for command execution

    def ssh_start(self,name):
        try:
            self.gsmd_stop()
                
            if self.device_check(name):
                self.__shell.exec_command("socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n"," ")
        except Exception as e:
            print(e)
            print("Failed to launch socat")

    ## Stops gsmd service

    def gsmd_stop(self):
        try:
            self.__shell.exec_command("/etc/init.d/gsmd stop\n"," ")  
        except Exception as e:
            print(e)
            print("Failed to stop gsmd")


    ## Starts gsmd service

    def gsmd_start(self):
        try:
            self.__shell.gsmd_start(bytes([26]),"/etc/init.d/gsmd start\n")                 
        except Exception as e:
            print(e)
            print("Failed to start gsmd")

    ## Adds non empty fileds to list and decode them

    def spc_del(self):
        try:
            self.__list=[]
            for item in self.__Outstring:
                if item!="":
                    self.__list.append(item) 
        except Exception as e:
            print(e)
            print("Failed to process output") 

    ## Checks the output and adds to command object 

    def res_check(self,command):
        try:
            sk=0

            for line in self.__list:
                if command["expectedO"] in line: 
                    command["res"]="Passed"
                    command["res_param"]=self.__list
                    sk+=1
                    self.__passed+=1

            if sk==0:
                command["res"]="Failed"
                command["res_param"]=self.__list
                self.__failed+=1 
        except Exception as e:
            print(e)
            print("Failed to write results")

    ## Modifies and executes commands

    def user_commands(self,device):
       
        try:

            self.__Outstring=self.__shell.exec_command((device["command"].replace("'",'"')+ '\r'),device["param"]) 
            time.sleep(0.2)
            self.spc_del()
            self.res_check(device)
            return device

        except Exception as e:
            print(e)
            print("Could not execute command")

        
    ## Gets modem information

    def modem_inf(self):
        try:
            self.__Outstring=self.__shell.exec_command("ATI\n"," ")
            self.spc_del()
            modem_inf=self.__list[:3]
            return modem_inf

        except Exception as e:
            print(e)
            print("Failed to get modem information")

    ## Main function that controls the flow of the module
    
    def commands(self,device,args):
        try:
            self.__shell=ssh_con()
            self.__print=print_terminal()
            self.__shell.connectionPort(args)

            self.ssh_start(device["device"])
            size=len(device["commands"])
            deviceName=device["device"]
            
            mod_inf= self.modem_inf()
            
            for com in device["commands"]:
                self.__print.term_print(com,size,deviceName,self.__passed,self.__failed)
                com=self.user_commands(com) 
                self.__print.term_print(com,size,deviceName,self.__passed,self.__failed)
            return device , mod_inf

        except Exception as e:
            print(e)
        finally:
            self.gsmd_start()
            self.__shell.close_connections()

        