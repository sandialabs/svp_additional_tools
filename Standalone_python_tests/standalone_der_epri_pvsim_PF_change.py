"""
Copyright (c) 2018, Sandia National Labs and SunSpec Alliance
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

Neither the names of the Sandia National Labs and SunSpec Alliance nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Questions can be directed to support@sunspec.org
"""

import os
import httplib
import json
import requests
import SimpleHTTPServer
import SocketServer

if __name__ == "__main__":

    # # Client tests
    # headers = {'Content-type': 'application/json'}
    #
    # comm_start_cmd = {
    #     "namespace": "comms",
    #     "function": "startCommunication",
    #     "requestId": "requestId",
    #     "parameters": {
    #         "deviceIds": ['03ac0d62-2d29-49ad-915e-15b9fbd46d86',]
    #     }
    # }
    #
    # response = requests.post('http://localhost:8000', json=comm_start_cmd)
    # print('Data Posted! statusMessage: %s' % response.json()['statusMessage'])

    pf_cmd = {"namespace": "der",
              "function": "configurePowerFactor",
              "requestId": "requestId",
              "parameters": {
                  "deviceIds": ["03ac0d62-2d29-49ad-915e-15b9fbd46d86"],
                  "timeWindow": 0,
                  "reversionTimeout": 0,
                  "rampTime": 0,
                  "powerFactor": -0.85,
                  "varAction": "reverseProducingVars"
                  }
              }

    print('Setting new PF...')
    response = requests.post('http://10.1.2.2:8000', json=pf_cmd)
    print('Data Posted! statusMessage: %s' % response.json()['statusMessage'])

    pf_enable_cmd = {"namespace": "der",
                     "function": "powerFactor",
                     "requestId": "requestId",
                     "parameters": {
                         "deviceIds": ["03ac0d62-2d29-49ad-915e-15b9fbd46d86"],
                         "enable": True
                         }
                     }

    print('Enabling new PF...')
    response = requests.post('http://10.1.2.2:8000', json=pf_enable_cmd)
    print('Data Posted! statusMessage: %s' % response.json()['statusMessage'])
