# encoding = utf-8
import os
import sys
import time
import datetime
import json
import re
import traceback
import base64


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # hostname_ip_address = definition.parameters.get('hostname_ip_address', None)
    # port = definition.parameters.get('port', None)
    # username = definition.parameters.get('username', None)
    # password = definition.parameters.get('password', None)
    # type = definition.parameters.get('type', None)
    # name_ = definition.parameters.get('name_', None)
    pass


def collect_events(helper, ew):

    msg1 = "Input: " + helper.get_input_stanza_names() + "triggered."
    helper.log_info(msg1)
    global_account = helper.get_arg('global_account')
    username = global_account['username']
    password = global_account['password']
    password_base64 = base64.b64encode(
        bytes(f"{password}", "utf-8")).decode("ascii")
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    # opt_username = helper.get_arg('username')
    # opt_password = helper.get_arg('password')
    opt_type = helper.get_arg('type')
    opt_name_ = helper.get_arg('name_')

    url = "https://" + opt_hostname_ip_address + \
        ":" + opt_port + "/api/eg/analytics/getAlerts"
    method = "POST"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    header1 = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    body1 = {
        "type": opt_type,
        "name": opt_name_
    }
    response = helper.send_http_request(url, method, parameters=None, payload=body1,
                                        headers=header1, cookies=None, verify=False, cert=None,
                                        timeout=None, use_proxy=True)

    r_json = response.json()

    r_status = response.status_code
    if r_status != 200:
        # check the response status, if the status is not sucessful, raise requests.HTTPError
        response.raise_for_status()

    # To create a splunk event
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    # data = r_json['data']
    try:
        data = r_json['data']
        for item in data:
            item_str = json.dumps(item)
            event = helper.new_event(
                source=source1, index=index1, sourcetype=sourcetype1, data=item_str)
            ew.write_event(event)
    except:
        e = json.dumps(r_json)
        helper.log_info("An exception occurred for " + source1 + ": " + e)
