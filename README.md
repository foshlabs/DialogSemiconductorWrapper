# Wrapper for Dialog DA14583 IoT module
Wrapper for DialogSemiconductor IoT bluetooth module. 
Tested on Ubuntu 16.04, Python 3.

Features:
  - Subscribe module characteristics
  - Configuration
  - Read/Write
  - Calibration
  - Examples
 
Sections:
- [Requirementss](#requirements)
- [Bluez installation](#bluez-installation)
- [FoshWrapper instalation](#foshwrapper-installation)
- [Usage](#usage)
- [Functions](#functions)

## Requirements
- Python 2.7 or greater (tested on v.3.5)
- BlueZ 5.18 or greater with gattool
- PyGTK library
## BlueZ installation
FoshWrapper is based on BlueZ. BlueZ is the official Linux Bluetooth protocol stack. For correct behaviour, install BlueZ v5.0 and later:
```sh
sudo apt-get install bluez
```
Change BlueZ service configuration for the experimental use (because of Bluetooth Low Energy):
```sh
sudo vim /lib/systemd/system/bluetooth.service
```
Edit the line starting with "ExecStart......" so it looks like this:
```sh
ExecStart=/usr/local/libexec/bluetooth/bluetoothd --experimental
```
Restart the Bluetooth service:
```sh
systemctl restart bluetooth
```
## FoshWrapper installation
FoshWrapper's main dependency is PyGTK (https://github.com/peplin/pygatt). However, it will be installed automatically along with FoshWrapper installation:
```sh
git clone git@github.com:foshlabs/FoshWrapper.git
cd FoshWrapper
python3 setup.py install
```
## Example
Basic usage is shown bellow (also in the example directory):
```python3
from dialog_iot import FoshWrapper

fosh = FoshWrapper()
#fosh = FoshWrapper(True) #for console logging

#find devices and print it
devices = fosh.find(connect = False)
print(devices)

#connect to the specific mac address
try:
    fosh.connect('80:EA:CA:00:D2:28')
except Exception as e:
    print(e) #error time :D
```
After that you can use any of Fosh functions doccumentated bellow:

## Functions
####  find(connect = False, timeout = 10, device_name = 'IoT')
- this function return array of all founded ble device
- if u set variable connect to the True, wrapper automatically connect into the first device with name IoT (or into the your defined device_name)
####  connect(address = '')
- just connect into specific device with mac address declared
####  subscribe(uuid_name = '', callback = None)
####  unsubscribe(uuid_name = '')
These functions just subscribe/unsubscribe predefined characteristics. For each response from this subscribe will be automatically called function "callback"
####  read(uuiod_name = '')
Table of uuid_names:

| uuid_name | description |
| ------ | ------ |
| accelerometer | data from accelerometer |
| gyroscope | data from gyroscope |
| magnetometer | data from magnetometer |
| sensorFusion | data from sensorFusion |
| deviceFeatures | data from hunidity and temperature sensor |
####   getConfig()
return configuration from device and also store it in the .config variable
####  setConfig(flash = True)
set device configuration which is in the .config variable like dictionary 
AFTER EACH SETCONFIG IS NEEDED TO SEND START COMMAND

| config[name] | options (more in 6.1.3.9 datasheets chapter) |
| ------ | ------ |
|sensor_combination|2: Gyro / 3: Accel + Gyro / 5: Accel + Mag / 7: Accel + Gyro + Mag|
|accelerometer_range|0x03: 2G / 0x05: 4G / 0x08: 8G /0x0C: 16G|
|accelerometer_rate|0x01: 0.78 Hz / 0x02: 1.56 Hz / 0x03: 3.12 Hz / 0x04: 6.25 Hz / 0x05: 12.5 Hz / 0x06: 25 Hz / 0x07: 50 Hz / 0x08: 100 Hz|
|gyroscope_range|0x00: 2000 deg/s / 0x01: 1000 deg/s / 0x02: 500 deg/ / 0x03: 250 deg/s|
|gyroscope_rate|0x01: 0.78 Hz / 0x02: 1.56 Hz / 0x03: 3.12 Hz / 0x04: 6.25 Hz / 0x05: 12.5 Hz / 0x06: 25 Hz / 0x07: 50 Hz / 0x08: 100 Hz|
|magnetometer_rate|Reserved for future use|
|enviromental_rate|1: 0.5 Hz / 2: 1 Hz / 4: 2 Hz|
|sensor_fusion_rate|10: 10 Hz / 15: 15 Hz / 20: 20 Hz / 25: 25 Hz|
|sensor_fusion_raw_en|0: Disabled / 1: Enabled|
|calibration_mode|0: None / 1: Static / 2: Continuous / 3: One Shot|
|auto_calibration_mode|0: Basic / 1: SmartFusion|

####  start()
####  stop()
####  reset()
####  accelerometerCalibration()
There are some predefined commands function


Finally you could create command request by someselve with cmd function
####  cmd(cmd, data = [])
cmd is command name from table which been described its function
data is array input of hex or dec data whatewer

| cmd | description |
| ------ | ------ |
|stop|There is some response|
|start|There is some response|
|read_flash|Response is none|
|reset|Response is none|
|store_config|Response is none|
|store_calibration_flash|Response is none|
|runing_status|There is some response|
|reset_calibration|Response is none|
|basic_configuration|Response is none|
|get_configuration|There is some response|
|set_sensor_fusion|Response is none|
|fusion_coeficients|There is some response|
|set_calibration_coeficients|Response is none|
|read_calibration_coeficients|There is some response|
|set_calibration_control_flag|Response is none|
|read_calibration_control|There is some response|
|fast_accelerometr_calibration|There is some response|

License
----

MIT

Authors
----
Michal Sladecek - misisnik@gmail.com
