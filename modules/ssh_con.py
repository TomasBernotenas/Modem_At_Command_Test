from paramiko import SSHClient,AutoAddPolicy
from time import sleep



# Connection module

class ssh_con:
    
    __shell=None
    __client_pre=None
    __Outstring=""

    ## Opens ssh shell

    def connectionPort(self,args):

        try:
            self.__client_pre = SSHClient()
            self.__client_pre.load_system_host_keys()
            self.__client_pre.set_missing_host_key_policy(AutoAddPolicy())
            self.__client_pre.connect(args.a,args.cp,args.u,args.p,look_for_keys=False, allow_agent=False, timeout=40)
            self.__shell=self.__client_pre.invoke_shell()
            return self.__shell

        except Exception as e:
            print(e)
            print("Failed to connect to SSH client")

    ## Starts gsmd service

    def gsmd_start(self, command, param):
        self.__shell.send(command) 
        sleep(0.2)
        self.__shell.send(param + "\r")
        sleep(0.2)

    ## Stops gsmd service

    def gsmd_stop(self, command):
        self.__shell.send(command) 
        sleep(0.2)


    ## Executes command and reads output

    def exec_command(self, command, param):
        try:
            self.__shell.send(command+"\r") 
            sleep(0.2)
            self.__shell.send(param+"\r")
            sleep(0.2)
            self.read_out()

            if "> " in self.__Outstring:
                self.__shell.send(bytes([26]))
                sleep(0.5)
                self.read_out()

            return self.__Outstring

        except Exception as e:
            print(e)
            print("Failed to execute command")

    ## Reads output of shell

    def read_out(self):
        try:
            while not self.__shell.recv_ready(): 
                sleep(0.5)
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
        print("shell closed")
        