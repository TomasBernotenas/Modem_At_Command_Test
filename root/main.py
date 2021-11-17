import argparse
import sys


# Main module which controls the flow 

## Loads modules from module folder

def __load_module():
        try:
            sys.path.append("../")
            conf_module = __import__('modules.configuration',fromlist=["modules"])
            csv_module = __import__('modules.csv_mod',fromlist=["modules"])
            
            return conf_module.config(),csv_module
        except:
            return False

## Dynamically loads module from module folder

def __load_data_collect(device):
    try:
        data_module = __import__('modules.{type}_data_collect'.format(type=device["con_type"]),fromlist=["modules"])
        return data_module.data_collect()
    except Exception as e:
        print(e)
        return False


## Main function that controls the flow

def main(args):

        configuration, csv_mod = __load_module()      
        device= configuration.__getDevice__(args.n)
        dataCollect =__load_data_collect(device)
        res,mod_inf=dataCollect.commands(device,args) 
        csv_mod.print_tocsv(res,mod_inf)
    
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