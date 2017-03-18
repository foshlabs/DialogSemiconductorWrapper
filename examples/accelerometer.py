from dialog_iot import FoshWrapper
import time


##subscribed functions
#function accelerometer_data_callback()
def accelerometer_data_callback(handle, data):
    #ok handle of commands will be store in "handle"
    #and accelerometer data will be store in "data" as bytearray
    print("{} -- {}".format(handle, data))

#connect to the device
fosh = FoshWrapper()

#show found devices, without connect
#if someone wants to connect directly, just connect = True
devices = fosh.find(connect = False)
print(devices)

#ok connect to the specific device via mac address
try:
    fosh.connect('80:EA:CA:00:D2:28')
except Exception as e:
    print(e) #error time :D
    exit()

#so we have been successfuly connected
#so now we wants to change speed of accelerometer

#load configuration from Iot device
config = fosh.getConfig()
#sensor_combination is accelerometer and Gyroscope
fosh.config['sensor_combination'] = 3
#accelerometer rate to 100Hz
fosh.config['accelerometer_rate'] = 0x08

#if config is not equal to the fosh.config just send it to the device
if config != fosh.config:
    fosh.setConfig()    #set config and also store this configuration in eeprom
    #fosh.setConfig(False) #set config without storing it in eeprom

#now we wants to get accelerometer data and response will be in f
fosh.subscribe('accelerometer', accelerometer_data_callback)
#send command for start!!!
fosh.start()

#ok we have to w8 for accelerometer data which will be 
#in accelerometer_data_callback
while 1:
    time.sleep(2)