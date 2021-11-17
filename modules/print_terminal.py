
# Terminal printer module

class print_terminal:

    ## Prints output to terminal

    def term_print(self,device,size,deviceName,passed,failed):
        CRED = '\033[91m'
        CGREEN  = '\33[32m'
        CEND = '\033[0m'
        back = "\033[F"

        try:
            print("Device: "+ deviceName + "                 \r")
            print(device["command"] + ": Running                   \r" )
            print("Command count: " + str(size) + "\r")
            print(CGREEN+"Passed: "+CEND + str(passed) + CRED +"  Failed: " + CEND + str(failed)+ (back*4) +"\r")
                
            if size == passed+failed:
                print("\n\n\n")
        except Exception as e:
            print(e)
            print("Failed to print output to terminal")