
class csv_mod: 
    
    ## Writes output to csv file

    def __print_csv__(device, mod_inf):
        try:

            import csv
            from datetime import datetime

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

## Calls csv writer function

def print_tocsv(device,mod_inf):
    csv_mod.__print_csv__(device,mod_inf)