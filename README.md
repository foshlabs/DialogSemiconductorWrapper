# Fosh Wrapper = Dialog DA14583 IoT module
Fosh Wrapper is dedicated for easy work with bluetooth module from DialogSemiconductor.
Module has been tested on Ubuntu 16.04 width Python 3.
FoshWrapper also using another Python librari which pygatt (https://github.com/peplin/pygatt)

IoT datasheet 
https://support.dialog-semiconductor.com/system/files/restricted/UM-B-063_DA14583_IoT_Sensor_Development_Kit_1v3.pdf

* How to install it
- install pygatt library

```
#!bash

    sudo pip3 install pygatt

```

- install FoshWrapper (clone this repository)

```
#!bash

    git clone https://github.com/misisnik/FoshWrapper
    cd FoshWrapper
    python3 setup.py install

```

- if u do not have bluez >= v.5

```
#!bash
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

- enable experimental

```
#!bash
    sudo vim /lib/systemd/system/bluetooth.service

```
    and add flag to ExecStart - it should looks like
    
```
#!bash
    ExecStart=/usr/local/libexec/bluetooth/bluetoothd --experimental

```
    
```
#!bash
    sudo systemctl restart bluetooth

```


* How to use it

```
#!python

    from FoshWrapper import FoshWrapper

    fosh = FoshWrapper()
    ......to dooo .....
```