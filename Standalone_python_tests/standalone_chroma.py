__author__ = 'detldaq'

# import Python IVI
#import ivi
#import usbtmc
import visa
import serial
from PyDAQmx import *


def load_query(chroma, cmd):
    resp = ''
    more_data = True
    chroma.flushInput()
    chroma.write(cmd)
    while more_data:
        count = chroma.inWaiting()
        if count < 1:
            count = 1
        data = chroma.read(count)
        if len(data) > 0:
            for d in data:
                resp += d
                if d == '\n':
                    more_data = False

    return resp

def national_instruments_analog_read():
    analog_input = Task()
    read = int32()
    data = numpy.zeros((1000,), dtype=numpy.float64)

    # DAQmx Configure Code
    analog_input.CreateAIVoltageChan("Dev1/ai0", "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts, None)
    analog_input.CfgSampClkTiming("", 10000.0, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, 1000)

    # DAQmx Start Code
    analog_input.StartTask()

    # DAQmx Read Code
    analog_input.ReadAnalogF64(1000, 10.0, DAQmx_Val_GroupByChannel, data, 1000, byref(read), None)

    print "Acquired %d points" % read.value

    # from nidaqmx import System
    # system = System()
    # print 'libnidaqmx version:', system.version
    # #libnidaqmx version: 8.0
    # print 'NI-DAQ devices:', system.devices
    # dev1 = system.devices[0]
    # print dev1.get_product_type()
    # print dev1.get_bus()
    # print dev1.get_analog_input_channels()

    # PXI INSTR 	PXI[bus]::device[::function][::INSTR]
    # PXI INSTR 	PXI[interface]::bus-device[.function][::INSTR]
    # PXI INSTR 	PXI[interface]::CHASSISchassis number::SLOTslot number[::FUNCfunction][::INSTR]

    # PXI::15::INSTR 	    PXI device number 15 on bus 0 with implied function 0.
    # PXI::2::BACKPLANE 	Backplane resource for chassis 2 on the default PXI system, which is interface 0.
    # PXI::CHASSIS1::SLOT3 	PXI device in slot number 3 of the PXI chassis configured as chassis 1.
    # PXI0::2-12.1::INSTR 	PXI bus number 2, device 12 with function 1.

    # inst = rm.open('PXI0::2-12.1::INSTR', resource_pyclass=MessageBasedResource)

    # my_instrument = rm.open_resource('ASRL1::INSTR')
    # print(my_instrument.query("*IDN?\n"))

def load_write(chroma, cmd):
    chroma.flushInput()
    chroma.write(cmd)

if __name__ == "__main__":

    # Power supply
    rm = visa.ResourceManager()
    print(rm.list_resources())

    my_instrument = rm.open_resource('USB0::0x1698::0x0837::008000000452::INSTR')
    print(my_instrument.query('*IDN?').rstrip('\n'))
    my_instrument.write('*RST\n')

    print(my_instrument.query('CONF:FOLD?\n').rstrip('\n'))
    print(my_instrument.query('CONF:FOLDT?\n').rstrip('\n'))

    print(my_instrument.query('CONF:OUTP?\n').rstrip('\n'))
    my_instrument.write('CONF:OUTP ON\n')
    print(my_instrument.query('CONF:OUTP?\n').rstrip('\n'))
    my_instrument.write('CONF:OUTP OFF\n')
    print(my_instrument.query('CONF:OUTP?\n').rstrip('\n'))

    print(my_instrument.query('SOUR:VOLT:LIMIT:LOW?\n').rstrip('\n'))
    my_instrument.write('SOUR:VOLT:LIMIT:LOW 20.0\n')
    print(my_instrument.query('SOUR:VOLT:LIMIT:LOW?\n').rstrip('\n'))
    my_instrument.write('SOUR:VOLT:LIMIT:LOW 30.0\n')
    print(my_instrument.query('SOUR:VOLT:LIMIT:LOW?\n').rstrip('\n'))

    print(my_instrument.query('SOUR:CURR:LIMIT:LOW?\n').rstrip('\n'))
    my_instrument.write('SOUR:CURR:LIMIT:LOW 20.0\n')
    print(my_instrument.query('SOUR:CURR:LIMIT:LOW?\n').rstrip('\n'))
    my_instrument.write('SOUR:CURR:LIMIT:LOW 30.0\n')
    print(my_instrument.query('SOUR:CURR:LIMIT:LOW?\n').rstrip('\n'))

    # Load bank
    chroma = serial.Serial(port="com7", baudrate=115200, bytesize=8, stopbits=1,
                           xonxoff=0, timeout=5, writeTimeout=5)

    # Working
    load_write(chroma, '*RST\n')
    #load_write(chroma, '*CLS\n')
    print(load_query(chroma, "*IDN?\n").rstrip('\n'))
    #chroma.write('SOUR:VOLT:LIMIT:HIGH 20.\n')
    print('MODE? %d' % float(load_query(chroma, 'MODE?\n').rstrip('\n')))
    load_write(chroma, 'MODE CCH\n') #set mode to constant current high
    print('MODE? %s' % load_query(chroma, 'MODE?\n').rstrip('\n'))
    # 0 = CCL
    # 1 = CCH
    # 2 = CCDL
    # 3 = CCDL, etc.

    print('MEAS:CURR?;VOLT? %s' % load_query(chroma, "MEAS:CURR?;VOLT?\n").rstrip('\n'))
    print('CONF:VOLT:RANG? %s' % load_query(chroma, 'CONF:VOLT:RANG?\n').rstrip('\n'))  # 0 = low range, 1 = high
    print('CONF:VOLT:PROT? %s' % load_query(chroma, 'CONF:VOLT:PROT?\n').rstrip('\n'))  # 0 = OFF, 1 = ON
    print('CONF:VOLT:ON? %s' % load_query(chroma, 'CONF:VOLT:ON?\n').rstrip('\n'))
    load_write(chroma, 'CONF:REM ON\n')
    load_write(chroma, 'CONF:VOLT:ON 1\n')
    print('CONF:VOLT:ON? %s' % load_query(chroma, 'CONF:VOLT:ON?\n').rstrip('\n'))

    print('FETCh:CURR? %s' % load_query(chroma, 'FETCh:CURR?\n').rstrip('\n'))
    print('FETCh:POW? %s' % load_query(chroma, 'FETCh:POW?\n').rstrip('\n'))
    print('FETCh:RES? %s' % load_query(chroma, 'FETCh:RES?\n').rstrip('\n'))
    print('FETCh:VOLT? %s' % load_query(chroma, 'FETCh:VOLT?\n').rstrip('\n'))
    print('FETCh:STAT? %s' % load_query(chroma, 'FETCh:STAT?\n').rstrip('\n'))

    load_write(chroma, 'CURR:STAT A\n')
    print('CURR:STAT? %s' % load_query(chroma, 'CURR:STAT?\n').rstrip('\n'))  # 0 = B, 1 = A
    print('CURR:STAT:L1? %s' % load_query(chroma, 'CURR:STAT:L1?\n').rstrip('\n'))
    print('CURR:STAT:L2? %s' % load_query(chroma, 'CURR:STAT:L2?\n').rstrip('\n'))
    print('CURR:STAT:L1? MAX %s' % load_query(chroma, 'CURR:STAT:L1? MAX\n').rstrip('\n'))
    print('CURR:STAT:L1? MIN %s' % load_query(chroma, 'CURR:STAT:L1? MIN\n').rstrip('\n'))

    print('LOAD? %s' % load_query(chroma, 'LOAD?\n').rstrip('\n'))
    load_write(chroma, 'LOAD ON\n')
    print('LOAD? %s' % load_query(chroma, 'LOAD?\n').rstrip('\n'))
    load_write(chroma, 'LOAD OFF\n')
    print('LOAD? %s' % load_query(chroma, 'LOAD?\n').rstrip('\n'))

    # Not working
    #print(load_query(chroma, 'CONF:VOLT:ON?\n'))
    #print(load_query(chroma, 'CURR:L1/L2?\n'))
    #print(load_query(chroma, 'VOLT:L1/L2?\n'))
