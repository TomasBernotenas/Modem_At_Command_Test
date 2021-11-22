from modules.print_terminal import print_terminal

# Serial data collection module

class data_collect:

    __shell=None
    __print=None
    __device=None
    __passed=0
    __failed=0
    __Outstring=None
    __list=[]

    def __init__(self,device,shell) :
        self.__device = device
        self.__shell = shell



    ## Checks if the connected device is the sames as the user entered
    ### ubus sys ?

    def device_name_check(self,dev_name):
        try:
            found=False
            self.__shell.read_output()
            self.__Outstring=self.__shell.exec_command("uci show system\n"," ")
            
            if dev_name.upper() in str(self.__Outstring):
                found=True
            if not found:
                raise
            return found

        except Exception as e:
            print("Wrong device connected")
            exit()
     
    ## SSH connection configuration for command execution

    def ssh_start(self):
        try:
            if self.__device["con_type"]=="ssh":
                self.gsmd_stop()
                    
                if self.device_name_check(self.__device["device"]):
                    self.__shell.exec_command("socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\n"," ")
            return
        except Exception as e:
            print("Failed to launch socat")
            exit()

    ## Stops gsmd service

    def gsmd_stop(self):
        try:
            self.__shell.gsmd_stop("/etc/init.d/gsmd stop\n")  
        except Exception as e:
            print("Failed to stop gsmd")
            exit()

    ## Starts gsmd service

    def gsmd_start(self):
        try:
            if self.__device["con_type"]=="ssh":
                self.__shell.gsmd_start(bytes([26]),"/etc/init.d/gsmd start\n") 
            return                
        except Exception as e:
            print("Failed to start gsmd")
            exit()

    ## Modifies and executes commands

    def user_commands(self,device):
        
        try:
            self.__Outstring=self.__shell.exec_command(device["command"].replace("'",'"'), device["param"])
            self.spc_del()
            self.command_res_check(device)
            return device

        except Exception as e:
            print(e)
            print("Could not execute command")
            exit()

    ## Checks the output and adds to command object 

    def command_res_check(self,command):
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
            print("Failed to write results")
            exit()

    ## Adds non empty fileds to list and decode them

    def spc_del(self):
        self.__list=[]
        try:
            if self.__device["con_type"]=="serial":
                for item in self.__Outstring:
                    if item.decode().replace("\r\n","")!="":
                        self.__list.append(item.decode('utf-8').replace("\r\n",""))
            elif self.__device["con_type"]=="ssh":
                for item in self.__Outstring:
                    if item!="":
                        self.__list.append(item) 
            return 
        except Exception as e:
            print("Failed to process output")
            exit()
    
    ## Gets modem info

    def get_modem_info(self):
        try:
            self.__Outstring=self.__shell.exec_command("ATI\n", " ")
            self.spc_del()
            if self.__device["con_type"]=="ssh":
                modem_inf=self.__list[:3]
            elif self.__device["con_type"]=="serial":
                modem_inf=self.__list[1:]
            return modem_inf

        except Exception as e:
            print("Failed to get modem information") 
            exit()

    ## Main function that controls the flow of the module

    def module_control_commands(self):
        try:
            self.__print=print_terminal()

            self.ssh_start()

            size=len(self.__device["commands"])
            deviceName=self.__device["device"]
            
            mod_inf= self.get_modem_info()
            
            for com in self.__device["commands"]:
                self.__print.term_print(com,size,deviceName,self.__passed,self.__failed)
                com=self.user_commands(com) 
                self.__print.term_print(com,size,deviceName,self.__passed,self.__failed)
            return self.__device , mod_inf

        except Exception as e:
            print(e)
            exit()

        finally:
            if self.__device["con_type"]=="ssh":
                self.gsmd_start()

        