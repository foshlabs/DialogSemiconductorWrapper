# Wrapper for Dialog DA14583 IoT Module

Wrapper for the Dialog Semiconductor IoT Bluetooth module. Tested on Ubuntu 16.04, Python 3.

**Features**

- Subscribe to module characteristics
- Configuration
- Read/Write
- Calibration
- Examples

## Sections

- [Requirements](https://chat.openai.com/c/1aea3db2-e7e1-4138-b81e-2c6eae8c1ef7#requirements)
- [BlueZ Installation](https://chat.openai.com/c/1aea3db2-e7e1-4138-b81e-2c6eae8c1ef7#bluez-installation)
- [FoshWrapper Installation](https://chat.openai.com/c/1aea3db2-e7e1-4138-b81e-2c6eae8c1ef7#foshwrapper-installation)
- [Usage](https://chat.openai.com/c/1aea3db2-e7e1-4138-b81e-2c6eae8c1ef7#usage)
- [Functions](https://chat.openai.com/c/1aea3db2-e7e1-4138-b81e-2c6eae8c1ef7#functions)

## Requirements

- Python 2.7 or greater (tested on v3.5)
- BlueZ 5.18 or greater with `gattool`
- PyGTK library

## BlueZ Installation

FoshWrapper is based on BlueZ. BlueZ is the official Linux Bluetooth protocol stack. For correct behavior, install BlueZ v5.0 or later:
```
sudo apt-get install bluez
```

Change the BlueZ service configuration for experimental use (because of Bluetooth Low Energy):
```
sudo vim /lib/systemd/system/bluetooth.service
```

Edit the line starting with "ExecStart" so it looks like this:
```
ExecStart=/usr/local/libexec/bluetooth/bluetoothd --experimental
```

Restart the Bluetooth service:
```
sudo systemctl restart bluetooth
```

## FoshWrapper Installation

FoshWrapper's main dependency is PyGTK (https://github.com/peplin/pygatt). However, it will be installed automatically along with FoshWrapper:
```
git clone git@github.com:foshlabs/FoshWrapper.git
cd FoshWrapper
python3 setup.py install
```

## Usage

Basic usage is shown below (also in the example directory):
```
from dialog_iot import FoshWrapper

fosh = FoshWrapper()
# fosh = FoshWrapper(True) # For console logging

# Find devices and print them
devices = fosh.find(connect=False)
print(devices)

# Connect to a specific MAC address
try:
    fosh.connect('80:EA:CA:00:D2:28')
except Exception as e:
    print(e)  # Error handling
```

## Functions

- **find(connect=False, timeout=10, device_name='IoT')**
    - Returns an array of all found BLE devices.
    - Automatically connects to the first device named "IoT" if `connect` is True.
- **connect(address='')**
    - Connects to a device using the specified MAC address.
- **subscribe(uuid_name='', callback=None)** / **unsubscribe(uuid_name='')**  
    - Subscribes/unsubscribes to predefined characteristics.
    - For each response, calls the `callback` function.
- **read(uuid_name='')**
    - Reads data from the specified UUID.
- **getConfig()**
    - Retrieves and stores the device configuration in the `.config` variable.
- **setConfig(flash=True)**
    - Sets the device configuration from the `.config` variable. Requires a start command afterward.
- **start()** / **stop()** / **reset()** / **accelerometerCalibration()**
    - Provides various control functions for device operation.
- **cmd(cmd, data=[])**
    - Sends a custom command to the device. `cmd` is the command name; `data` is an array of hex or decimal data.

## License

MIT

## Authors

Michal Sladecek - misisnik@gmail.com
