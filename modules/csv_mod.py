
# CSV file functions

class csv_mod: 
    
    ## Writes output to csv file

    def print_to_csv(device, mod_inf):
        try:

            from csv import writer
            from datetime import datetime

            header=[]
            list=[]
            with open("results/" + str(device["device"]) + "_" + str(datetime.now()) + '.csv', 'x') as file:
                write = writer(file)

                for line in device["commands"]:
                    header=line
                    parameters=""
                    for item in line["res_param"]:
                        parameters=parameters+str(item)+","
                    list.append([line["command"],line["param"],line["expectedO"],parameters,line["res"]])

                write.writerow(mod_inf)    
                write.writerow(header)    
                write.writerows(list)

        except Exception as e:
            print(e)
            exit()
