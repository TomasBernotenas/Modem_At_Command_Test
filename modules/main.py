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
    parser.add_argument('-n')#device name
    parser.add_argument('-a')#address
    parser.add_argument('-p',default=22)#port
    parser.add_argument('-ln')#login name
    parser.add_argument('-lp')#login password
    args = parser.parse_args()
    main(args)