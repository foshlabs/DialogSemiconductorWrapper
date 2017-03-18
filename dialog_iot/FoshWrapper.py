"""
FoshWrapper
======================================
.. moduleauthor:: Michal Sladecek <misisnik@gmail.com>
.. autoclass:: FoshWrapper
   :members:

"""
import logging
import pygatt
from pygatt.exceptions import NotConnectedError, BLEError, NotificationTimeout
import time

#uuids of all characteristics
_uuids = { 'accelerometer'  : '2ea78970-7d44-44bb-b097-26183f402401'
         , 'gyroscope'      : '2ea78970-7d44-44bb-b097-26183f402402'
         , 'magnetometer'   : '2ea78970-7d44-44bb-b097-26183f402403'
         , 'sensorFusion'   : '2ea78970-7d44-44bb-b097-26183f402407'
         , 'deviceFeatures' : '2ea78970-7d44-44bb-b097-26183f402408'
         , 'controlPoint'   : '2ea78970-7d44-44bb-b097-26183f402409'
         , 'commandReply'   : '2ea78970-7d44-44bb-b097-26183f40240a' }

#commands with result mark
_cmd_db = {   'stop'                            : (0, True)
            , 'start'                           : (1, True)
            , 'read_flash'                      : (2, False)
            , 'reset'                           : (3, False)
            , 'store_config'                    : (4, False)
            , 'store_calibration_flash'         : (5, False)
            , 'runing_status'                   : (6, True)
            , 'reset_calibration'               : (7, False)
            , 'basic_configuration'             : (10, False)
            , 'get_configuration'               : (11, True)
            , 'set_sensor_fusion'               : (12, False)
            , 'fusion_coeficients'              : (13, True)
            , 'set_calibration_coeficients'     : (14, False)
            , 'read_calibration_coeficients'    : (15, True)
            , 'set_calibration_control_flag'    : (16, False)
            , 'read_calibration_control'        : (17, True)
            , 'fast_accelerometr_calibration'   : (18, True) }

#config data structure
_config_structure = [ 'sensor_combination' 
                    , 'accelerometer_range'
                    , 'accelerometer_rate'
                    , 'gyroscope_range'
                    , 'gyroxcope_rate'
                    , 'magnetometer_rate'
                    , 'enviromental_rate'
                    , 'sensor_fusion_rate'
                    , 'sensor_fusion_raw_en'
                    , 'calibration_mode'
                    , 'auto_calibration_mode' ]

class FoshWrapper(object):
    """
        Fosh Iot is easy wraper for Dialog semiconductor IoT development kit
        More info about it you could find in Readme.md and IoT datasheet
        For connection is used pygatt library with bluetooth linux library
        bluez which has to be version 5 or gigher!!
    """
    def __init__(self, log = False):
        # set logging
        if log:
            logging.basicConfig()
            logging.getLogger('pygatt').setLevel(logging.DEBUG)
        self.device = None
        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()

        self.reply_buf = {}
        self.config = {  'sensor_combination'    : 7
                        , 'accelerometer_range'   : 0x0C
                        , 'accelerometer_rate'    : 0x08
                        , 'gyroscope_range'       : 0x03
                        , 'gyroxcope_rate'        : 0x08
                        , 'magnetometer_rate'     : 0x00
                        , 'enviromental_rate'     : 1
                        , 'sensor_fusion_rate'    : 25
                        , 'sensor_fusion_raw_en'  : 1
                        , 'calibration_mode'      : 1
                        , 'auto_calibration_mode' : 0 }
        self.subscribed_uuids = []
        self.subscribed_callbacks = {}
        self.run = None

    def __exit__(self):
        """ Just make shure that device will be disconect"""
        self.adapter.stop()

    def __del__(self):
        """ Just make shure that device will be disconect"""
        self.adapter.stop()

    def find(self, connect = False, timeout = 10, device_name = 'IoT'):
        """
            Function find() could scan all bluetooth devices.
            If parameter connect is True and any iot device exists, it will be
            called function for connect to this device. If there are more than
            one, program will connect to the first one.
            Parameter timeout define time for searching ble devices.
            It resurns array of devices if any exists or just True/False if 
            user want to connect to those. Parameter device_name is scring which
            describe your device name
        """
        try:
            devices = self.adapter.scan(timeout)
        except BLEError as e:
            raise e

        if not connect:
            return devices

        #find out any IoT device
        for d in devices:
            if d['name'].startswith(device_name):
                return self.connect(d['address'])

    def connect(self, address = ''):
        """
            Function connect() with paramere address is constructed for 
            connection into ble device
        """
        try:
            self.device = self.adapter.connect(str(address))
            return True
        except NotConnectedError as e:
            #connection error
            raise e

    def subscribe(self, uuid_name = '', callback = None):
        """
            Function subscribe is for subscribing characterictic with predefined
            uuid, if any data come from device with uuid function callback will
            be define. Indication is alwais False because of linux communication
        """
        uuid = _uuids[uuid_name]
        if uuid not in self.subscribed_uuids:
            self.device.subscribe(uuid, callback, False)
            self.subscribed_uuids.append(uuid)
            self.subscribed_callbacks['uuid'] = callback

    def unsubscribe(self, uuid_name = ''):
        """
            Unsubscribe communication with uuid
        """
        uuid = _uuids[uuid]
        if uuid in self.subscribed_uuids:
            self.device.unsubscribe(uuid)
            self.subscribed_uuids.remove(uuid)
            del self.subscribed_callbacks[uuid]

    def read(self, uuid = ''):
        """
            Read from uuid
        """
        self.device.char_read(uuid)

    def write(self, uuid = '', data = []):
        """
            write into connected device with uuid
            data should be array od commands
        """
        if uuid == _uuids['controlPoint'] and _uuids['commandReply']\
        not in self.subscribed_uuids:
            self.subscribeCommands()
        self.device.char_write(uuid, bytearray(data), True)

    #configuration
    def subscribeCommands(self):
        """
            this intern function subscribe commands reply char
        """
        def commandReply(handle, data):
            self.reply_buf = {'id': data[1], 'data': data[2:]}
        self.subscribe('commandReply', commandReply)

    def cmd(self, cmd, data = []):
        """
            this function getting configuration seting of IoT
        """
        if cmd not in _cmd_db:
            raise IOError('Command is not in db')

        cmd , response = _cmd_db[cmd]
        data = [cmd] + data
        if response:
            self.reply_buf = {}
        self.write(_uuids['controlPoint'], data)

        if response:
            while self.reply_buf == {}:
                time.sleep(0.0001)
            return self.reply_buf
        else:
            time.sleep(0.0001)
            return True

    def setConfig(self, flash = True):
        """
            function for config sensor
            write to flash 
        """
        def getConfigData():
            return [self.config[n] for n in _config_structure]

        if self.run or self.run is None:
            self.run = False
            self.cmd('stop')
        #write !
        self.cmd('basic_configuration', getConfigData())
        if flash:
            self.cmd('store_config')

    def getConfig(self):
        """
            just return actual sensor configuration and push it into local 
            config dictionary
        """
        data = self.cmd('get_configuration')
        for i, b in enumerate(_config_structure):
            self.config[b] =  data['data'][i]
        return self.config

    def start(self):
        """
            function for start
        """
        self.cmd('start')

    def stop(self):
        """
            function for stop
        """
        self.cmd('stop')

    def reset(self):
        """
            function for reset
        """
        self.cmd('reset')

    def accelerometerCalibration(self):
        """
            just fast accelerometer calibration
        """
        return self.cmd('fast_accelerometr_calibration')
