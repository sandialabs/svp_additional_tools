__author__ = 'jayatsandia'

import sys
import time
import numpy as np
import math

sys.path.insert(0, r'C:/Typhoon HIL Control Center/python_portable/Lib/site-packages')
sys.path.insert(0, r'C:/Typhoon HIL Control Center/python_portable/Scripts')
sys.path.insert(0, r'C:/Typhoon HIL Control Center/python_portable')
sys.path.insert(0, r'C:/Typhoon HIL Control Center')
#sys.path.insert(0, r'C:/Typhoon HIL Control Center/typhoon/conf')
#sys.path.insert(0, r'C:/Typhoon HIL Control Center/typhoon/conf/components')

import typhoon.api.hil_control_panel as hil
from typhoon.api.schematic_editor import model
import typhoon.api.pv_generator as pv
import os

hil.set_debug_level(level=1)
hil.stop_simulation()

model.get_hw_settings()
#model_dir = r'D:/SVP/SVP Directories 11-7-16/UL 1741 SA Dev/Lib/Typhoon/'
#print model_dir, os.path.isfile(model_dir)
if not model.load(r'D:/SVP/SVP Directories 11-7-16/UL 1741 SA Dev/Lib/Typhoon/ASGC_AI.tse'):
    print "Model did not load!"

if not model.compile():
    print "Model did not compile!"

# first we need to load model
hil.load_model(file=r'D:/SVP/SVP Directories 11-7-16/UL 1741 SA Dev/Lib/Typhoon/ASGC_AI Target files/ASGC_AI.cpd')

# we could also open existing settings file...
hil.load_settings_file(file=r'D:/SVP/SVP Directories 11-7-16/UL 1741 SA Dev/Lib/Typhoon/settings.runx')

# after setting parameter we could start simulation
hil.start_simulation()

# let the inverter startup
sleeptime = 15
for i in range(1, sleeptime):
    print ("Waiting another %d seconds until the inverter starts. Power = %f." %
           ((sleeptime-i), hil.read_analog_signal(name='Pdc')))
    time.sleep(1)


'''
Setup the circuit for anti-islanding
'''
V_nom = 230.94
P_rating = 34500
freq_nom = 50
resistor = (V_nom**2)/P_rating
capacitor = P_rating/(2*np.pi*freq_nom*(V_nom**2))
inductor = (V_nom**2)/(2*np.pi*freq_nom*P_rating)
resonance_freq = 1/(2*np.pi*math.sqrt(capacitor*inductor))
Qf = resistor*(math.sqrt(capacitor/inductor))
X_C = 1/(2*np.pi*freq_nom*capacitor)
X_L = (2*np.pi*freq_nom*inductor)

print('R = %0.3f, L = %0.3f, C = %0.3f' % (resistor, capacitor, inductor))
print('F_resonance = %0.3f, Qf = %0.3f, X_C = %0.3f, X_L = %0.3f' % (resonance_freq, Qf, X_C, X_L))

R3 = 0
R4 = 0
R5 = 0
L1 = 0
L2 = 0
L3 = 0
C3 = capacitor
C4 = capacitor
C5 = capacitor
L5 = inductor
L6 = inductor
L4 = inductor
R14 = resistor
R15 = resistor
R16 = resistor

'''
set_component_property(component, property, value)
Sets component property value to provided value.

Parameters:
component - name of component.
property - name of property.
value - new property value.
Returns:
True if successful, False otherwise.

set_simulation_time_step(time_step)
Set schematic model simulation time time_step

Arguments:
simulation time step - time step used for simulation
Returns:
True if successful, False otherwise
'''

'''
Waveform capture
'''
simulationStep = hil.get_sim_step()
print('Simulation time step is %f' % simulationStep)
trigsamplingrate = 1./simulationStep
pretrig = 1
posttrig = 2.5
trigval = 0.5
trigtimeout = 5
trigcondition = 'Falling edge'
trigchannel = 'S1_fb'
trigacqchannels = [['V( V_DC3 )', 'I( Ipv )', 'V( V_L1 )', 'I( Ia )'], ['S1_fb']]
n_analog_channels = 4
save_file_name = r'D:\SVP\SVP Directories 11-7-16\UL 1741 SA Dev\Results\capture_test.mat'

# signals for capturing
channelSettings = trigacqchannels

# cpSettings - list[decimation,numberOfChannels,numberOfSamples, enableDigitalCapture]
numberOfSamples = int(trigsamplingrate*(pretrig+posttrig))
print('Numer of Samples is %d' % numberOfSamples)
if numberOfSamples > 32e6/len(channelSettings):
    print('Number of samples is not less than 32e6/numberOfChannels!')
    numberOfSamples = 32e6/n_analog_channels
    print('Number of samples set to 32e6/numberOfChannels!')
elif numberOfSamples < 256:
    print('Number of samples is not greater than 256!')
    numberOfSamples = 256
    print('Number of samples set to 256.')
elif numberOfSamples % 2 == 1:
    print('Number of samples is not even!')
    numberOfSamples += 1
    print('Number of samples set to %d.' % numberOfSamples)

captureSettings = [1, n_analog_channels, numberOfSamples, True]

'''
triggerSource - channel or the name of signal that will be used for triggering (int value or string value)
    Note:
    In case triggerType == Analog:
        triggerSource (int value) - value can be > 0 and <= "numberOfChannels" if we enter channel number.
        triggerSource (string value) - value is Analog signal name that we want to use for trigger source. Analog Signal
        name must be one of signal names from list of signals that we want to capture ("chSettings" list, see below).
    In case triggerType == Digital:
        triggerSource (int value) - value must be > 0 and maximal value depends of number of digital signals in loaded model
        triggerSource (string value) - value is Digital signal name that we want to use for trigger source.

threshold - trigger threshold (float value)
    Note: "threshold" is only used for "Analog" type of trigger. If you use "Digital" type of trigger, you still need to
    provided this parameter (for example 0.0 )

edge - trigger on "Rising edge" or "Falling edge"

triggerOffset - Define the number of samples in percentage to capture before the trigger event (for example 20, if the
    numberOfSamples is 100k, 20k samples before and 80k samples after the trigger event will be captured)
'''

# trSettings - list[triggerType,triggerSource,threshold,edge,triggerOffset]
# triggerSettings = ["Analog", 'I( Irms1 )', trigval, trigcondition, (pretrig*100.)/(pretrig+posttrig)]
# triggerSettings = ["Digital", 'S1_fb', trigval, trigcondition, (pretrig*100.)/(pretrig+posttrig)]
triggerSettings = ["Forced"]
# print('digital signals = %s' % hil.available_digital_signals())

# python list is used for data buffer
capturedDataBuffer = []

print captureSettings
print triggerSettings
print channelSettings
print('Power = %0.3f' % hil.read_analog_signal(name='Pdc'))
if hil.read_digital_signal(name='S1_fb') == 1:
    print('Contactor is closed.')
else:
    print('Contactor is open.')

# start capture process...
if hil.start_capture(captureSettings,
                     triggerSettings,
                     channelSettings,
                     dataBuffer=capturedDataBuffer,
                     fileName=save_file_name,
                     timeout=trigtimeout):

    time.sleep(0.5)

    #print hil.available_contactors()
    print("Actuating S1 Contactor")
    hil.set_contactor_control_mode('S1', swControl=True)
    hil.set_contactor_state('S1', swState=False, executeAt=None)  # open contactor

    if hil.read_digital_signal(name='S1_fb') == 1:
        print('Contactor is closed.')
    else:
        print('Contactor is open.')

    # when capturing is finished...
    while hil.capture_in_progress():
        pass

    # unpack data from data buffer
    (signalsNames, wfm_data, wfm_time) = capturedDataBuffer[0]

    # unpack data for appropriate captured signals
    V_dc = wfm_data[0]  # first row for first signal and so on
    i_dc = wfm_data[1]
    V_ac = wfm_data[2]
    i_ac = wfm_data[3]
    contactor_trig = wfm_data[4]

    import matplotlib.pyplot as plt
    plt.plot(wfm_time, V_ac, 'b', wfm_time, i_ac, 'r', wfm_time, contactor_trig*100, 'k')
    plt.show()

# hil.set_contactor_state('S1', swState=True, executeAt=None)

# read the AC Power
# for i in range(1, 10):
#     print hil.read_analog_signal(name='Pdc')
#     time.sleep(2)

# stop simulation
hil.stop_simulation()

