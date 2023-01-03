# encoding = utf-8
import os
import sys
import time
import datetime
import json
import re
import traceback
import base64


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
    stanza_name = helper.get_input_stanza_names()
    input_type = helper.get_input_type()
    # ---------------------------------------------------------------------------------
    url1 = "https://" + opt_hostname_ip_address + "/api/flowApplications"
    method1 = "GET"
    header1 = {
        "Accept": "application/json",
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
        r_json1 = response1.json()
    # ---------------------------------------------------------------------------------
    # Parse data to Splunk format <field>=<value>
    try:
        devices = r_json1['applications']
        for device in devices:
            outputList = [(f'{key}=\"{value}\"')
                          for key, value in device.items()]
            outputString = ",".join(map(str, outputList))
            event = helper.new_event(
                source=source1, index=index1, sourcetype=sourcetype1, data=outputString)
            ew.write_event(event)
    except Exception as e:
        message1 = "Exception=" + str(e)
        helper.log_debug(message1)
    # ---------------------------------------------------------------------------------
