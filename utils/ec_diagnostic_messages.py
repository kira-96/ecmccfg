#!/usr/bin/env python3
'''
ec_diagnostic_messages.py

read diagnostic messages from EtherCAT slaves.
usage:
    ./ec_diagnostic_messages.py [-m MASTERID] [-s SLAVEID]

example:
    ./ec_diagnostic_messages.py -s2

reads all diagnostic messages from EtherCAT slave 2 on master 0

---
Author: Felix Maier (felix.maier@psi.ch)
Date: March 27, 2025
'''

# pylint: disable-msg=C0103
# vim: ts=4 sw=4 et
import argparse
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta

MSG_LUT = {
    # default applies to all devices, can be overwritten by key of device
    (0x0, 0x0): {
        0x0001: "No error",
        0x0002: "Communication established",
        0x0003: "Initialization: 0x%X, 0x%X, 0x%X",
        0x1000: "Information: 0x%X, 0x%X, 0x%X",
        0x4000: "Warning: 0x%X, 0x%X, 0x%X",
        0x8001: "Error: 0x%X, 0x%X, 0x%X",
        0x8201: "No communication to field-side (Auxiliary voltage missing)",
        0xFFFF: "Debug: 0x%X, 0x%X, 0x%X",
    },

    # ['EL5001', 'EL5001-0010', 'EL5001-0011', 'EL5001-0012', 'EL5001-0090']
    (0x2, 0x13893052): {
        0x1303: "Encoder Supply ok",
        0x8350: "Data Length Mismatch (Channel %d, Expect: %d, Received: %d)",
    },

    # ['EL5031-0011']
    (0x2, 0x13a73052): {
        0x1303: "Encoder Supply ok",
        0x1304: "Encoder initialization successfully, channel: %X",
        0x1305: "Sent command encoder reset, channel: %X",
        0x8303: "Encoder supply error",
        0x8304: "Encoder communication error, channel: %X",
        0x8305: "EnDat2.2 is not supported, channel: %X",
        0x8306: "Delay time, tolerance limit exceeded, 0x%X, channel: %X",
        0x8307: "Delay time, maximum value exceeded, 0x%X, channel: %X",
        0x8308: "Unsupported ordering designation, 0x%X, channel: %X (only 02 and 22 is supported)",
        0x8309: "Encoder CRC error, channel: %X",
        0x830A: "Temperature %X could not be read, channel: %X",
        0x830B: "Oversampling error, channel: %X",
    },

    # ['EL5032', 'EL5032-0090']
    (0x2, 0x13a83052): {
        0x1303: "Encoder Supply ok",
        0x1304: "Encoder initialization successfully, channel: %X",
        0x1305: "Sent command encoder reset, channel: %X",
        0x8303: "Encoder supply error",
        0x8304: "Encoder communication error, channel: %X",
        0x8305: "EnDat2.2 is not supported, channel: %X",
        0x8306: "Delay time, tolerance limit exceeded, 0x%X, channel: %X",
        0x8307: "Delay time, maximum value exceeded, 0x%X, channel: %X",
        0x8308: "Unsupported ordering designation, 0x%X, channel: %X (only 02 and 22 is supported)",
        0x8309: "Encoder CRC error, channel: %X",
        0x830A: "Temperature %X could not be read, channel: %X",
    },

    # ['EL5042']
    (0x2, 0x13b23052): {
        0x1303: "Encoder Supply ok",
        0x1304: "Encoder initialization successfully, channel: %X",
        0x8302: "general encoder error, channel: %X",
        0x8303: "Encoder supply error",
        0x8304: "Encoder communication error, channel: %X",
        0x830B: "Encoder Watchdog Error, channel: %X",
        0x830C: "Encoder Single-Cycle-Data Error, channel: %X",
    },

    # ['EL5072']
    (0x2, 0x13d03052): {
        0x117F: "Information: 0x%X",
        0x417F: "Warning: 0x%X",
        0x470E: "Overtemprature in device %d°C",
        0x8003: "Configuration error: 0x%X",
        0x8104: "Error: allowed temprature exeeded",
        0x810B: "Supply voltage Up too low or missing",
        0x817F: "Error: 0x%X",
        0x8581: "Wire broken Ch %d",
        0x8613: "Overload detected Ch %d, excitation voltage off",
        0x8623: "Short circuit detected Ch %d, excitation voltage off",
        0x8624: "Overload current Ch 1 + Ch 2 detected, excitation voltage off",
        0x8706: "Channel %d saturation",
        0x8707: "Channel %d overload",
        0x870A: "Channel %d range error",
        0x4101: "Overtemperature in device %d°C",
    },

    # ['EL5102']
    (0x2, 0x13ee3052): {
        0x4302: "Maximum frequency of the input signal is nearly reached (channel %d)",
        0x4303: "Limit counter value was reduced because of the PDO configuration (channel %d)",
        0x4304: "Reset counter value was reduced because of the PDO configuration (channel %d)",
        0x817F: "Internal hardware error (%d)",
        0x8303: "Encoder power missing (channel %d)",
        0x8310: "Initialisation error",
        0x8311: "Maximum frequency of the input signal is exceeded (channel %d)",
        0x8312: "Encoder plausibility error (channel %d)",
        0x8313: "Configuration error (channel %d)",
        0x8314: "Synchronisation error",
        0x8315: "Error status input (channel %d)",
        0x831B: "Open circuit or short circuit track A (channel %d)",
        0x831C: "Open circuit or short circuit track B (channel %d)",
        0x831D: "Open circuit or short circuit track C (channel %d)",
    },

    # ['EL5112']
    (0x2, 0x13f83052): {
        0x4302: "Maximum frequency of the input signal is nearly reached (channel %d)",
        0x4303: "Limit counter value was reduced because of the PDO configuration (channel %d)",
        0x4304: "Reset counter value was reduced because of the PDO configuration (channel %d)",
        0x817F: "Internal hardware error (%d)",
        0x8303: "Encoder power missing (channel %d)",
        0x8310: "Initialisation error",
        0x8311: "Maximum frequency of the input signal is exceeded (channel %d)",
        0x8312: "Encoder plausibility error (channel %d)",
        0x8313: "Configuration error (channel %d)",
        0x8314: "Synchronisation error",
        0x8315: "Error status input (channel %d)",
        0x831B: "Open circuit or short circuit track A (channel %d)",
        0x831C: "Open circuit or short circuit track B (channel %d)",
        0x831D: "Open circuit or short circuit track C (channel %d)",
    },

    # ['EL5122']
    (0x2, 0x14023052): {
        0x4302: "Maximum frequency of the input signal is nearly reached (channel %d)",
        0x4303: "Limit counter value was reduced because of the PDO configuration (channel %d)",
        0x4304: "Reset counter value was reduced because of the PDO configuration (channel %d)",
        0x817F: "Internal hardware error (%d)",
        0x8303: "Encoder power missing (channel %d)",
        0x8310: "Initialisation error",
        0x8311: "Maximum frequency of the input signal is exceeded (channel %d)",
        0x8312: "Encoder plausibility error (channel %d)",
        0x8313: "Configuration error (channel %d)",
        0x8314: "Synchronisation error",
        0x8315: "Error status input (channel %d)",
        0x831B: "Open circuit or short circuit track A (channel %d)",
        0x831C: "Open circuit or short circuit track B (channel %d)",
        0x831D: "Open circuit or short circuit track C (channel %d)",
    },

    # ['EL5131']
    (0x2, 0x140b3052): {
        0x4302: "Maximum frequency of the input signal is nearly reached (channel %d)",
        0x4303: "Limit counter value was reduced because of the PDO configuration (channel %d)",
        0x4304: "Reset counter value was reduced because of the PDO configuration (channel %d)",
        0x817F: "Internal hardware error (%d)",
        0x8303: "Encoder power missing (channel %d)",
        0x8310: "Initialisation error",
        0x8311: "Maximum frequency of the input signal is exceeded (channel %d)",
        0x8312: "Encoder plausibility error (channel %d)",
        0x8313: "Configuration error (channel %d)",
        0x8314: "Synchronisation error",
        0x8315: "Error status input (channel %d)",
        0x8318: "Error output (channel %d, output %d)",
        0x8319: "Error PDOs for threshold base not active (channel %d, output %d)",
        0x831B: "Open circuit or short circuit track A (channel %d)",
        0x831C: "Open circuit or short circuit track B (channel %d)",
        0x831D: "Open circuit or short circuit track C (channel %d)",
    },

    # Beckhoff EL7041
    (0x2, 0x1b813052): {
        0x1100: "Detection of operation mode completed: 0x%X, %d",
        0x1135: "Cycle time o.k.: %d",
        0x1201: "Communication re-established",
        0x1300: "Position set: %d, %d",
        0x1400: "Drive is calibrated: %d, %d",
        0x1401: "Actual drive state: 0x%X, %d",
        0x4101: "Terminal-Overtemperature",
        0x4300: "Subincrements deactivated: %d, %d",
        0x4301: "Encoder-Warning",
        0x4400: "Drive is not calibrated: %d, %d",
        0x4401: "Starttype not supported: 0x%X, %d",
        0x4402: "Command rejected: %d, %d",
        0x4403: "Maximum position lag exceeded (%d): channel %d",
        0x4405: "Invalid modulo subtype: %d, %d",
        0x4410: "Target overrun: %d, %d",
        0x4411: "DC-Link undervoltage",
        0x4412: "DC-Link overvoltage",
        0x4413: "I2T Amplifier overload",
        0x4414: "I2T Motor overload",
        0x4415: "Speed limitation active",
        0x4416: "Step lost detected at position: 0x%X%X",
        0x8002: "Communication aborted",
        0x8003: "Configuration error: 0x%X, 0x%X, 0x%X",
        0x8100: "Status word set: 0x%X, %d",
        0x8101: "Operation mode incompatible to PDO interface: 0x%X, %d",
        0x8102: "Invalid combination of Inputs and Outputs PDOs",
        0x8104: "Terminal-Overtemperature",
        0x8105: "PD-Watchdog",
        0x8135: "Large cycle time: %d",
        0x8200: "Write access error: %d, %d",
        0x82FF: "Bootmode not activated",
        0x8300: "Set position error: 0x%X, %d",
        0x8301: "Encoder increments not configured: 0x%X, %d",
        0x8302: "Encoder-Error",
        0x8400: "Incorrect drive configuration: 0x%X, %d",
        0x8401: "Limiting of calibration velocity: %d, %d",
        0x8402: "Emergency stop activated: 0x%X, %d",
        0x8403: "ADC Error",
        0x8404: "Overcurrent",
        0x8405: "Invalid modulo position: %d",
        0x8406: "Undervoltage DC-Link",
        0x8407: "Overvoltage DC-Link",
        0x8408: "I2T-Model Amplifier overload",
        0x8409: "I2T-Model motor overload",
        0x8415: "Invalid modulo factor: %d",
        0x8440: "Motor cable not connected",
    },

    # ['EL7201', 'EL7201-0001', 'EL7201-0010', 'EL7201-0011', 'EL7201-9014', 'EL7201-9015']
    (0x2, 0x1c213052): {
        0x1201: "Communication re-established",
        0x4101: "Terminal-Overtemperature",
        0x4301: "Encoder-Warning",
        0x4411: "DC-Link undervoltage",
        0x4412: "DC-Link overvoltage",
        0x4413: "I2T Amplifier overload",
        0x4414: "I2T Motor overload",
        0x4415: "Speed limitation active",
        0x8002: "Communication aborted",
        0x8003: "Configuration error: 0x%X, 0x%X, 0x%X",
        0x8102: "Invalid combination of Inputs and Outputs PDOs",
        0x8103: "No variable linkage",
        0x8104: "Terminal-Overtemperature",
        0x8105: "PD-Watchdog",
        0x8135: "Cycletime has to be a multiple of 125 µs",
        0x8302: "Encoder-Error",
        0x8403: "ADC Error",
        0x8404: "Overcurrent",
        0x8406: "Undervoltage DC-Link",
        0x8407: "Overvoltage DC-Link",
        0x8408: "I2T-Model Amplifier overload",
        0x8409: "I2T-Model motor overload",
        0x4102: "Discrepancy in the PDO-Configuration",
        0x4418: "Limit: Current",
        0x4419: "Limit: Amplifier I2T-model exceeds 100%%",
        0x441A: "Limit: Motor I2T-model exceeds 100%%",
        0x441B: "Limit: Velocity limitation",
        0x8417: "Maximum rotating field velocity exceeded",
        0x4417: "Motor-Overtemperature",
        0x8137: "Electronic name plate: CRC error",
        0x8416: "Motor-Overtemperature",
        0x441C: "Voltage on STO-Input missing",
        0x441D: "Interner Hardwarefehler",
        0x8304: "OCT communication error",
        0x841C: "STO while the axis was enabled",
        0x841D: "Internal hardware error",
        0x840B: "Motor error or commutation malfunction",
        0x840C: "Phase failure",
        0x4420: "Cogging compensation not supported (%u)",
        0x8146: "Sync-Mode and PDO-Configuration are not compatible",
        0x8441: "Following error",
        0x8450: "Invalid start type 0x%x",
        0x8451: "Invalid limit switch level",
        0x8452: "Drive error during positioning",
        0x8453: "Latch unit will be used by multiple modules",
        0x8454: "Drive not in control",
        0x8455: "Invalid value for Target acceleration",
        0x8456: "Invalid value for Target deceleration",
        0x8457: "Invalid value for Target velocity",
        0x8458: "Invalid value for Target position",
        0x8459: "Emergency stop active",
        0x845A: "Target position exceeds Modulofactor",
        0x845B: "Drive must be disabled",
        0x845C: "No Feedback found",
        0x845D: "Modulo factor invalid",
        0x845E: "Invalid target position window",
        0x8145: "Sync-Mode and PDO-Configuration are not compatible",
    },

    # ['EL7211', 'EL7211-0001', 'EL7211-0010', 'EL7211-0011']
    (0x2, 0x1c2B3052): {
        0x1201: "Communication re-established",
        0x4101: "Terminal-Overtemperature",
        0x4301: "Encoder-Warning",
        0x4411: "DC-Link undervoltage",
        0x4412: "DC-Link overvoltage",
        0x4413: "I2T Amplifier overload",
        0x4414: "I2T Motor overload",
        0x4415: "Speed limitation active",
        0x8002: "Communication aborted",
        0x8003: "Configuration error: 0x%X, 0x%X, 0x%X",
        0x8102: "Invalid combination of Inputs and Outputs PDOs",
        0x8103: "No variable linkage",
        0x8104: "Terminal-Overtemperature",
        0x8105: "PD-Watchdog",
        0x8135: "Cycletime has to be a multiple of 125 µs",
        0x8302: "Encoder-Error",
        0x8403: "ADC Error",
        0x8404: "Overcurrent",
        0x8406: "Undervoltage DC-Link",
        0x8407: "Overvoltage DC-Link",
        0x8408: "I2T-Model Amplifier overload",
        0x8409: "I2T-Model motor overload",
        0x4102: "Discrepancy in the PDO-Configuration",
        0x4418: "Limit: Current",
        0x4419: "Limit: Amplifier I2T-model exceeds 100%%",
        0x441A: "Limit: Motor I2T-model exceeds 100%%",
        0x441B: "Limit: Velocity limitation",
        0x8417: "Maximum rotating field velocity exceeded",
        0x4417: "Motor-Overtemperature",
        0x8137: "Electronic name plate: CRC error",
        0x8416: "Motor-Overtemperature",
    },

    # ['EL7211-0010', 'EL7211-0011', 'EL7211-9014', 'EL7211-9015']
    (0x2, 0x1c2b3052): {
        0x1201: "Communication re-established",
        0x4101: "Terminal-Overtemperature",
        0x4102: "Discrepancy in the PDO-Configuration",
        0x4301: "Feedback-Warning",
        0x4411: "DC-Link undervoltage",
        0x4412: "DC-Link overvoltage",
        0x4413: "I2T Amplifier overload",
        0x4414: "I2T Motor overload",
        0x4415: "Speed limitation active",
        0x4417: "Motor-Overtemperature",
        0x4418: "Limit: Current",
        0x4419: "Limit: Amplifier I2T-model exceeds 100%%",
        0x441A: "Limit: Motor I2T-model exceeds 100%%",
        0x441B: "Limit: Velocity limitation",
        0x441C: "Voltage on STO-Input missing",
        0x441D: "Interner Hardwarefehler",
        0x8002: "Communication aborted",
        0x8003: "Configuration error: 0x%X, 0x%X, 0x%X",
        0x8102: "Invalid combination of Inputs and Outputs PDOs",
        0x8103: "No variable linkage",
        0x8104: "Terminal-Overtemperature",
        0x8105: "PD-Watchdog",
        0x8135: "Cycletime has to be a multiple of 125 µs",
        0x8137: "Electronic name plate: CRC error",
        0x8302: "Feedback-Error",
        0x8304: "OCT communication error",
        0x8403: "ADC Error",
        0x8404: "Overcurrent",
        0x8406: "Undervoltage DC-Link",
        0x8407: "Overvoltage DC-Link",
        0x8408: "I2T-Model Amplifier overload",
        0x8409: "I2T-Model motor overload",
        0x8416: "Motor-Overtemperature",
        0x8417: "Maximum rotating field velocity exceeded",
        0x841C: "STO while the axis was enabled",
        0x841D: "Internal hardware error",
        0x840B: "Motor error or commutation malfunction",
        0x840C: "Phase failure",
        0x4420: "Cogging compensation not supported (%u)",
        0x8146: "Sync-Mode and PDO-Configuration are not compatible",
        0x8441: "Following error",
        0x8450: "Invalid start type 0x%x",
        0x8451: "Invalid limit switch level",
        0x8452: "Drive error during positioning",
        0x8453: "Latch unit will be used by multiple modules",
        0x8454: "Drive not in control",
        0x8455: "Invalid value for Target acceleration",
        0x8456: "Invalid value for Target deceleration",
        0x8457: "Invalid value for Target velocity",
        0x8458: "Invalid value for Target position",
        0x8459: "Emergency stop active",
        0x845A: "Target position exceeds Modulofactor",
        0x845B: "Drive must be disabled",
        0x845C: "No Feedback found",
        0x845D: "Modulo factor invalid",
        0x845E: "Invalid target position window",
        0x8145: "Sync-Mode and PDO-Configuration are not compatible",
    },

    # ['EL7221', 'EL7221-0001', 'EL7221-9014', 'EL7221-9015']
    (0x2, 0x1c353052): {
        0x1201: "Communication re-established",
        0x4101: "Terminal-Overtemperature",
        0x4102: "Discrepancy in the PDO-Configuration",
        0x4301: "Encoder-Warning",
        0x4411: "DC-Link undervoltage",
        0x4412: "DC-Link overvoltage",
        0x4413: "I2T Amplifier overload",
        0x4414: "I2T Motor overload",
        0x4415: "Speed limitation active",
        0x4418: "Limit: Current",
        0x4419: "Limit: Amplifier I2T-model exceeds 100%%",
        0x441A: "Limit: Motor I2T-model exceeds 100%%",
        0x441B: "Limit: Velocity limitation",
        0x8002: "Communication aborted",
        0x8003: "Configuration error: 0x%X, 0x%X, 0x%X",
        0x8102: "Invalid combination of Inputs and Outputs PDOs",
        0x8103: "No variable linkage",
        0x8104: "Terminal-Overtemperature",
        0x8105: "PD-Watchdog",
        0x8135: "Cycletime has to be a multiple of 125 µs",
        0x8302: "Encoder-Error",
        0x8403: "ADC Error",
        0x8404: "Overcurrent",
        0x8406: "Undervoltage DC-Link",
        0x8407: "Overvoltage DC-Link",
        0x8408: "I2T-Model Amplifier overload",
        0x8409: "I2T-Model motor overload",
        0x8417: "Maximum rotating field velocity exceeded",
        0x4417: "Motor-Overtemperature",
        0x441C: "Voltage on STO-Input missing",
        0x441D: "Interner Hardwarefehler",
        0x8137: "Electronic name plate: CRC error",
        0x8304: "OCT communication error",
        0x840B: "Motor error or commutation malfunction",
        0x840C: "Phase failure",
        0x8416: "Motor-Overtemperature",
        0x841C: "STO while the axis was enabled",
        0x841D: "Internal hardware error",
        0x4420: "Cogging compensation not supported (%u)",
        0x8146: "Sync-Mode and PDO-Configuration are not compatible",
        0x8441: "Following error",
        0x8450: "Invalid start type 0x%x",
        0x8451: "Invalid limit switch level",
        0x8452: "Drive error during positioning",
        0x8453: "Latch unit will be used by multiple modules",
        0x8454: "Drive not in control",
        0x8455: "Invalid value for Target acceleration",
        0x8456: "Invalid value for Target deceleration",
        0x8457: "Invalid value for Target velocity",
        0x8458: "Invalid value for Target position",
        0x8459: "Emergency stop active",
        0x845A: "Target position exceeds Modulofactor",
        0x845B: "Drive must be disabled",
        0x845C: "No Feedback found",
        0x845D: "Modulo factor invalid",
        0x845E: "Invalid target position window",
        0x8145: "Sync-Mode and PDO-Configuration are not compatible",
    },
}

# configure diagnostic sdos
SDO_MAX_MSG = {"index": "0x10f3", "subindex": "0x01", "type": "uint8"}
SDO_START_MSG = {"index": "0x10f3", "subindex": "0x06", "type": "octet_string"}
SDO_DEVICE_NAME = {"index": "0x1008", "subindex": "0x00", "type": "string"}
SDO_VENDOR_ID = {"index": "0x1018", "subindex": "0x01", "type": "uint32"}
SDO_PRODUCT_CODE = {"index": "0x1018", "subindex": "0x02", "type": "uint32"}


class ReadDiagMessage:

    def __init__(self):
        self.id_master = 0
        self.id_slave = 1
        self.messages = list()
        self.device_name = ""
        self.device_vendor_id = 0
        self.device_product_code = 0


    def run(self, master_id, slave_id):
        self.id_master = master_id
        self.id_slave = slave_id
        self.read_device_information()
        self.print_device_information()
        self.read_diag_messages()

        # sort messages by time
        self.messages = sorted(self.messages, key=lambda x: x['time'])

        self.print_diagnostic_messages()

    def getNumberFromRespond(self, respond, datatype):
        respond = respond.decode()

        regex = ""
        base_system = 0
        if datatype == "int":
            regex = re.compile(r'(\d+)$')
            base_system = 10
        if datatype == "hex":
            regex = re.compile(r'^(0x[a-zA-Z0-9]+)')
            base_system = 16

        match = regex.search(respond)
        if match is None:
            sys.exit("error: cannot find " + datatype + " part in respond")

        return int(match.group(), base=base_system)


    def read_device_information(self):
        self.device_name = self.read_sdo(SDO_DEVICE_NAME)
        self.device_vendor_id = self.read_sdo(SDO_VENDOR_ID)
        self.device_vendor_id = self.getNumberFromRespond(self.device_vendor_id, "hex")
        self.device_product_code = self.read_sdo(SDO_PRODUCT_CODE)
        self.device_product_code = self.getNumberFromRespond(self.device_product_code, "hex")


    def read_diag_messages(self):
        max_msg_no = self.getNumberFromRespond(self.read_sdo(SDO_MAX_MSG), "int")

        # read messages
        start_index = int(SDO_START_MSG['subindex'], base=16) # hex to int
        for idx in range(start_index, start_index + max_msg_no):
            sdo = SDO_START_MSG
            sdo["subindex"] = hex(idx)
            readMsg = self.read_sdo(sdo)

            if self.is_none_empty_msg(readMsg) is True:
                msg = self.decode_diag_msg((idx-start_index+1), readMsg)
                msg["text"] = self.decode_text_id(msg["text_id"])
                self.messages.append(msg)


    def read_sdo(self, sdo):
        command = "ethercat -m" + str(self.id_master)
        command += " -p" + str(self.id_slave)
        command += " --type " + sdo["type"]
        command += " upload " + sdo["index"] + " " + sdo["subindex"]

        try:
            return subprocess.check_output(command, shell=True)
        except:
            sys.exit("error while calling: " + command)


    def is_none_empty_msg(self, msg):
        is_none_empty = False
        for byte in msg:
            if byte != 0:
                is_none_empty = True
                break

        return is_none_empty


    def decode_diag_msg(self, msg_no, raw_msg):
        return {
            "msg_no":    msg_no,
            "diag_code": hex(int.from_bytes(raw_msg[0:4], byteorder='little')),
            "flags":     hex(int.from_bytes(raw_msg[4:6], byteorder='little')),
            "text_id":   hex(int.from_bytes(raw_msg[6:8], byteorder='little')),
            "time":      self.decode_ethercat_time(int.from_bytes(raw_msg[8:16], byteorder='little')),
            "dynamic":   hex(int.from_bytes(raw_msg[16:], byteorder='little'))
        }

    def decode_ethercat_time(self, ns):
      # dt is based on UNIX epoche 01.01.1970
        dt = datetime.fromtimestamp(ns / 1000000000)

      # days = 01.01.2000 - 01.01.1970 = 10957 days
      # hours, not sure why -1 is needed, summer/wintertime?
        dt = dt + timedelta(days=10957, hours=-1)
        return dt

    def decode_text_id(self, id):
        table = ""
        for lut_entry in MSG_LUT:
            if self.device_vendor_id == lut_entry[0]:
                prod_code = self.device_product_code
                is_in_tuple = isinstance(lut_entry[1], tuple) and prod_code in lut_entry[1]
                is_in_int = isinstance(lut_entry[1], int) and prod_code == lut_entry[1]

                if is_in_tuple or is_in_int:
                    table = MSG_LUT[(lut_entry[0], lut_entry[1])]

        id = int(id, base=16)
        assert isinstance(id, int)
        if table != "" and id in table:
            return table[id]

        if id in MSG_LUT[(0, 0)]:
            return MSG_LUT[(0, 0)][id]

        return ""

    def print_device_information(self):
        print("\nDEVICE INFORMATION:\n" + "="*19 + "\n")
        print("name:\t\t" + ((self.device_name).decode()).rstrip())
        print("master id:\t" + str(self.id_master))
        print("slave id:\t" + str(self.id_slave))
        print("vendor id:\t" + hex(self.device_vendor_id))
        print("product id:\t" + hex(self.device_product_code))
        print("host time:\t" + str(datetime.now()))

    def print_diagnostic_messages(self):

        print("\n\nDIAGNOSTIC MESSAGES:\n" + "="*20)

        # calculate width of each column ------------
        col_width = OrderedDict({"msg_no": 6, "time": 4, "text_id": 7, "text": 4,
                                 "flags": 5, "diag_code": 9, "dynamic": 7})



        for msg in self.messages:
            for key, val in msg.items():
                length = max(len(str(key)), len(str(val)))

                if length > col_width[key]:
                    col_width[key] = length

        col_width = {k: v+2 for k, v in col_width.items()}

      # print table -------------------------------
        print(self.generateTableLine(col_width, col_width, True))
        for msg in self.messages:
            print(self.generateTableLine(msg, col_width))
        print()


    def generateTableLine(self, data, col_width, useKey=False):
        line = ""
        for key, _ in col_width.items():
            if useKey:
                text = key
            else:
                text = str(data[key])
            width = col_width[key]
            line += text.ljust(width)
        return line


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(
        prog="ec_diagnostic_messages",
        usage="ec_diagnostic_messages [-h] [-m MASTERID] [-s SLAVEID]",
        description="read diagnostic messages from EtherCAT slaves")

    arg_parser.add_argument('-m', help="EtherCAT master id (default=0)", type=int, default=0)
    arg_parser.add_argument('-s', help="EtherCAT slave id (default=1)", type=int, default=1)
    arg_parser.add_argument('-v', action='version', version='ec_diagnostic_messages v1.0.0')
    ARGS = arg_parser.parse_args()

    diag_reader = ReadDiagMessage()
    diag_reader.run(ARGS.m, ARGS.s)
