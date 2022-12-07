# encoding = utf-8
import os
import sys
import time
import datetime
import json
import re


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # text = definition.parameters.get('text', None)
    pass


def collect_events(helper, ew):

    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    opt_username = helper.get_arg('username')
    opt_password = helper.get_arg('password')
    opt_component_type = helper.get_arg('component_type')
    opt_component_name = helper.get_arg('component_name')
    opt_category = helper.get_arg('category')
    opt_test_type = helper.get_arg('test_type')
    opt_test_port = helper.get_arg('test_port')
    opt_checkpoint_initial_value = helper.get_arg('checkpoint_initial_value')

    stanza_name = helper.get_input_stanza_names()

    url = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/orchestration/showtests"
    method = "POST"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    header1 = {"managerurl": managerurl,
               "user": opt_username,
               "pwd": opt_password}
    body1 = {"componenttype": opt_component_type,
             "category": opt_category,
             "testtype": opt_test_type}

    # Obtain test names by component
    response1 = helper.send_http_request(url, method, parameters=None, payload=body1,
                                         headers=header1, cookies=None, verify=False, cert=None,
                                         timeout=None, use_proxy=True)

    r_json1 = response1.json()
    enabledTests = r_json1['enabledTests']
    disabledTests = r_json1['disabledTests']
    r_status1 = response1.status_code
    if r_status1 != 200:
        response1.raise_for_status()

    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()

    for etest in enabledTests:

        key = "startDate"

        endDate = datetime.datetime.now()
        endDate_str = endDate.strftime("%Y-%m-%d %H:%M:%S")

        state = helper.get_check_point(key)
        if state is None:
            state = opt_checkpoint_initial_value
        # Update the checkpoint
        helper.save_check_point(key, endDate_str)
        # helper.delete_check_point(key)

        body2 = {
            "test": etest,
            "host": opt_component_name,
            "port": opt_test_port
        }
        response2 = helper.send_http_request(url, method, parameters=None, payload=body2,
                                             headers=header1, cookies=None, verify=False, cert=None,
                                             timeout=None, use_proxy=True)
        r_json2 = response2.json()
        fields = r_json2[0]
        fields_list = fields.split()
        data_raw = r_json2[1:]
        # Split the each row of data into list
        for row in data_raw:
            match = re.search(
                r"^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(.+)", row)
            # event = helper.new_event(source=source1, index=index1, sourcetype=sourcetype1, data=match.group(7))
            # ew.write_event(event)
            output = ""
            test_data = match.group(7).split()
            try:
                for i in range(0, 6, 1):
                    output += fields_list[i] + "=" + match.group(i+1) + ","
                for i in range(6, len(fields_list), 1):
                    if (i == len(fields_list)-1):
                        output += fields_list[i] + "=" + \
                            test_data[i-6] + ",test=" + etest
                    else:
                        output += fields_list[i] + \
                            "=" + test_data[i-6] + ","
                event = helper.new_event(
                    source=source1, index=index1, sourcetype=sourcetype1, data=output)
                ew.write_event(event)
            except:
                pass
