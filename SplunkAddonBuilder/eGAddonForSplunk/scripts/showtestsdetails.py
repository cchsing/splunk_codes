
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
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # hostname_ip_address = definition.parameters.get('hostname_ip_address', None)
    # port = definition.parameters.get('port', None)
    # component_type = definition.parameters.get('component_type', None)
    # component_name = definition.parameters.get('component_name', None)
    # test_type = definition.parameters.get('test_type', None)
    # test_name = definition.parameters.get('test_name', None)
    pass


def collect_events(helper, ew):
    global_account = helper.get_arg('global_account')
    username = global_account['username']
    password = global_account['password']
    password_base64 = base64.b64encode(
        bytes(f"{password}", "utf-8")).decode("ascii")
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    opt_component_type = helper.get_arg('component_type')
    opt_component_name = helper.get_arg('component_name')
    opt_test_type = helper.get_arg('test_type')
    opt_test_name = helper.get_arg('test_name')

    url = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/orchestration/showtestsdetails"
    method = "POST"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    header1 = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    body1 = {
        "componenttype": opt_component_type,
        "componentname": opt_component_name,
        "testtype": opt_test_type,
        "testname": opt_test_name
    }
    response = helper.send_http_request(url, method, parameters=None, payload=body1,
                                        headers=header1, cookies=None, verify=False, cert=None,
                                        timeout=None, use_proxy=False)

    r_status = response.status_code
    if (r_status != 200):
        response.raise_for_status()
    else:
        r_json = response.json()

    data = json.dumps(r_json)
    event = helper.new_event(data, time=None, host=None, index=None,
                             source=None, sourcetype=None, done=True, unbroken=True)
    ew.write_event(event)
