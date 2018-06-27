
import sunspec.core.modbus.client as client
import sunspec.core.util as util
import binascii
import time

def trace(msg):
    print msg

def readAdvancedPwrControlEn():
    data = device.read(0xf142, 2)  # read AdvancedPwrControlEn
    AdvancedPwrControlEn = util.data_to_u32(data)
    print 'AdvancedPwrControlEn = %s' % (AdvancedPwrControlEn == 1)
    return (AdvancedPwrControlEn == 1)

def writeAdvancedPwrControlEn(control=True):
    if control:
        device.write(0xf142, util.u32_to_data(1))  # write power factor
    else:
        device.write(0xf142, util.u32_to_data(0))  # write power factor
    return readAdvancedPwrControlEn()

def readFrtEn():
    data = device.read(0xf144, 2)  # read AdvancedPwrControlEn
    FrtEn = util.data_to_u32(data)
    print 'FrtEn = %s' % FrtEn
    return FrtEn

def readPF():
    # data = device.read(0xf002, 2)  #read power factor
    # pf = util.data_to_float(data)
    # print 'power factor = %s' % pf
    data = device.read(0xf10a, 2)  #read power factor
    pf = util.data_to_float(data)
    print 'power factor = %s' % pf
    return pf

def writePF(power_factor=1.0):
    # device.write(0xf002, util.float32_to_data(power_factor))  # write power factor
    device.write(0xf10a, util.float32_to_data(power_factor))  # write power factor
    pf = readPF()
    return pf

def writePF_Ena(Ena=True):
    # Modbus F104 codes
    # 0 - Fixed CosPhi mode
    # 1 - CosPhi(P) mode
    # 2 - Fixed Q mode
    # 3 - Q(U) + Q(P) mode
    # 4 - RRCR mode
    if Ena:
        device.write(0xf104, util.u16_to_data(0))    # write power factor enable
    else:
        device.write(0xf104, util.u16_to_data(4))    # write power factor enable
    return readPF_Ena()

def readPF_Ena():
    data = device.read(0xf104, 1)  # read power factor enable
    pf_ena = util.data_to_u16(data)
    print 'power factor ena = %s' % (pf_ena == 0)
    return (pf_ena == 0)

def readPower():
    data = device.read(0xf001, 1)    # read power
    w_max = util.data_to_u16(data)
    print 'active power = %s' % w_max
    return w_max

def writePower(power=100):
    device.write(0xf001, util.u16_to_data(power))  # write power
    return readPower()

def readCommitPower():
    data = device.read(0xf100, 1)  # read Commit Power Control Settings
    w_max_ena = util.data_to_u16(data)
    print 'active power ena = %s' % (w_max_ena == 0)

def writeCommitPower(commit=True):
    if commit:
        device.write(0xf100, util.u16_to_data(1))  # write Commit Power Control Settings
    else:
        device.write(0xf100, util.u16_to_data(0))  # write Commit Power Control Settings
    return readCommitPower()

def restorePowerControl(restore=True):
    if restore:
        device.write(0xf101, util.u16_to_data(1))  # write Restore Power Control Default Settings
    else:
        device.write(0xf101, util.u16_to_data(0))  # write Restore Power Control Default Settings
    return readRestorePowerControl()

def readRestorePowerControl():
    data = device.read(0xf100, 1)  # read Restore Power Control Default Settings
    restore = util.data_to_u16(data)
    print 'active power ena = %s' % restore
    return restore

if __name__ == "__main__":

    ipaddr = '134.253.142.44'
    #ipaddr = str(raw_input('ip address: '))
    device = None

    if ipaddr:
        device = client.ModbusClientDeviceTCP(slave_id=1, ipaddr=ipaddr, ipport=502, timeout=10) #trace_func=trace

        '''
        if not readAdvancedPwrControlEn():
            writeAdvancedPwrControlEn(control=True)
        pf = 0.85
        if readPF() != pf:
            writePF(power_factor=0.85)
        if not readPF_Ena():
            writePF_Ena(Ena=True)
        readPF()
        '''

        if not readAdvancedPwrControlEn():
            writeAdvancedPwrControlEn(control=True)
            writeCommitPower(commit=True)
        for p in range(1, 15):
            print "Setting power to %d" % p
            writePower(power=p)
            time.sleep(5)
        writePower(power=10)
        #readPower()

