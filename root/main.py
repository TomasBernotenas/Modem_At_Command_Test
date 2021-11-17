import argparse
import sys




# Main module which controls the flow 
def __load_module():
        try:
            sys.path.append("../")
            conf_module = __import__('modules.configuration',fromlist=["modules"])
            con_module = __import__('modules.connection',fromlist=["modules"])
            csv_module = __import__('modules.csv_mod',fromlist=["modules"])
            
            return conf_module.shared(), con_module.connection(), csv_module
        except:
            return False

def __load_data_collect(device):
    try:
        data_module = __import__('modules.{type}_data_collect'.format(type=device["con_type"]),fromlist=["modules"])
        return data_module.data_collect()
    except Exception as e:
        print(e)
        return False

def main(args):

        configuration, connection, csv_mod = __load_module()      
        device= configuration.__getDevice__(args.n)
        inst=connection.connect(device)
        dataCollect=__load_data_collect(device)
        shell = inst.connectionPort(args)
        res,mod_inf=dataCollect.commands(device,shell) 
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