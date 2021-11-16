import json
from datetime import datetime


# Functions for shared module use

## Config file reading
## CSV file writing

class shared:

    __configName = "config.json"
    __config = None

    ## On initialization calls configuration open function

    def __init__(self):
        self.__openConfig__()

    ## Opens configuration file

    def __openConfig__(self):
        config = open(self.__configName, "r")
        try:
            self.__config = config
        except:
            print("Unable to open file")
            exit()

    ## Closes configuration file

    def __closeConfig__(self):
        if self.__config:
            self.__config.close()

    ## Checks if the config file has the entered device and returns its commands 

    def getDevice(self, deviceName):
        try:
            device = None
            devices = json.load(self.__config)
            for dev in devices["devices"]:
                if dev["device"] == deviceName:
                    device = dev
                    break 
            if device==None:    
                raise TypeError
        except TypeError:
            print("There is no such device in configuration file")
        return device

    ## Calls configuration file closing function

    def __del__(self):
        self.__closeConfig__()

    ## Writes output to csv file

    def print_csv(device, mod_inf):
        try:
            import csv
            header=[]
            list=[]
            with open("../results/" + str(device["device"]) + "_" + str(datetime.now()) + '.csv', 'x') as file:
                writer = csv.writer(file)

                for line in device["commands"]:
                    header=line
                    list.append([line["command"],line["param"],line["expectedO"],line["res_param"],line["res"]])

                writer.writerow(mod_inf)    
                writer.writerow(header)    
                writer.writerows(list)
        except Exception as e:
            print(e)

## Returns commands of the provided device

def getDevice(args):

    dev=shared()
    device = dev.getDevice(args.n)
    return device

## Calls csv writer function

def print_tocsv(device,mod_inf):
    shared.print_csv(device,mod_inf)
