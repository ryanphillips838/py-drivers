#Driver for NXP MAG3110 3 axis digital magnetometer
#Datasheet here: https://www.nxp.com/docs/en/data-sheet/MAG3110.pdf

#!/usr/bin/python

import smbus

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

class MAG3110:
    def __init__(self, port):
        self.bus = smbus.SMBus(port)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

    DEVICE_ADDRESS = 0x0E      #7 bit address (will be left shifted to add the read write bit)

    #Register Addresses
    DR_STATUS = 0x00
    OUT_X_MSB = 0x01
    OUT_X_LSB = 0x02
    OUT_Y_MSB = 0x03
    OUT_Y_LSB = 0x04
    OUT_Z_MSB = 0x05
    OUT_Z_LSB = 0x06
    WHO_AM_I  = 0x07
    SYSMOD    = 0x08
    OFF_X_MSB = 0x09
    OFF_X_LSB = 0x0A
    OFF_Y_MSB = 0x0B
    OFF_Y_LSB = 0x0C
    OFF_Z_MSB = 0x0D
    OFF_Z_LSB = 0x0E
    DIE_TEMP  = 0x0F
    CTRL_REG1 = 0x10
    CTRL_REG2 = 0x11

    def WhoAmI(self):
        return self.bus.read_byte_data(self.DEVICE_ADDRESS, self.WHO_AM_I)

    def GetSysMod(self):
        return self.bus.read_byte_data(self.DEVICE_ADDRESS, self.SYSMOD)

    def GetDataReadyStatus(self):
        return self.bus.read_byte_data(self.DEVICE_ADDRESS, self.DR_STATUS)

    def GetXAxis(self):
        msb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_X_MSB)
        lsb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_X_LSB)
        result = (msb << 8) + lsb
        return twos_comp(result, 16)

    def GetYAxis(self):
        msb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Y_MSB)
        lsb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Y_LSB)
        result = (msb << 8) + lsb
        return twos_comp(result, 16)

    def GetZAxis(self):
        msb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Z_MSB)
        lsb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Z_LSB)
        result = (msb << 8) + lsb
        return twos_comp(result, 16)

    def GetXYZAxis(self):
        msb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_X_MSB)
        lsb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_X_LSB)
        x = (((msb << 8) + lsb) ^ 0xFFFF) + 1
        msb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Y_MSB)
        lsb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Y_LSB)
        y = (((msb << 8) + lsb) ^ 0xFFFF) + 1
        msb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Z_MSB)
        lsb = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.OUT_Z_LSB)
        z = (((msb << 8) + lsb) ^ 0xFFFF) + 1
        return x, y, z

    def GetDieTemp(self):
        temp = self.bus.read_byte_data(self.DEVICE_ADDRESS, self.DIE_TEMP)
        return twos_comp(temp, 8)

    def SetCtrlReg1(self, data):
        self.bus.write_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1, data)

    def SetCtrlReg2(self, data):
        self.bus.write_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG2, data)