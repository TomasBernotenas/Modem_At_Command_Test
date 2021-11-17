import time
import paramiko

#SSH connection module

class ssh_con:
    ## Opens ssh shell

    def connectionPort(self,args):

        try:
            __client_pre = paramiko.SSHClient()
            __client_pre.load_system_host_keys()
            __client_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __client_pre.connect(args.a,args.p,args.ln,args.lp,look_for_keys=False, allow_agent=False)
            __shell=__client_pre.invoke_shell()
        except Exception as e:
            print(e)
        return __shell


    