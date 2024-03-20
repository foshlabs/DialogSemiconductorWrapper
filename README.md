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

FoshWrapper is based on BlueZ, the official Linux Bluetooth protocol stack. Install BlueZ v5.0 or later for correct behavior.

## FoshWrapper Installation

FoshWrapper's main dependency is PyGTK, which will be installed automatically with FoshWrapper.

## Usage

Basic usage is shown below, demonstrating device discovery and connection.

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
