import importlib

# Conection module


class connection: 

    ## imports module for device connection

    def connect(self,device):
        try:
            module = importlib.import_module("modules.{type}_con".format(type=device["con_type"]))
            my_class = getattr(module, "{type}_con".format(type=device["con_type"]))
            inst = my_class()
            return inst    
        except TypeError:
            print("Could not import module") 

            

