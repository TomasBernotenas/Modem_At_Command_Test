import sys
import signal
from argparse import ArgumentParser

from modules.configuration import config as configuration 
from modules.csv_mod import csv_mod as csv_mod
import modules.data_collect as data_collect

# Main module which controls the flow 

def signal_handler(sig, frame):
    print('\n\n\n\nYou pressed Ctrl+C!')
    sys.exit(0)

## Dynamically loads module from module folder

def __load_data_collect(device):
    try:
        connection_module = __import__('modules.{type}_con'.format(type=device["con_type"]),fromlist=["modules"])
        connection_atr = getattr(connection_module,'{type}_con'.format(type=device["con_type"]))
        connection_class= connection_atr()
        return connection_class
    except Exception as e:
        print(e)
        exit()

## Main function that controls the flow

def main(args):
    try:
        signal.signal(signal.SIGINT, signal_handler)
        device= configuration.getDevice(args.d)
        connection_class=__load_data_collect(device)
        if connection_class:
            try:
                connection_class.connectionPort(args)
                data=data_collect.data_collect(device,connection_class)
                res,mod_inf = data.commands() 
                csv_mod.print_csv(res,mod_inf)
            except:
                raise
            finally:
                connection_class.close_connections()

    except Exception as e:
        print(e)
        exit()
        
    
## Processes user arguments and calls main function 

def argument_parser():
    parser = ArgumentParser(description='Connection parameters')
    parser.add_argument('-d', help= "Device name")#device name
    parser.add_argument('-a', help= "Device address or port")#address
    parser.add_argument('-cp',default=22, help= "Connection port")#port
    parser.add_argument('-u', help= "Login name")#login name
    parser.add_argument('-p', help= "Login password")#login password
    args = parser.parse_args()
    return args


if __name__ == '__main__': 
    args=argument_parser()
    main(args)