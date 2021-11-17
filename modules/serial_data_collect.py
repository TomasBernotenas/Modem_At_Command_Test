from modules.print_terminal import print_terminal
from modules.connection import serial_con

# Serial data collection module

class data_collect:

    __shell=None
    __print=None
    __args=None
    __passed=0
    __failed=0
    __Outstring=None
    __list=[]
 
    ## Modifies and executes commands

    def user_commands(self,device):
        
        try:
            self.__Outstring=self.__shell.exec_command(self.__args,device["command"].replace("'",'"'), device["param"])
            self.spc_del()
            self.res_check(device)
            return device

        except Exception as e:
            print(e)
            print("Could not execute command")

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

    ## Adds non empty fileds to list and decode them

    def spc_del(self):
        self.__list=[]
        try:
            for item in self.__Outstring:
                if item.decode().replace("\r\n","")!="":
                    self.__list.append(item.decode('utf-8').replace("\r\n","")) 
        except Exception as e:
            print(e)
            print("Failed to process output")
    
    ## Gets modem info

    def modem_inf(self):
        try:
            self.__Outstring=self.__shell.exec_command(self.__args,"ATI", " ")
            self.spc_del()
            modem_inf=self.__list
            return modem_inf[1:]

        except Exception as e:
            print(e)
            print("Failed to get modem information") 

    ## Main function that controls the flow of the module

    def commands(self,device, args):
        try:
            self.__args=args
            self.__shell=serial_con()
            self.__print=print_terminal()
            size=len(device["commands"])
            deviceName=device["device"]
            modem_inf=self.modem_inf()

            for com in device["commands"]:
                self.__print.term_print(com,size,deviceName,self.__passed,self.__failed)
                com=self.user_commands(com) 
                self.__print.term_print(com,size,deviceName,self.__passed,self.__failed)
            return device , modem_inf[:3]

        except Exception as e:
            print(e)

        