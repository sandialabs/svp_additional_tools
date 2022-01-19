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

        # initialize the pv simulators
        pv = []
        for i in range(n_pv):
            pv.append(pvsim.pvsim_init(ts, '%s' % (i+1)))
        for i in range(n_pv):
            pv[i].power_on()

        # initialize the hardware in the loop - this is only for AC data capture
        phil = hil.hil_init(ts)
        if phil is not None:
            ts.log("{}".format(phil.info()))
            phil.config()

        # initialize the das
        das_points = {'sc': ('Test', 'PV_P_MPP_NO_DERATE', 'PV_V_MPP',
                             'PV_V_1', 'PV_I_1', 'PV_P_1', 'PV_V_2', 'PV_I_2', 'PV_P_2',
                             'PV_V_3', 'PV_I_3', 'PV_P_3', 'PV_V_4', 'PV_I_4', 'PV_P_4',
                             'PV_V_5', 'PV_I_5', 'PV_P_5', 'PV_V_6', 'PV_I_6', 'PV_P_6',
                             'PV_MPPT_Acc_1', 'PV_MPPT_Acc_2', 'PV_MPPT_Acc_3',
                             'PV_MPPT_Acc_4', 'PV_MPPT_Acc_5', 'PV_MPPT_Acc_6')}
        daq = das.das_init(ts, sc_points=das_points['sc'], support_interfaces={'hil': phil})
        daq.sc['PV_P_MPP_NO_DERATE'] = 0
        daq.sc['PV_V_MPP'] = 0
        for i in range(n_pv):
            daq.sc['PV_V_%s' % (i+1)] = 0
            daq.sc['PV_I_%s' % (i+1)] = 0
            daq.sc['PV_P_%s' % (i+1)] = 0
            daq.sc['PV_MPPT_Acc_%s' % (i+1)] = 0

        # initialize the der
        eut = der.der_init(ts)
        ts.log('Allowing inverter %0.2f seconds to start...' % t_start)
        ts.sleep(t_start)

        # open result summary file
        result_summary_filename = 'result_summary.csv'
        result_summary = open(ts.result_file_path(result_summary_filename), 'a+')
        ts.result_file(result_summary_filename)
        result_summary.write('Test, n_derated, p_max, p_ac, p_dc, eff, mppt_accuracy\n')

        total_runs = 0
        for v_mp in [600, 720, 800]:  # 3
            ts.log('Starting tests with v_mp = %s' % v_mp)
            for derating in [0.2, 0.4, 0.6, 0.8]:  # 4
                ts.log('Starting Test with derating = %s' % derating)
                for combo in list(itertools.product([0, 1], repeat=n_pv)):  # 2^6 = 64
                    n_derated = sum(combo)
                    max_power = ((n_pv - n_derated) + (n_derated * derating)) * p_max_per_input
                    total_runs += 1
                    test_name = 'mppt_v=%s_derate=%s_strings=%s' % (v_mp, derating, str(combo).replace(',', ''))
                    ts.log_debug('Starting Test #%d: %s' % (total_runs, test_name))

                    # Set PV I-V Curves
                    for i in range(n_pv):
                        if str(combo[i]) == '1':
                            # ts.log_debug('Setting PV #%d to the derated power level' % (i + 1))
                            p_mp = p_max_per_input * derating
                            pv[i].iv_curve_config(pmp=p_mp, vmp=v_mp)
                        else:
                            # ts.log_debug('Setting PV #%d to NO DERATE' % (i + 1))
                            pv[i].iv_curve_config(pmp=p_max_per_input, vmp=v_mp)

                    ts.sleep(t_stable)  # give inverter time to reach steady-state
                    daq.data_capture(True)  # begin dataset for this test case

                    p_ac = 0.
                    p_dc = 0.
                    mppt_acc = 0.
                    for meas in range(n_meas):  # Take n_meas measurements
                        daq.sc['PV_P_MPP_NO_DERATE'] = p_max_per_input
                        daq.sc['PV_V_MPP'] = v_mp
                        for i in range(n_pv):  # Get PV data and add to the soft channel list
                            pv_data = pv[i].measurements_get()
                            daq.sc['Test'] = test_name
                            daq.sc['PV_V_%s' % (i+1)] = pv_data['DC_V']
                            daq.sc['PV_I_%s' % (i+1)] = pv_data['DC_I']
                            daq.sc['PV_P_%s' % (i+1)] = pv_data['DC_P']
                            daq.sc['PV_MPPT_Acc_%s' % (i+1)] = pv_data['MPPT_Accuracy']

                        daq.data_sample()  # add new data points with soft channels to data set
                        data = daq.data_capture_read()  # get last points sampled
                        # ts.log('current data: %s' % data)  # print last data points
                        p_ac += (data['AC_P_1'] + data['AC_P_2'] + data['AC_P_3']) / n_meas
                        p_dc += (data['PV_P_1'] + data['PV_P_2'] + data['PV_P_3'] + data['PV_P_4']
                                 + data['PV_P_5'] + data['PV_P_6']) / n_meas
                        mppt_acc += (data['PV_MPPT_Acc_1'] + data['PV_MPPT_Acc_2'] + data['PV_MPPT_Acc_3']
                                     + data['PV_MPPT_Acc_4'] + data['PV_MPPT_Acc_5'] + data['PV_MPPT_Acc_6']) / \
                                    (n_meas * n_pv)  # average over the measurements and DC inputs
                        ts.sleep(1)
                    ds = daq.data_capture_dataset()  # get dataset
                    ds.to_csv(ts.result_file_path(test_name + '.csv'))  # write to csv
                    daq.data_capture(False)  # finish this dataset

                    # Create new entry for summary file
                    mppt_eff = 100. * (p_ac / p_dc)
                    result_summary.write('%s, %s, %s, %s, %s, %s, %s\n' % (test_name, n_derated, max_power,
                                                                           p_ac, p_dc, mppt_eff, mppt_acc))
                    ts.log_warning('Avg data for %s: P_AC = %0.1f W, P_DC = %0.1f W, MPPT Eff = %0.4f, '
                                   'MPPT Accuracy = %s\n' % (test_name, p_ac, p_dc, mppt_eff, mppt_acc))

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
info.param('test.n_meas', label='Number of Measurements at Each I-V Curve Config?', default=12)
info.param('test.p_max', label='Inverter Nameplate Power (W)?', default=33000.)
info.param('test.t_start', label='Inverter Start Up Time (s)?', default=300.)
info.param('test.t_stable', label='Inverter Stabilization Time (s)?', default=5.)

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



