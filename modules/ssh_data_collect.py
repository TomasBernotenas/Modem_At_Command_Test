import time

class data_collect:

    __shell=None
    __client_pre=None
    __passed=0
    __failed=0
    __Outstring=""
    __list=[]

    def __load_print(self):
        try:
            terminal_print = __import__('modules.print_terminal',fromlist=["modules"])
            return terminal_print.print_terminal()
        except Exception as e:
            print(e)
            return False

    ## Checks if the connected device is the sames as the user entered

    def device_check(self,dev_name):
        try:
            found=False
            self.read_out()
            self.__shell.send("uci show system\n")
            time.sleep(0.2)
            self.read_out()
            if dev_name.upper() in self.__Outstring[8]:
                found=True
            if not found:
                raise
        except:
            print("Wrong device connected")
        return found

    ## SSH connection configuration for command execution

    def ssh_start(self,name):

        self.gsmd_stop()
        time.sleep(0.2)
            
        if self.device_check(name):
            time.sleep(0.2)
            self.__shell.send("socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n")
            time.sleep(0.2)
            self.read_out()

    ## Stops gsmd service

    def gsmd_stop(self):
        self.__shell.send("/etc/init.d/gsmd stop\n")    

    ## Starts gsmd service

    def gsmd_start(self):
        self.__shell.send(bytes([26]))
        time.sleep(1)
        self.__shell.send("/etc/init.d/gsmd start\n")    

    

    ## Closes ssh connections

    def close_connections(self):
        if self.__shell:
            self.__shell.close() 
        if self.__client_pre:
            self.__shell.close()                  

    ## Reads output of shell

    def read_out(self):
        while not self.__shell.recv_ready(): 
            time.sleep(0.5)
        self.__Outstring = self.__shell.recv(9999).decode("ascii").splitlines()

    ## Adds non empty fileds to list and decode them

    def spc_del(self):
        self.__list=[]
        for item in self.__Outstring:
            if item!="":
                self.__list.append(item)  

    ## Checks the output and adds to command object 

    def res_check(self,command):

        sk=0

        for line in self.__list:
            if "OK" in line: 
                command["res"]="Passed"
                command["res_param"]=self.__list
                sk+=1
                self.__passed+=1

        if sk==0:
            command["res"]="Failed"
            command["res_param"]=self.__list
            self.__failed+=1 

    ## Modifies and executes commands

    def user_commands(self,device):
       
        try:

            self.__shell.send(device["command"].replace("'",'"') + '\r') 
            self.__shell.send((device["param"]) + "\r")
            self.read_out()
            time.sleep(1)

            if "> " in self.__Outstring:
                time.sleep(1)
                self.__shell.send(bytes([26]))
                self.read_out()

            time.sleep(0.5)
            self.spc_del()
            self.res_check(device)

        except Exception as e:
            print(e)

        return device

    ## Gets modem information

    def modem_inf(self):
        self.__shell.send("ATI\n")
        time.sleep(0.2)
        self.read_out()
        time.sleep(0.2)
        self.spc_del()
        modem_inf=self.__list[:3]
        return modem_inf

    ## Main function that controls the flow of the module
    
    def commands(self,device,shell):
        try:
            self.__shell=shell
            self.ssh_start(device["device"])
            print_terminal=self.__load_print()

            size=len(device["commands"])
            deviceName=device["device"]
            mod_inf= self.modem_inf()

            for com in device["commands"]:
                print_terminal.term_print(com,size,deviceName,self.__passed,self.__failed)
                com=self.user_commands(com) 
                print_terminal.term_print(com,size,deviceName,self.__passed,self.__failed)

        except Exception as e:
            print(e)
        finally:
            self.gsmd_start()
            self.close_connections() 

        return device , mod_inf