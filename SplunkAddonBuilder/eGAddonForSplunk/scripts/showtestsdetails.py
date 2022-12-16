# encoding = utf-8
import os
import sys
import time
import datetime
import json


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # hostname_ip_address = definition.parameters.get('hostname_ip_address', None)
    # port = definition.parameters.get('port', None)
    # username = definition.parameters.get('username', None)
    # password = definition.parameters.get('password', None)
    # component_type = definition.parameters.get('component_type', None)
    # component_name = definition.parameters.get('component_name', None)
    # test_type = definition.parameters.get('test_type', None)
    # test_name = definition.parameters.get('test_name', None)
    pass


def collect_events(helper, ew):

    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    opt_username = helper.get_arg('username')
    opt_password = helper.get_arg('password')
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
        "user": opt_username,
        "pwd": opt_password
    }
    body1 = {
        "componenttype": opt_component_type,
        "componentname": opt_component_name,
        "testtype": opt_test_type,
        "testname": opt_test_name
    }

    response = helper.send_http_request(url, method, parameters=None, payload=body1,
                                        headers=header1, cookies=None, verify=False, cert=None,
                                        timeout=None, use_proxy=True)
    r_json = response.json()

    r_status = response.status_code
    if (r_status != 200):
        # check the response status, if the status is not sucessful, raise requests.HTTPError
        response.raise_for_status()

    # To create a splunk event
    data = json.dumps(r_json)
    event = helper.new_event(data, time=None, host=None, index=None,
                             source=None, sourcetype=None, done=True, unbroken=True)
    ew.write_event(event)
