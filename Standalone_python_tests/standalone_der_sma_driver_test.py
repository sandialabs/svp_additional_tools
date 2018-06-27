import sunspec.core.client as client
import time

ipaddr = '134.253.142.29'
port = 502
comm_id = 126

device = client.SunSpecClientDevice(client.TCP, slave_id=comm_id, ipaddr=ipaddr, ipport=port)

for x in range(3):
    for p in [25, 50, 75, 100]:
        device.settings.read()
        print(device.settings)
        device.settings.WMax = p/100.*3000
        device.settings.write()
        device.settings.read()
        print(device.settings)
        time.sleep(1)

device.close()
