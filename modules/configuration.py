import json

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

    def __getDevice__(self, deviceName):
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

## Returns commands of the provided device

def getDevice(args):

    dev=shared()
    device = dev.__getDevice__(args.n)
    return device



