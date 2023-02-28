# encoding = utf-8
import os
import sys
import time
import datetime
import json
import re
import traceback
import base64
import xmltodict


def basic_auth(username, password):
    token = base64.b64encode(
        bytes(f"{username}:{password}", "utf-8")).decode("ascii")
    return f'Basic {token}'


def validate_input(helper, definition):
    pass


def collect_events(helper, ew):
    global_account = helper.get_arg('global_account')
    username = global_account['username']
    password = global_account['password']
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    # ---------------------------------------------------------------------------------
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    # ---------------------------------------------------------------------------------
    url1 = "https://" + opt_hostname_ip_address + "/api/flowHistory/"
    method1 = "GET"
    header1 = {
        "content-type": "application/json",
        "Authorization": basic_auth(username, password)
    }
    # ---------------------------------------------------------------------------------
    # HTTP Request
    response1 = helper.send_http_request(
        url1, method1, parameters=None, payload=None, headers=header1, cookies=None, verify=False, timeout=None, use_proxy=False)
    r_status1 = response1.status_code
    if (r_status1 != 200):
        response1.raise_for_status()
    else:
        r_json1 = response1.text
    # ---------------------------------------------------------------------------------
    try:
        poller = r_json1['PerfExport'][0]['serverName']
        allDevices = r_json1['PerfExport'][0]['DeviceData']
        for device in allDevices:
            deviceKeys = device[0].keys()
            device_meta = ""
            for key in deviceKeys:
                if not isinstance(device[0][key], list):
                    device_meta = ",".join(
                        [device_meta, f"{key}=\"{device[0][key]}\""])
            allPorts = device[0]['PortInfo']
            if len(allPorts) == 1:
                for i in range(0, len(allPorts), 1):
                    output = ""
                    keys = list(allPorts[i].keys())
                    for key in keys:
                        output = ",".join(
                            [output, f"{key}=\"{allPorts[i][key]}\""])
                    outputString = poller + device_meta + output
                    event = helper.new_event(
                        source=source1, index=index1, sourcetype=sourcetype1, data=outputString)
                    ew.write_event(event)
            else:
                for i in range(0, len(allPorts), 1):
                    output = ""
                    keys = list(allPorts[i][0].keys())
                    for key in keys:
                        output = ",".join(
                            [output,  f"{key}=\"{allPorts[i][0][key]}\""])
                    outputString = poller + device_meta + output
                    event = helper.new_event(
                        source=source1, index=index1, sourcetype=sourcetype1, data=outputString)
                    ew.write_event(event)
    except Exception as e:
        message1 = "Exception=" + str(e)
        helper.log_debug(message1)
