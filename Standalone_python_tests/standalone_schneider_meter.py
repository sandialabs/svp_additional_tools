"""
Communications to a EGX100 Gateway to the Schneider Electric PowerLogic PM800 Series Power Meters

Communications use Modbus TCP/IP
"""


import sunspec.core.modbus.client as client
import sunspec.core.util as util
import binascii
import time


def trace(msg):
    print msg

# Reg   Name            Size    Type    Access  NV  Scale   Units       Range
# 1120  Voltage, A-B    1       Integer RO      N   D       Volts/Scale 0 - 32,767 RMS Voltage measured between A & B
def readVoltageAB():
    data = device.read(1119, 1)
    voltage = util.data_to_s16(data)*(10**scaleD())
    return voltage

# Reg   Name                Size    Type    Access  NV  Scale   Units       Range
# 1140  Real Power, Phase A 1       Integer RO      N   F       kW/Scale    -32,767 to 32,767 (-32,768 if N/A)
def readPowerA():
    data = device.read(1139, 1)
    watt = util.data_to_s16(data)*(10**scaleF())
    return watt

# Reg   Name                Size    Type    Access  NV  Scale   Units       Range
# 1141  Real Power, Phase B 1       Integer RO      N   F       kW/Scale    -32,767 to 32,767 (-32,768 if N/A)
def readPowerB():
    data = device.read(1140, 1)
    watt = util.data_to_s16(data)*(10**scaleF())
    return watt

# Reg   Name                Size    Type    Access  NV  Scale   Units       Range
# 1142  Real Power, Phase C 1       Integer RO      N   F       kW/Scale    -32,767 to 32,767 (-32,768 if N/A)
def readPowerC():
    data = device.read(1141, 1)
    watt = util.data_to_s16(data)*(10**scaleF())
    return watt

# Reg   Name                Size    Type    Access  NV  Scale   Units       Range
# 1143  Real Power, Total   1       Integer RO      N   F       kW/Scale    -32,767 to 32,767 (-32,768 if N/A)
def readPower():
    data = device.read(1142, 1)
    watt = util.data_to_s16(data)*(10**scaleF())
    return watt

# Reg   Name                Size    Type    Access  NV  Scale   Units       Range
# 11736 Real Power, Total   2       Float   RO      N
def readFloatPower():
    data = device.read(11735, 2)
    watt = util.data_to_float(data)
    return watt

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 1144  Reactive Power, Phase A 1       Integer RO      N   F       kVAr/Scale  -32,767 to 32,767 (-32,768 if N/A)
def readVarsA():
    data = device.read(1143, 1)
    vars = util.data_to_s16(data)
    return vars

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 1145  Reactive Power, Phase B 1       Integer RO      N   F       kVAr/Scale  -32,767 to 32,767 (-32,768 if N/A)
def readVarsB():
    data = device.read(1144, 1)
    vars = util.data_to_s16(data)*(10**scaleF())
    return vars

# 1146 Reactive Power, Phase C 1 Integer RO N F kVAr/Scale -32,767 to 32,767 (-32,768 if N/A)
def readVarsC():
    data = device.read(1145, 1)
    vars = util.data_to_s16(data)*(10**scaleF())
    return vars

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 1147  Reactive Power, Total   1       Integer RO      N   F       kVAr/Scale  -32,767 to 32,767 (-32,768 if N/A)
def readVars():
    data = device.read(1146, 1)
    vars = util.data_to_s16(data)*(10**scaleF())
    return vars

# Reg   Name        Size    Type    Access  NV  Scale   Units   Range
# 1180  Frequency   1       Integer RO      N   xx      0.01Hz  2,300 - 6,700 (-32,768 if N/A),
# Frequency of circuits being monitored. If the frequency is out of range, the register will be -32,768.
def readHz():
    data = device.read(1179, 1)
    freq = util.data_to_u16(data)*(10**-2)
    return freq

# Reg   Name        Size    Type    Access  NV  Scale   Units       Range
# 11762 Frequency   2       Float   RO      N   -       Hz          Frequency of circuits being monitored.
def readFloatHz():
    data = device.read(11761, 2)
    freq = util.data_to_float(data)
    return freq

# Reg   Name                     Size   Type    Access  NV  Scale   Units       Range
# 11760 True Power Factor, Total 2      Float   RO      N   -       Derived using the complete harmonic content of real
#                                                                   and apparent power
def readFloatPF():
    data = device.read(11759, 2)
    pf = util.data_to_float(data)
    return pf

# 11699 (Use this as a check for the floating point activation)
def readFloatCurrentA():
    data = device.read(11699, 1)
    currA = util.data_to_s16(data)
    return currA

def enableFloats():
    device.write(7999, util.u16_to_data(9020))  # enable float values
    device.write(3247, util.u16_to_data(1))  # enable float values
    device.write(8000, util.u16_to_data(1))  # enable float values
    device.write(7999, util.u16_to_data(9021))  # enable float values

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 3209  Scale A - 3 Phase Amps  1       Integer R/CW    Y   xx      1.0         -2 to 1 Power of 10 Default = 0
def scaleA():
    data = device.read(3208, 1)
    return util.data_to_s16(data)

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 3210  Scale B - Neutral Amps  1       Integer R/CW    Y   xx      1.0         -2 to 1 Power of 10 Default = 0
def scaleB():
    data = device.read(3209, 1)
    return util.data_to_s16(data)

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 3212  Scale D - 3 Phase Volts 1       Integer R/CW    Y   xx      1.0         -2 to 2 Power of 10 Default = 0
def scaleD():
    data = device.read(3211, 1)
    return util.data_to_s16(data)

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 3213  Scale E - Neutral Volts 1       Integer R/CW    Y   xx      1.0         -2 to 2 Power of 10 Default = -1
def scaleE():
    data = device.read(3212, 1)
    return util.data_to_s16(data)

# Reg   Name            Size    Type    Access  NV  Scale   Units       Range
# 3214  Scale F - Power 1       Integer R/CW    Y   xx      1.0         -3 to 3 Power of 10 Default = 0
def scaleF():
    data = device.read(3213, 1)
    return util.data_to_s16(data)

# Reg   Name                        Size    Type    Access  NV  Scale   Units       Range
# 3208  Nominal System Frequency    1       Integer R/CW    Y   xx      Hz          50, 60, 400 Default = 60
def readFreqNom():
    data = device.read(3207, 1)
    return util.data_to_u16(data)

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 624   IP Subnet Mask          2       Octets  R/CW    Y   -       -           IP Address Format Last octet can not
#                                                                               be set to 254. Network part of the mask
#                                                                               must be all '1's and device part must be
#                                                                               all '0's example: 255.255.255.0 is good
#                                                                               255.253.255.0 is invalid
def readIPSubnet():
    data = device.read(623, 2)
    ip_subnet = '%d:%d:%d:%d' % (ord(data[0]), ord(data[1]), ord(data[2]), ord(data[3]))
    #print('%d:%d:%d:%d' % (ord(data[0]), ord(data[1]), ord(data[2]), ord(data[3])))
    return ip_subnet

# Reg   Name                    Size    Type    Access  NV  Scale   Units       Range
# 622   IP Address              2       Octets  R/CW    Y   -       -           IP Address Format First octet must not
#                                                                               be set to 254. Network part of the mask
#                                                                               must be all '1's and device part must be
#                                                                               all '0's example: 255.255.255.0 is good
#                                                                               255.253.255.0 is invalid
def readIP():
    data = device.read(621, 2)
    ip = '%d:%d:%d:%d' % (ord(data[0]), ord(data[1]), ord(data[2]), ord(data[3]))
    #print('%d:%d:%d:%d' % (ord(data[0]), ord(data[1]), ord(data[2]), ord(data[3])))
    return ip

# Reg   Name      Size  Type    Access  NV  Scale   Units       Range
# 629   Baud Rate 1     Integer R/CW    Y   -       -           5-11 Currently Supported 5 = 2400, 6 = 4800, 7 = 9600,
#                                                               8 = 19200 (Default), 9 = 38400
def readBaudRate():
    data = device.read(628, 1)
    return util.data_to_u16(data)

if __name__ == "__main__":

    ipaddr = '134.253.170.243'
    #ipaddr = str(raw_input('ip address: '))
    device = None

    if ipaddr:
        device = client.ModbusClientDeviceTCP(slave_id=22, ipaddr=ipaddr, ipport=502, timeout=10) #, trace_func=trace)

        readVoltageAB()

        print('Freq is = %s' % readHz())
        print('Power is = %s' % readPower())

        print('Baud Rate = %s' % readBaudRate())
        print('Freq Nom = %s' % readFreqNom())
        print('Freq (float) = %s' % readFloatHz())
        print('Power (float) = %s' % readFloatPower())
        print('Power (float) = %s' % readFloatPF())

        print('Scale A = %s' % scaleA())
        print('Scale B = %s' % scaleB())
        print('Scale D = %s' % scaleD())
        print('Scale E = %s' % scaleE())
        print('Scale F = %s' % scaleF())

        for i in range(100):
            print('Power (float) = %s' % readFloatPower())
            print('Power is = %s' % readPower())
            time.sleep(0.25)

