import argparse

import shared

from connection import connection

# Main module which controls the flow 

def main(args):
    
        device= shared.getDevice(args)
        inst=connection.connect(device)
        res, mod_inf= inst.commands(device,args) 
        shared.print_tocsv(res,mod_inf)
    
## Processes user arguments and calls main function 

if __name__=="__main__": 
    parser = argparse.ArgumentParser(description='Connection parameters')
    parser.add_argument('-n', help= "Device name")#device name
    parser.add_argument('-a', help= "Device address or port")#address
    parser.add_argument('-p',default=22, help= "Connection port")#port
    parser.add_argument('-ln', help= "Login name")#login name
    parser.add_argument('-lp', help= "Login password")#login password
    args = parser.parse_args()
    main(args)