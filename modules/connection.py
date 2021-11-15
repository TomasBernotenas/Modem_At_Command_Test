import importlib

# Conection module


class connection: 

    ## imports module for device connection

    def connect(device):
        try:
            module = importlib.import_module(device["con_type"]+"_con")
            my_class = getattr(module, device["con_type"]+"_con")
            inst = my_class()
            return inst    
        except TypeError:
            print("Could not import module") 

            

