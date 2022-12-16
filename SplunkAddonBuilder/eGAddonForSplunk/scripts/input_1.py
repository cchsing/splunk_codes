
# encoding = utf-8

import os
import sys
import time
import datetime
import json
import re
import traceback

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''


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
    opt_component_name_and_test_port = helper.get_arg(
        'component_name_and_test_port')
    opt_category = helper.get_arg('category')
    opt_test_type = helper.get_arg('test_type')
    opt_checkpoint_initial_value = helper.get_arg('checkpoint_initial_value')

    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    stanza_name = helper.get_input_stanza_names()
    input_type = helper.get_input_type()

    # Get a list of tests for specified component type
    url1 = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/orchestration/showtests"
    method1 = "POST"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    header1 = {
        "managerurl": managerurl,
        "user": opt_username,
        "pwd": opt_password
    }
    body1 = {
        "componenttype": opt_component_type,
        "category": opt_category,
        "testtype": opt_test_type
    }
    url2 = "https://" + opt_hostname_ip_address + \
        ":" + opt_port + "/api/eg/analytics/getTestData"
    # ---------------------------------------------------------------------------------
    # FIRST API CALL for All TEST NAME
    response1 = helper.send_http_request(url1, method1, parameters=None, payload=body1,
                                         headers=header1, cookies=None, verify=False, cert=None,
                                         timeout=None, use_proxy=False)

    r_json1 = response1.json()
    if "enabledTests" in r_json1.keys():
        enabledTests = r_json1['enabledTests']
    if "disabledTests" in r_json1.keys():
        disabledTests = r_json1['disabledTests']

    r_status1 = response1.status_code
    if r_status1 != 200:
        response1.raise_for_status()

    # ---------------------------------------------------------------------------------

    cName_list = opt_component_name_and_test_port.split(",")
    # remove duplicates
    cName_list = list(dict.fromkeys(cName_list))
    cName_port_list = [None] * len(cName_list)
    for i in range(0, len(cName_list), 1):
        # event = helper.new_event(source=source1, index=index1, sourcetype=sourcetype1, data=str(cName_list[i]))
        # ew.write_event(event)
        cName_port_list[i] = cName_list[i].split(":")

    # ---------------------------------------------------------------------------------
    # CHECKPOINTING
    key = "startDate"
    endDate = datetime.datetime.now()
    endDate_str = endDate.strftime("%Y-%m-%d %H:%M:%S")
    # # Retrieve datetime checkpoint
    state = helper.get_check_point(key)
    if state is None:
        state = opt_checkpoint_initial_value
    # # Update the checkpoint
    helper.save_check_point(key, endDate_str)
    # helper.delete_check_point(key)

    # ---------------------------------------------------------------------------------

    # try:
    for test in enabledTests:
        for cName_port in cName_port_list:
            try:
                body2 = {
                    "test": test,
                    "host": cName_port[0],
                    "port": cName_port[1],
                    "lastmeasure": "false",
                    "startDate": state,
                    "endDate": endDate_str
                }
                response = helper.send_http_request(url2, method1, parameters=None, payload=body2,
                                                    headers=header1, cookies=None, verify=False, cert=None,
                                                    timeout=None, use_proxy=False)
                r_json = response.json()
                if len(r_json) > 1:
                    fields = r_json[0]
                    fields_list = fields.split()

                    data_raw = r_json[1:]

                    for row in data_raw:
                        if row != None:
                            try:
                                match = re.search(
                                    r"^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(.+)", row)
                                # event = helper.new_event(source=source1, index=index1, sourcetype=sourcetype1, data=match.group(7))
                                # ew.write_event(event)
                                output = ""
                                test_data = match.group(7).split()
                                for i in range(0, 6, 1):
                                    output += fields_list[i] + \
                                        "=" + match.group(i+1) + ","
                                for i in range(6, len(fields_list), 1):
                                    if (i == len(fields_list)-1):
                                        output += fields_list[i] + "=" + \
                                            test_data[i-6] + \
                                            ",test=\"" + test + "\""
                                    else:
                                        output += fields_list[i] + \
                                            "=" + test_data[i-6] + ","
                                event = helper.new_event(
                                    source=source1, index=index1, sourcetype=sourcetype1, data=output)
                                ew.write_event(event)
                            except Exception as e:
                                message1 = "Exception=" + "\"" + str(e) + "\"" + ",inputName=" + "\"" + stanza_name + "\"" + ",inputType=" + "\"" + input_type + "\"" + ",test=" + str(test) + ",componentName=" + "\"" + str(
                                    cName_port) + "\"" + ",length of json=" + str(len(r_json)) + ",json=" + json.dumps(r_json) + ",fields=" + str(fields) + ",allData=" + str(data_raw) + ",dataInThePipeline=" + str(row)
                                helper.log_info(message1)
                                message2 = "ExceptionInfo=" + \
                                    str(sys.exc_info())
                                helper.log_info(message2)
                                message3 = "Traceback=" + \
                                    str(traceback.format_exc())
                                helper.log_info(message3)
                                pass
                        else:
                            pass

                else:
                    fields = None
                    pass

            except Exception as e:
                message1 = "Exception=" + "\"" + str(e) + "\"" + ",inputName=" + "\"" + stanza_name + "\"" + ",inputType=" + "\"" + input_type + "\"" + ",test=" + str(
                    test) + ",componentName=" + "\"" + str(cName_port) + "\"" + ",HTTPResponse=" + "\"" + str(r_json) + "\""
                helper.log_info(message1)
                message2 = "ExceptionInfo=" + str(sys.exc_info())
                helper.log_info(message2)
                message3 = "Traceback=" + str(traceback.format_exc())
                helper.log_info(message3)
