from json import load

# Functions for shared module use

## Config file reading

class config:

    ## Checks if the config file has the entered device and returns its commands 

    def get_device_info(deviceName):
        try:
            device = None
            with open("config.json","r") as file:
                devices = load(file)
                for dev in devices["devices"]:
                    if dev["device"].lower() == deviceName.lower():
                        device = dev
                        break 
            if device==None:    
                raise TypeError
        except TypeError:
            print("There is no such device in configuration file")
        return device




