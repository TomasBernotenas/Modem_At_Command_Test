import time
import paramiko

#SSH connection module

class ssh_con:

    __shell=None
    __client_pre=None
    __device=None
    __passed=0
    __failed=0
    __Outstring=""
    __list=[]

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

    ## Opens ssh shell

    def ssh(self,args):

        try:
            __client_pre = paramiko.SSHClient()
            __client_pre.load_system_host_keys()
            __client_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __client_pre.connect(args.a,args.p,args.ln,args.lp,look_for_keys=False, allow_agent=False)
            self.__shell=__client_pre.invoke_shell()
        except Exception as e:
            print(e)

    ## Closes ssh connections

    def close_connections(self):
        if self.__shell:
            self.__shell.close() 
        if self.__client_pre:
            self.__shell.close()         

    ## Prints output to terminal

    def term_print(self,device,size):
        CRED = '\033[91m'
        CGREEN  = '\33[32m'
        CEND = '\033[0m'
        back = "\033[F"

        print("Device: "+ self.__device + "                 \r")
        print(device["command"] + ": Running                   \r" )
        print("Command count: " + str(size) + "\r")
        print(CGREEN+"Passed: "+CEND + str(self.__passed) + CRED +"  Failed: " + CEND + str(self.__failed)+ (back*4) +"\r")
            
        if size == self.__passed+self.__failed:
            print("\n\n\n")         

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
                self.__shell.send(bytes([26]))
                self.read_out()

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
    
    def commands(self,device,args):
        try:
            self.ssh(args)
            self.ssh_start(device["device"])

            size=len(device["commands"])
            self.__device=device["device"]
            mod_inf= self.modem_inf()

            for com in device["commands"]:
                self.term_print(com,size)
                com=self.user_commands(com) 
                self.term_print(com,size)

        except Exception as e:
            print(e)
        finally:
            self.gsmd_start()
            self.close_connections() 

        return device , mod_inf

    