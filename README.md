# FoshWrapper for Dialog DA14583 IoT module
Fosh Wrapper is dedicated for easy work with DialogSemiconductor bluetooth module. 
Wraper is tested on Ubuntu 16.04 and Python 3.

Wrappers features:
  - Subscribes all characteristics
  - Change configuration things
  - Read/Write
  - Simple calibration
  - Examples
 
Sections:
- [Requirementss](#requirements)
- [Bluez installation](#bluez-installation)
- [FoshWrapper instalation](#foshwrapper-installation)
- [Usage](#usage)
- [Functions](#functions)

## Requirements
- python 2.7 or greater (tested on v.3.5)
- BlueZ 5.18 or greater with gattool
- pygatt library
## Bluez installation
Fosh wrapper is based on bluez module which is official bluetooth distribution in ubuntu linux
```sh
sudo apt-get install bluez
```
For correctly function is needs bluez>=5 so if you dont have this wersion install the newest. For example in Ubuntu 16.4 you needs to upgrade it because bluez version higher than 5 is compose from Ubuntu 16.10.
```sh
sudo apt-get update
sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.44.tar.xz
tar xvf bluez-5.44.tar.xz
cd bluez-5.44
./configure --prefix=/usr           \
            --mandir=/usr/share/man \
            --sysconfdir=/etc       \
            --localstatedir=/var    \
            --enable-library        \
            --disable-systemd       \
            --disable-android       
make
sudo make install
```
Finally you have to edit configuration of bluez to the expperimental use (because BLE)
```sh
sudo vim /lib/systemd/system/bluetooth.service
```
and eddit line which starts with "ExecStart......" to this format:
```sh
ExecStart=/usr/local/libexec/bluetooth/bluetoothd --experimental
```
finally just restart the bluetooth service
```sh
systemctl restart bluetooth
```
## FoshWrapper installation
Fosh wrapper using pygatt (https://github.com/peplin/pygatt) module which is main dependence. This module should be installed automatically with FoshWrapper installation:
```sh
git clone https://github.com/misisnik/FoshWrapper
cd FoshWrapper
python3 setup.py install
```
## Usage
Basic usege is indicate in example directory. Or here
```python3
from dialog_iot import FoshWrapper

fosh = FoshWrapper()

#find devices and print it
devices = fosh.find(connect = False)
print(devices)

#connect to the specific mac address
try:
    fosh.connect('80:EA:CA:00:D2:28')
except Exception as e:
    print(e) #error time :D
```
after that you could deal with easy Fosh functions

## Functions
####  find(connect = False, timeout = 10, device_name = 'IoT')
- this function returns array of all ble device
- if u set connect to True, wrapper automatically connect into first device with name IoT
####  connect(address = '')
- just connect into specific device with declared mac address
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
Finally you could create command request someselve by function
####  cmd(cmd, data = [])
cmd is command name from table which is describe in downpage
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
