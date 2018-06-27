
import os
import sys
import traceback
import script
import sunspec.core.modbus.client as client
import sunspec.core.util as util

def test_run():

    result = script.RESULT_FAIL
    gsim = None

    ts.log_debug(' ')
    ts.log_debug('Note: Please remove the Grid Guard Code from the test configuration after '
                 'it has been to run to avoid exposing your Grid Guard Code to others.')
    ts.log_debug(' ')

    try:
        ipaddr = ts.param_value('gg.ipaddr')
        new_gg = ts.param_value('gg.code')
        # register = ts.param_value('gg.register')
        # port = ts.param_value('gg.port')
        # comm_id = ts.param_value('gg.id')

        register = 43090
        port = 502
        comm_id = 3

        if not new_gg or new_gg == 'None':
            raise script.ScriptFail('No Grid Guard Code specified.')

        device = client.ModbusClientDeviceTCP(comm_id, ipaddr, port)
        data = device.read(register, 2)
        gg = util.data_to_u32(data)
        ts.log('Current grid guard code: %s' % hex(gg))
        if gg == 0:
            ts.log('Original grid guard was not enabled')
        else:
            ts.log('Original grid guard was enabled')

        device.write(register, util.u32_to_data(int(new_gg)))
        data = device.read(register, 2)
        gg = util.data_to_u32(data)

        ts.log('Updated grid guard code: = %s' % hex(gg))
        if gg == 0:
            ts.log_warning('Current grid guard is not enabled')
            result = script.RESULT_FAIL
        else:
            ts.log('Current grid guard is enabled')
            result = script.RESULT_PASS

    except script.ScriptFail, e:
        reason = str(e)
        if reason:
            ts.log_error(reason)
    finally:
        if gsim:
            gsim.close()

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

        result = test_run()

        ts.result(result)
        if result == script.RESULT_FAIL:
            rc = 1

    except Exception, e:
        ts.log_error('Test script exception: %s' % traceback.format_exc())
        rc = 1

    sys.exit(rc)

info = script.ScriptInfo(name=os.path.basename(__file__), run=run, version='1.0.0')

info.param_group('gg', label='Parameters', glob=True)
info.param('gg.ipaddr', label='IP Address', default='192.168.0.2')
#info.param('gg.id', label='Slave ID', default=3)
#info.param('gg.register', label='Modbus Register', default=43090)
#info.param('gg.port', label='TCP Port', default=502)
info.param('gg.code', label='Grid Guard Code', default='12345678')

def script_info():
    return info


if __name__ == "__main__":

    # stand alone invocation
    config_file = None
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    test_script = script.Script(info=script_info(), config_file=config_file)

    run(test_script)



