#!/usr/bin/env python3.7

# NB: extremely Work In Progress, here be dragons, enter at own risk, etc

import sys
import os
import base64
import requests
import struct
import time
import argparse
import zeroconf
import json

MY_DEVICE_ID='robs-script'
MY_OPERATOR_ID='rob'

TIMEZONE='UTC'
if os.path.exists('/etc/timezone'):
    TIMEZONE=open('/etc/timezone', 'r').read().strip()

OUTDOOR_TEMPS = [
    -50.0,
    -50.0,
    -50.0,
    -50.0,
    -50.0,
    -48.9,
    -46.0,
    -44.0,
    -42.0,
    -41.0,
    -39.0,
    -38.0,
    -37.0,
    -36.0,
    -35.0,
    -34.0,
    -33.0,
    -32.0,
    -31.0,
    -30.0,
    -29.0,
    -28.5,
    -28.0,
    -27.0,
    -26.0,
    -25.5,
    -25.0,
    -24.0,
    -23.5,
    -23.0,
    -22.5,
    -22.0,
    -21.5,
    -21.0,
    -20.5,
    -20.0,
    -19.5,
    -19.0,
    -18.5,
    -18.0,
    -17.5,
    -17.0,
    -16.5,
    -16.0,
    -15.5,
    -15.0,
    -14.6,
    -14.3,
    -14.0,
    -13.5,
    -13.0,
    -12.6,
    -12.3,
    -12.0,
    -11.5,
    -11.0,
    -10.6,
    -10.3,
    -10.0,
    -9.6,
    -9.3,
    -9.0,
    -8.6,
    -8.3,
    -8.0,
    -7.6,
    -7.3,
    -7.0,
    -6.6,
    -6.3,
    -6.0,
    -5.6,
    -5.3,
    -5.0,
    -4.6,
    -4.3,
    -4.0,
    -3.7,
    -3.5,
    -3.2,
    -3.0,
    -2.6,
    -2.3,
    -2.0,
    -1.7,
    -1.5,
    -1.2,
    -1.0,
    -0.6,
    -0.3,
    0.0,
    0.2,
    0.5,
    0.7,
    1.0,
    1.3,
    1.6,
    2.0,
    2.2,
    2.5,
    2.7,
    3.0,
    3.2,
    3.5,
    3.7,
    4.0,
    4.2,
    4.5,
    4.7,
    5.0,
    5.2,
    5.5,
    5.7,
    6.0,
    6.2,
    6.5,
    6.7,
    7.0,
    7.2,
    7.5,
    7.7,
    8.0,
    8.2,
    8.5,
    8.7,
    9.0,
    9.2,
    9.5,
    9.7,
    10.0,
    10.2,
    10.5,
    10.7,
    11.0,
    11.2,
    11.5,
    11.7,
    12.0,
    12.2,
    12.5,
    12.7,
    13.0,
    13.2,
    13.5,
    13.7,
    14.0,
    14.2,
    14.4,
    14.6,
    14.8,
    15.0,
    15.2,
    15.5,
    15.7,
    16.0,
    16.2,
    16.5,
    16.7,
    17.0,
    17.2,
    17.5,
    17.7,
    18.0,
    18.2,
    18.5,
    18.7,
    19.0,
    19.2,
    19.4,
    19.6,
    19.8,
    20.0,
    20.2,
    20.5,
    20.7,
    21.0,
    21.2,
    21.5,
    21.7,
    22.0,
    22.2,
    22.5,
    22.7,
    23.0,
    23.2,
    23.5,
    23.7,
    24.0,
    24.2,
    24.5,
    24.7,
    25.0,
    25.2,
    25.5,
    25.7,
    26.0,
    26.2,
    26.5,
    26.7,
    27.0,
    27.2,
    27.5,
    27.7,
    28.0,
    28.2,
    28.5,
    28.7,
    29.0,
    29.2,
    29.5,
    29.7,
    30.0,
    30.2,
    30.5,
    30.7,
    31.0,
    31.3,
    31.6,
    32.0,
    32.2,
    32.5,
    32.7,
    33.0,
    33.2,
    33.5,
    33.7,
    34.0,
    34.3,
    34.6,
    35.0,
    35.2,
    35.5,
    35.7,
    36.0,
    36.3,
    36.6,
    37.0,
    37.2,
    37.5,
    37.7,
    38.0,
    38.3,
    38.6,
    39.0,
    39.3,
    39.6,
    40.0,
    40.3,
    40.6,
    41.0,
    41.3,
    41.6,
    42.0,
    42.3,
    42.6,
    43.0
]

INDOOR_TEMPS = [
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -30.0,
    -29.0,
    -28.0,
    -27.0,
    -26.0,
    -25.0,
    -24.0,
    -23.0,
    -22.5,
    -22.0,
    -21.0,
    -20.0,
    -19.5,
    -19.0,
    -18.0,
    -17.5,
    -17.0,
    -16.5,
    -16.0,
    -15.0,
    -14.5,
    -14.0,
    -13.5,
    -13.0,
    -12.5,
    -12.0,
    -11.5,
    -11.0,
    -10.5,
    -10.0,
    -9.5,
    -9.0,
    -8.6,
    -8.3,
    -8.0,
    -7.5,
    -7.0,
    -6.5,
    -6.0,
    -5.6,
    -5.3,
    -5.0,
    -4.5,
    -4.0,
    -3.6,
    -3.3,
    -3.0,
    -2.6,
    -2.3,
    -2.0,
    -1.6,
    -1.3,
    -1.0,
    -0.5,
    0.0,
    0.3,
    0.6,
    1.0,
    1.3,
    1.6,
    2.0,
    2.3,
    2.6,
    3.0,
    3.2,
    3.5,
    3.7,
    4.0,
    4.3,
    4.6,
    5.0,
    5.3,
    5.6,
    6.0,
    6.3,
    6.6,
    7.0,
    7.2,
    7.5,
    7.7,
    8.0,
    8.3,
    8.6,
    9.0,
    9.2,
    9.5,
    9.7,
    10.0,
    10.3,
    10.6,
    11.0,
    11.2,
    11.5,
    11.7,
    12.0,
    12.3,
    12.6,
    13.0,
    13.2,
    13.5,
    13.7,
    14.0,
    14.2,
    14.5,
    14.7,
    15.0,
    15.3,
    15.6,
    16.0,
    16.2,
    16.5,
    16.7,
    17.0,
    17.2,
    17.5,
    17.7,
    18.0,
    18.2,
    18.5,
    18.7,
    19.0,
    19.2,
    19.5,
    19.7,
    20.0,
    20.2,
    20.5,
    20.7,
    21.0,
    21.2,
    21.5,
    21.7,
    22.0,
    22.2,
    22.5,
    22.7,
    23.0,
    23.2,
    23.5,
    23.7,
    24.0,
    24.2,
    24.5,
    24.7,
    25.0,
    25.2,
    25.5,
    25.7,
    26.0,
    26.2,
    26.5,
    26.7,
    27.0,
    27.2,
    27.5,
    27.7,
    28.0,
    28.2,
    28.5,
    28.7,
    29.0,
    29.2,
    29.5,
    29.7,
    30.0,
    30.2,
    30.5,
    30.7,
    31.0,
    31.3,
    31.6,
    32.0,
    32.2,
    32.5,
    32.7,
    33.0,
    33.2,
    33.5,
    33.7,
    34.0,
    34.2,
    34.5,
    34.7,
    35.0,
    35.3,
    35.6,
    36.0,
    36.2,
    36.5,
    36.7,
    37.0,
    37.2,
    37.5,
    37.7,
    38.0,
    38.3,
    38.6,
    39.0,
    39.2,
    39.5,
    39.7,
    40.0,
    40.3,
    40.6,
    41.0,
    41.2,
    41.5,
    41.7,
    42.0,
    42.3,
    42.6,
    43.0,
    43.2,
    43.5,
    43.7,
    44.0,
    44.3,
    44.6,
    45.0,
    45.3,
    45.6,
    46.0,
    46.2,
    46.5,
    46.7,
    47.0,
    47.3,
    47.6,
    48.0,
    48.3,
    48.6,
    49.0,
    49.3,
    49.6,
    50.0,
    50.3,
    50.6,
    51.0,
    51.3,
    51.6,
    52.0
]

def get_home_leave_mode_air_flow(i):
    if i == 3:
        return 1
    if i == 5:
        return 2
    if i != 7:
        return 0 if i != 14 else 4
    return 3

class AttrBase(object):
    def __init__(self, name):
        self.name = name
        self.value = None

    def __str__(self):
        return '%s: %r' % (self.name, self.value)
        
    def set(self, value):
        self.value = value

    def set_from_bytes(self, byte_array):
        raise NotImplementedError

    def apply(self, byte_array, is_control=None):
        raise NotImplementedError
        
class AttrByte(AttrBase):
    def __init__(self, name, bytepos, mask=None, controlbit=None, to_byte=None, of_byte=None):
        super().__init__(name)
        self.name = name
        self.bytepos = bytepos
        self.mask = mask
        self.controlbit = controlbit
        self.value = None
        self.is_control = False
        self.to_byte = to_byte
        self.of_byte = of_byte

    def set_from_bytes(self, byte_array):
        byte = byte_array[self.bytepos]
        if self.mask:
            byte &= self.mask
        if self.controlbit:
            self.is_control = bool(byte & self.controlbit)
            byte &= ~ self.controlbit
        if self.of_byte:
            byte = self.of_byte(byte)
        self.value = byte

    def apply(self, byte_array, is_control=None):
        if is_control is None:
            is_control = self.is_control
        byte = self.value if self.value else 0
        if self.to_byte:
            byte = self.to_byte(byte)
        if self.mask:
            byte &= self.mask
        if is_control and self.controlbit:
            byte |= self.controlbit
        byte_array[self.bytepos] |= byte

class AttrByteEnum(AttrByte):
    def __init__(self, name, bytepos, mask=None, controlbit=None, values=None):
        byte_to_val = dict((b, i) for (b, i, _name) in values)
        val_to_byte = dict((i, b) for (b, i) in byte_to_val.items())
        super().__init__(name,
                         bytepos,
                         mask=mask,
                         controlbit=controlbit,
                         to_byte=val_to_byte.get,
                         of_byte=byte_to_val.get)
        self._values = values or []
        self._value_names = dict((i, name) for (_b, i, name) in self._values)

    def __str__(self):
        s = super().__str__()
        if self.value is None:
            return s
        return '%s (%s)' % (s, self._value_names[self.value])

class AttrAggregateEnum(AttrBase):
    def __init__(self, name, components, values=None):
        self._components = components
        self._values = values or []
        self._component_value_to_value = { k: v for (k, v, _name) in self._values }
        self._value_to_component_value = { v: k for (k, v, _name) in self._values }
        self._value_names = { v: name for (_k, v, name) in self._values }
        super().__init__(name)

    def __str__(self):
        s = super().__str__()
        if self.value is None:
            return s
        return '%s (%s)' % (s, self._value_names[self.value])

    @property
    def value(self):
        values = tuple([c.value for c in self._components])
        for (k, v, _name) in self._values:
            if all(k_i is None or k_i == values[i] for i, k_i in enumerate(k)):
                return v
        return None

    @value.setter
    def value(self, value):
        if value is None:
            for c in self._components:
                c.set(None)
            return
        for (k, v, _name) in self._values:
            if v == value:
                for i, c_value in enumerate(k):
                    self._components[i].set(c_value)
                return
        raise ValueError(f"{repr(value)} isn't a valid value for {self.name}")

    def set_from_bytes(self, byte_array):
        for component in self._components:
            component.set_from_bytes(byte_array)
        
    def apply(self, byte_array, is_control=None):
        for component in self._components:
            component.apply(byte_array, is_control=is_control)

class Settings(object):
    def __init__(self, aircon_id):
        self.aircon_id = aircon_id
        self.on_off = AttrByte('On/off',
                               2,
                               mask=3,
                               controlbit=2,
                               of_byte=lambda b: b == 1,
                               to_byte=lambda v: 1 if v else 0)

        self.preset_temp = AttrByte('Preset temperature',
                                    4,
                                    controlbit=128,
                                    of_byte=lambda b: float(b)/2.0,
                                    to_byte=lambda v: int(v*2))
    
        self.op_mode = AttrByteEnum('Operation Mode',
                                    2,
                                    mask=60,
                                    controlbit=32,
                                    values=[
                                        (0, 0, "Auto"),
                                        (8, 1, "Cool"),
                                        (16, 2, "Heat"),
                                        (12, 3, "Fan"),
                                        (4, 4, "Dry")])
    
        self.airflow = AttrByteEnum('Airflow',
                                    3,
                                    mask=15,
                                    controlbit=8,
                                    values=[
                                        (7, 0, "Auto"),
                                        (0, 1, "|"),
                                        (1, 2, "||"),
                                        (2, 3, "|||"),
                                        (6, 4, "||||")])
    
        self.entrust = AttrByteEnum('3D Auto',
                                    12,
                                    mask=12,
                                controlbit=8,
                                    values=[
                                        (0, 0, "Off"),
                                        (4, 1, "On")])

        self.model_no = AttrByte('Model Number',
                                 0,
                                 mask=127)

        self.cool_hot_judge = AttrByte('Cool Hot Judge(?)',
                                       8,
                                       mask=8,
                                       of_byte=lambda b: 0 if b <=0 else 1)

        self.vacant_property = AttrByte('Vacant Property',
                                        10,
                                        mask=1)

        self.self_clean = AttrByte('Self clean',
                                   15,
                                   mask=15)

        self.wind_dir_ud = AttrAggregateEnum('Wind Direction (Up/Down)',
                                             [ AttrByte('wind_ud_auto',
                                                        2,
                                                        mask=192,
                                                        controlbit=128),
                                               AttrByte('wind_ud_pos',
                                                        3,
                                                        mask=240,
                                                        controlbit=128)
                                             ],
                                             values=[
                                                 ((64, None), 0, 'auto'),
                                                 ((0, 0), 1, '1'),
                                                 ((0, 16), 2, '2'),
                                                 ((0, 32), 3, '3'),
                                                 ((0, 48), 4, '4'),
                                             ])

        self.wind_dir_lr = AttrAggregateEnum('Wind Direction (Left/Right)',
                                             [ AttrByte('wind_lr_auto',
                                                        12,
                                                        mask=3,
                                                        controlbit=2),
                                               AttrByte('wind_lr_pos',
                                                        11,
                                                        mask=31,
                                                        controlbit=16)
                                             ],
                                             values=[
                                                 ((1, None), 0, 'auto'),
                                                 ((0, 0), 1, '1'),
                                                 ((0, 1), 2, '2'),
                                                 ((0, 2), 3, '3'),
                                                 ((0, 3), 4, '4'),
                                                 ((0, 4), 5, '5'),
                                                 ((0, 5), 6, '6'),
                                                 ((0, 6), 7, '7'),
                                             ])

        self._attributes = [
            'on_off',
            'preset_temp',
            'op_mode',
            'airflow',
            'entrust',
            'model_no',
            'cool_hot_judge',
            'vacant_property',
            'self_clean',
            'wind_dir_ud',
            'wind_dir_lr'
        ]
        
    def __str__(self):
        return '\n'.join('  %s' % (getattr(self, k)) for k in self._attributes)
        
    def set_from_bytes(self, byte_array):
        for attr in self._attributes:
            getattr(self, attr).set_from_bytes(byte_array)

    def to_bytes(self):
        byte_array = []
        for is_control in [True, False]:
            buf = [0] * 18
            buf[5] = 255
            for attr in self._attributes:
                getattr(self, attr).apply(buf, is_control=is_control)
            # TODO: in the app code, if modelno == 1, these trailing
            # bytes of the 'command' data are set based on the
            # "HomeLeaveMode" settings
            buf += [1, 255, 255, 255, 255]
            byte_array += buf + self.crc(buf)
        
        return byte_array


    def crc(self, byte_array):
        i = 65535
        for b in byte_array:
            for i2 in range(0, 8):
                z = True
                z2 = ((b >> (7 - i2)) & 1) == 1
                if ((i >> 15) & 1) != 1:
                    z = False
                i <<= 1
                if z2 ^ z:
                    i ^= 4129
        i = i & 65535
        return [ i & 255, (i >> 8) & 255 ]
    
def call_aircon_command(aircon_ip, command, contents=None):
    url = f"http://{aircon_ip}:51443/beaver/command/{command}"
    data = {
        "apiVer": "1.0",
        "command": command,
        "deviceId": MY_DEVICE_ID,
        "operatorId": MY_OPERATOR_ID,
        "timestamp": int(time.time())
    }
    if contents:
        data['contents'] = contents
    
    print("posting to %r" % url)
    print("data: %r" % data)
    
    response = requests.post(url, json=data)
    if response:
        response = response.json()

    print("response: %r" % response)
    
    if not response or response.get('result', None) != 0:
        raise Exception("Call to %s failed" % url)
    return response
    
def get_status(args):
    r = call_aircon_command(
        args.IP,
        'getAirconStat',
        contents={ "airconId": 'unused-but-required' })

    #print("Got response:\n" + json.dumps(r, indent=2))
    blob = base64.b64decode(r['contents']['airconStat'])

    #print(repr(blob))
    #print(len(blob))
    
    offset = blob[18] * 4 + 21
    #print(offset)
    end = offset + 18

    chunk1 = blob[offset:end]  # r5

    #print(repr(chunk1))
    
    offset += 19
    end = len(blob) - 2
    
    chunk2 = blob[offset:end]  # r1

    settings = Settings(r['contents']['airconId'])
    settings.set_from_bytes(chunk1)

    print(settings)

    def print_hex(bs):
        print(' '.join('%02x' % b for b in bs))

    v = chunk1[6] & 127
    if v == 0:
        error_code = "00"
    elif chunk1[6] & 128 <= 0:
        error_code = "M%02d" % int(v)
    else:
        error_code = "E%s" % str(v)
        
    print("Error code: %r" % error_code)


    p = 0
    while (len(chunk2) / 4) > p:
        y = p * 4
        p += 1
        v1 = chunk2[y]   # r12
        v2 = chunk2[y+1] # r4
        v3 = chunk2[y+2] # r3
        v4 = chunk2[y+3] # r11
        if v1 == 128 and v2 == 16:
            outdoor_temp = OUTDOOR_TEMPS[v3 & 255]
            print("Outdoor Temp: %r" % outdoor_temp)
        else:
            if v1 == 128 and v2 == 32:
                indoor_temp = INDOOR_TEMPS[v3 & 255]
                print("Indoor Temp: %r" % indoor_temp)
            else:
                if v1 == 148 and v2 == 16:
                    electric = float((v4 & 255) << 8 + (v3 & 255)) * 0.25
                    print("Electric: %r" % electric)
                else:
                    home_leave_mode_for_cooling = 0
                    home_leave_mode_for_heating = 0
                    if v1 == 248 and v2 == 16:
                        if v3 == 27:
                            home_leave_cooling_temp_rule = v4 / 2.0
                        elif v3 == 28:
                            home_leave_heating_temp_rule = v4 / 2.0
                        elif v3 == 29:
                            home_leave_cooling_temp_setting = v4 / 2.0
                        elif v3 == 30:
                            home_leave_heating_temp_setting = v4 / 2.0
                        elif v3 == 31:
                            home_leave_cooling_air_flow = get_home_leave_mode_air_flow(v4 & 15)
                        elif v3 == 32:
                            home_leave_heating_air_flow = get_home_leave_mode_air_flow(v4 & 15)

    return settings

def set_status(args):
    settings = get_status(args)
    print(f"Current settings:\n{settings}")

    for arg, setting in [
            (args.temperature, settings.preset_temp),
            (args.on_off, settings.on_off),
            (args.airflow, settings.airflow),
            (args.wind_ud, settings.wind_dir_ud),
            (args.wind_lr, settings.wind_dir_lr),
            ]:
        if arg is not None:
            setting.set(arg)
    
    print(f"New settings:\n{settings}")
    
    payload = base64.b64encode(bytes(settings.to_bytes())).decode('utf-8')
    
    r = call_aircon_command(
        args.IP,
        'setAirconStat',
        contents={
            "airconId": settings.aircon_id,
            "airconStat": payload,
        })

    blob = base64.b64decode(r['contents']['airconStat'])

    offset = blob[18] * 4 + 21
    end = offset + 18

    updated_settings = Settings(r['contents']['airconId'])
    updated_settings.set_from_bytes(blob[offset:end])

    print(f"Updated settings:\n{updated_settings}")    

def register_with_aircon(aircon_id, aircon_ip):
    r = call_aircon_command(
        aircon_ip,
        'updateAccountInfo',
        contents={
            "accountId": MY_OPERATOR_ID,
            "airconId": aircon_id,
            "remote": 0,
            "timezone": TIMEZONE
        })

    if r['result'] == 0:
        print("Registered successfully")
    else:
        print(f"FAILED! Result = {r['result']}")


def register(args):
    info = get_device_info(args.IP)
    
    r = register_with_aircon(info['airconId'], args.IP)

    print(repr(r))
    
   
def get_device_info(aircon_ip):
    response = call_aircon_command(aircon_ip, 'getDeviceInfo')

    return response['contents']

def get_info(args):
    r = get_device_info(args.IP)
    print("Aircon ID: %r" % r['airconId'])
    print("Aircon MAC: %r" % r['macAddress'])


    
def find_devices(args):
    from zeroconf import Zeroconf, ServiceStateChange, ServiceBrowser
    from typing import cast
    def on_service_state_change(
            zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
    ) -> None:
        if state_change is ServiceStateChange.Added:
            info = zc.get_service_info(service_type, name)
            if info:
                addrs = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
                print(f"Server: {info.server}")
                print("Weight: %d, priority: %d" % (info.weight, info.priority))
                print("Addresses: %s" % (' '.join(addrs)))
                print()
    
    zc = Zeroconf()
    browser = ServiceBrowser(zc, ['_beaver._tcp.local.'], handlers=[on_service_state_change])
    until = time.time() + args.timeout
    try:
        while time.time() < until:
            time.sleep(0.1)
    finally:
        zc.close()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subs = parser.add_subparsers()

    p_info = subs.add_parser('info', help="Get aircon device info (ID/MAC address)")
    p_info.add_argument('IP', help="Aircon device IP")
    p_info.set_defaults(func=get_info)

    p_status = subs.add_parser('status', help="Get aircon status")
    p_status.add_argument('IP', help="Aircon device IP")
    p_status.set_defaults(func=get_status)

    p_reg = subs.add_parser('register', help="Register with aircon device")
    p_reg.add_argument('IP', help="Aircon device IP")
    p_reg.set_defaults(func=register)

    p_find = subs.add_parser('find', help="Find aircon devices")
    p_find.add_argument('--timeout', type=float, default=2.0, help="How long to wait (seconds)")
    p_find.set_defaults(func=find_devices)

    p_set = subs.add_parser('set', help="Set aircon settings")
    p_set.add_argument('IP', help="Aircon device IP")
    p_set.add_argument('--on', dest='on_off', action='store_true')
    p_set.add_argument('--off', dest='on_off', action='store_false')
    p_set.add_argument('--temp', dest='temperature', type=float)
    p_set.add_argument('--airflow', dest='airflow', type=int, choices=[0,1,2,3,4])
    p_set.add_argument('--wind-ud', dest='wind_ud', type=int, choices=[0,1,2,3,4])
    p_set.add_argument('--wind-lr', dest='wind_lr', type=int, choices=[0,1,2,3,4,5,6,7])
    p_set.set_defaults(on_off=None, func=set_status)
    
    args = parser.parse_args()
    args.func(args)
    
