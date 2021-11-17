import time


class data_collect:


    __shell=None
    __passed=0
    __failed=0
    __Outstring=None
    __list=[]

    def __load_print(self):
        try:
            terminal_print = __import__('modules.print_terminal',fromlist=["modules"])
            return terminal_print.print_terminal()
        except Exception as e:
            print(e)
            return False

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
            if command["expectedO"] in line: 
                command["res"]="Passed"
                command["res_param"]=self.__list[1:]
                sk+=1
                self.__passed+=1

        if sk==0:
            command["res"]="Failed"
            command["res_param"]=self.__list[1:]
            self.__failed+=1 

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

    def commands(self,device,shell):
        try:
            self.__shell=shell
            print_terminal=self.__load_print()

            size=len(device["commands"])
            deviceName=device["device"]
            modem_inf=self.modem_inf()

            for com in device["commands"]:
                print_terminal.term_print(com,size,deviceName,self.__passed,self.__failed)
                com=self.user_commands(com) 
                print_terminal.term_print(com,size,deviceName,self.__passed,self.__failed)

        except Exception as e:
            print(e)
        finally:
            self.close_connections() 

        return device , modem_inf[:3]