
# import sunspec.core.modbus.client as client
import sunspec.core.client as client
import sunspec.core.util as util
import binascii
import time
import socket
import commands

if __name__ == "__main__":

    timeout = 2
    # ipports = [502, 1502, 5502]
    # slave_ids = [1, 126]
    ipports = [1502]
    slave_ids = [1]

    ipaddr = socket.gethostbyname(socket.gethostname())
    print('This machine has the following default IP: %s' % ipaddr)
    ip_values = ipaddr.split(".")

    for i in range(256):
        # ip = '%s.%s.%s.%s' % (ip_values[0], ip_values[1], ip_values[2], i)
        ip = '%s.%s.%s.%s' % (10, 1, 2, i)
        for ipport in ipports:
            for slave_id in slave_ids:
                try:
                    print('Communicating to %s on port %s with slave_id %s' % (ip, ipport, slave_id))
                    device = client.SunSpecClientDevice(client.TCP, slave_id=slave_id, ipaddr=ip, ipport=ipport, timeout=timeout)
                    # device = client.ModbusClientDeviceTCP(slave_id=slave_id, ipaddr=ip, ipport=ipport, timeout=timeout)
                    params = {}
                    device.common.read()
                    params['Manufacturer'] = device.common.Mn
                    params['Model'] = device.common.Md
                    params['Options'] = device.common.Opt
                    params['Version'] = device.common.Vr
                    params['SerialNumber'] = device.common.SN
                    print('This is a %s %s device' % (params['Manufacturer'], params['Model']))
                except Exception, e:
                    print('Error: %s' % e)

