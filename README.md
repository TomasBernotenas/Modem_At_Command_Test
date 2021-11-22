# Modem_At_Command_Test
## Setup
**Python version:** 3.9.5 <br>
<br>
**Paramiko library:**<br>
used to communicate with the device using SSH protocol ```$ pip install paramiko```<br>
<br>
**PySerial library:**<br>
used to communicate with the device using serial port ```$ pip install pyserial```<br>
<br>
## Configuration file usage
Configuration file is used to define devices with their connection type and the commands that will be tested on those devices.<br>
<br>
All information has to be stored inside ```"devices":``` json object array.<br>
<br>
Every command parameter that requires qoutes ```""``` has to be encapsulated in single qoutes ```''``` <br>
<br>
**Device structure**<br>
<br>
```"device":``` Device name for which the configuration is being created.<br>
```"con_type":``` Connection type that this device is using.<br>
```"commands":[]``` All commands for the specified device is stroed inside **commands** array.<br>
<br>
**Command structure**<br>
<br>
```"command":``` Modem command to be executed.<br>
```"param":``` Parameters for the command if needed, if not then param should be left with 1 empty space.<br>
```"expectedOutput":``` Expected output of the modem command.<br>
<br>
**Example**
```json
{
    "devices": [
        {
            "device": "trm240", 
            "con_type" : "serial",
            "commands":[
                {
                    "command": "ATI",
                    "param": " ",
                    "expectedOutput":"OK" 
                },
                {
                    "command": "AT+CMGF=1",
                    "param": " ",
                    "expectedOutput":"OK"
                },
                {
                    "command": "AT+CMGS='+37067247441'",
                    "param": "zinute",
                    "expectedOutput":"OK"
                },
                {
                    "command": "AT+CSCS='GSM'",
                    "param": " ",
                    "expectedOutput":"OK"
                }
            ]
         }
     ]
}
```


## Starting the script
Script is started using **main.py** module but it requires some parameters depending on the connection type.<br>
<br>
**Parameters**<br>
+ Serial connection<br>
```-d``` Device name that will be tested.<br>
```-a``` Device ip address or connection port.<br>
+ SSH connection<br>
```-d``` Device name that will be tested.<br>
```-a``` Device ip address or connection port.<br>
```-cp``` Connection port for SSH connection (Optional, default=22) .<br>
```-u``` Username for SSH connection athentification.<br>
```-p``` Password for SSH connection authentification.<br>

**Example**<br>

* Example for serial connection<br>
```python3 main.py -d trm240 -a /dev/ttyUSB3```

* Example for SSH connection<br>
```python3 main.py -d rutx11 -a 192.168.5.2 -u root -p Admin123```<br>
