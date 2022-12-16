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
    # hostname_ip_address = definition.parameters.get('hostname_ip_address', None)
    # port = definition.parameters.get('port', None)
    # username = definition.parameters.get('username', None)
    # password = definition.parameters.get('password', None)
    # component_name_list = definition.parameters.get('component_name_list', None)
    # test_name_list = definition.parameters.get('test_name_list', None)
    # checkpoint_initial_value = definition.parameters.get('checkpoint_initial_value', None)
    pass


def collect_events(helper, ew):

    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    opt_username = helper.get_arg('username')
    opt_password = helper.get_arg('password')
    opt_component_name_list = helper.get_arg('component_name_list')
    opt_test_name_list = helper.get_arg('test_name_list')
    opt_checkpoint_initial_value = helper.get_arg('checkpoint_initial_value')

    stanza_name = helper.get_input_stanza_names()
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()

    url1 = "https://" + opt_hostname_ip_address + \
        ":" + opt_port + "/api/eg/analytics/getTestData"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    method1 = "POST"
    header1 = {
        "managerurl": managerurl,
        "user": opt_username,
        "pwd": opt_password
    }

    cName_list = opt_component_name_list.split(",")
    # remove duplicates
    cName_list = list(dict.fromkeys(cName_list))
    cName_port_list = [None] * len(cName_list)
    for i in range(0, len(cName_list), 1):
        cName_port_list[i] = cName_list[i].split(":")

    tName_list = opt_test_name_list.split(",")

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

    try:
        for test in tName_list:
            for cName_port in cName_port_list:
                body1 = {
                    "test": test,
                    "host": cName_port[0],
                    "port": cName_port[1],
                    "lastmeasure": "false",
                    "startDate": state,
                    "endDate": endDate_str
                }
                response = helper.send_http_request(url1, method1, parameters=None, payload=body1,
                                                    headers=header1, cookies=None, verify=False, cert=None,
                                                    timeout=None, use_proxy=True)
                r_json = response.json()
                fields = r_json[0]
                fields_list = fields.split()
                data_raw = r_json[1:]
                for row in data_raw:
                    match = re.search(
                        r"^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(.+)", row)

                    output = ""
                    test_data = match.group(7).split()
                    for i in range(0, 6, 1):
                        output += fields_list[i] + "=" + match.group(i+1) + ","
                    for i in range(6, len(fields_list), 1):
                        if (i == len(fields_list)-1):
                            output += fields_list[i] + "=" + \
                                test_data[i-6] + ",test=\"" + test + "\""
                        else:
                            output += fields_list[i] + \
                                "=" + test_data[i-6] + ","
                    event = helper.new_event(
                        source=source1, index=index1, sourcetype=sourcetype1, data=output)
                    ew.write_event(event)

    except Exception as e:
        message = "Exception=" + str(e)
        helper.log_info(message)
