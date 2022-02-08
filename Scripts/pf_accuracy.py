"""
The phase-angle change ride-through (PCRT) test verifies the ability of the EUT to ride through sudden voltage
phase-angle changes without tripping in accordance with the requirements in 6.5.2.6 of IEEE Std 1547-2018.

Initial Script: 2-4-20, jjohns2@sandia.gov

"""

import sys
import os
import traceback
from svpelab import hil
from svpelab import das
from svpelab import pvsim
from svpelab import der
from svpelab import p1547
import script
import itertools
import numpy as np


def test_run():

    result = script.RESULT_PASS
    phil = None
    daq = None
    pv = None
    eut = None
    result_summary = None
    dataset_filename = None
    ds = None
    result_params = None

    try:
        n_pv = ts.param_value('test.n_pv')
        n_meas = ts.param_value('test.n_meas')
        p_max = ts.param_value('test.p_max')
        p_max_per_input = p_max / n_pv
        t_start = ts.param_value('test.t_start')
        t_stable = ts.param_value('test.t_stable')
        test_start = int(ts.param_value('test.test_start'))

        # initialize the pv simulators
        pv = []
        for i in range(n_pv):
            pv.append(pvsim.pvsim_init(ts, '%s' % (i+1)))
        for i in range(n_pv):
            pv[i].power_on()

        eut = der.der_init(ts)
        eut.config()

        # initialize the hardware in the loop - this is only for AC data capture
        phil = hil.hil_init(ts)
        if phil is not None:
            ts.log("{}".format(phil.info()))
            phil.config()

        # initialize the das
        das_points = {'sc': ('Test', 'PF_Target', 'Irradiance')}
        daq = das.das_init(ts, sc_points=das_points['sc'], support_interfaces={'hil': phil})
        daq.sc['Test'] = 0
        daq.sc['PF_Target'] = 0
        daq.sc['Irradiance'] = 0

        # initialize the der
        eut = der.der_init(ts)
        ts.log('Allowing inverter %0.2f seconds to start...' % t_start)
        ts.sleep(t_start)

        # open result summary file
        result_summary_filename = 'result_summary.csv'
        result_summary = open(ts.result_file_path(result_summary_filename), 'a+')
        ts.result_file(result_summary_filename)
        result_summary.write('Test, PF_Target, Irradiance, P, Q\n')

        ts.log_debug('Starting experiments from Test #%d' % test_start)

        total_runs = 0
        for irradiance in list(np.linspace(100, 1000, 10)):  # 3
            ts.log('Starting tests with Irradiance = %s' % irradiance)

            # Set PV I-V Curves
            for i in range(n_pv):
                pv[i].irradiance(irradiance)

            for pf in list(np.linspace(0.85, 1, 16)) + list(np.linspace(-0.99, -0.85, 15)):  # 4
                total_runs += 1
                pf = round(pf, 2)
                ts.log('Starting PF = %s' % pf)
                eut.fixed_pf(params={'pf': pf, 'ena': True})
                test_name = 'Test_%s_Irr=%s_PF=%s' % (total_runs, irradiance, pf)

                ts.sleep(t_stable)  # give inverter time to reach steady-state
                daq.data_capture(True)  # begin dataset for this test case

                p_ac = 0.
                q_ac = 0.

                for meas in range(n_meas):  # Take n_meas measurements
                    daq.sc['PF_Target'] = pf
                    daq.sc['Irradiance'] = irradiance
                    daq.data_sample()  # add new data points with soft channels to data set
                    data = daq.data_capture_read()  # get last points sampled
                    # ts.log('current data: %s' % data)  # print last data points
                    p_ac += data['AC_P_1'] + data['AC_P_2'] + data['AC_P_3']
                    q_ac += data['AC_Q_1'] + data['AC_Q_2'] + data['AC_Q_3']

                    ts.sleep(1)

                ds = daq.data_capture_dataset()  # get dataset
                ds.to_csv(ts.result_file_path(test_name + '.csv'))  # write to csv
                daq.data_capture(False)  # finish this dataset

                # Create new entry for summary file
                p_avg = p_ac / n_meas
                q_avg = q_ac / n_meas
                result_summary.write('%s, %s, %s, %s, %s\n' % (test_name, pf, irradiance, p_avg, q_avg))
                ts.log_warning('Avg data for %s: P_AC = %0.1f W, Q_AC = %0.1f Var, pf=%s' %
                               (test_name, p_avg, q_avg, pf))

        result = script.RESULT_COMPLETE

    except script.ScriptFail as e:
        reason = str(e)
        if reason:
            ts.log_error(reason)
    finally:
        if phil is not None:
            phil.close()
        if daq is not None:
            daq.close()
        if pv is not None:
            for pv_item in pv:
                pv_item.close()
        if eut is not None:
            eut.close()
        if result_summary is not None:
            result_summary.close()
    return result


def run(test_script):

    try:
        global ts
        ts = test_script
        rc = 0
        result = script.RESULT_COMPLETE

        ts.log_debug('')
        ts.log_debug('**************  Starting %s  **************' % (ts.config_name()))
        ts.log_debug('Script: %s %s' % (ts.name, ts.info.version))
        ts.log_active_params()

        ts.svp_version(required='1.5.9')

        result = test_run()

        ts.result(result)
        if result == script.RESULT_FAIL:
            rc = 1

    except Exception as e:
        ts.log_error('Test script exception: %s' % traceback.format_exc())
        rc = 1

    sys.exit(rc)


info = script.ScriptInfo(name=os.path.basename(__file__), run=run, version='1.0.0')

# Test
info.param_group('test', label='Test Configuration')
info.param('test.n_pv', label='Number of PV Inputs?', default=6)
info.param('test.n_meas', label='Number of Measurements at Each PF?', default=10)
info.param('test.t_start', label='Inverter Start Up Time (s)?', default=300.)
info.param('test.t_stable', label='Inverter Stabilization Time (s)?', default=5.)
info.param('test.test_start', label='Start Test Number?', default=1)

hil.params(info)
das.params(info)
pvsim.params(info, '1', 'PV Simulator 1')
pvsim.params(info, '2', 'PV Simulator 2')
pvsim.params(info, '3', 'PV Simulator 2')
pvsim.params(info, '4', 'PV Simulator 2')
pvsim.params(info, '5', 'PV Simulator 2')
pvsim.params(info, '6', 'PV Simulator 2')
der.params(info)


def script_info():
    
    return info


if __name__ == "__main__":

    # stand alone invocation
    config_file = None
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    params = None

    test_script = script.Script(info=script_info(), config_file=config_file, params=params)
    test_script.log('log it')

    run(test_script)



