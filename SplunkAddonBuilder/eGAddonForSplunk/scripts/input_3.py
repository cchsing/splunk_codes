# encoding = utf-8
import os
import sys
import time
import datetime
import json
import re
import traceback


def hostnamePort_parsing(nameList_string):
    cName_list = nameList_string.split(",")
    cName_list = list(dict.fromkeys(cName_list))  # remove duplicate name
    cName_port_list = [None] * len(cName_list)
    for i in range(0, len(cName_list), 1):
        cName_port_list[i] = cName_list[i].split(":")
    return cName_port_list


def httpReq(helper, URL, Method, Body, Header):
    return helper.send_http_request(URL, Method, parameters=None, payload=Body, headers=Header, cookies=None, verify=False, cert=None, timeout=None, use_proxy=False)


def checkpoint(helper, initialValue):
    # CHECKPOINTING
    key = "startDate"
    endDate = datetime.datetime.now()
    endDate_str = endDate.strftime("%Y-%m-%d %H:%M:%S")
    # # Retrieve datetime checkpoint
    state = helper.get_check_point(key)
    if state is None:
        state = initialValue
    # # Update the checkpoint
    helper.save_check_point(key, endDate_str)
    # helper.delete_check_point(key)
    return state, endDate_str


def collect_events(helper, ew):
    # declare all variables
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
    # ---------------------------------------------------------------------------------
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    stanza_name = helper.get_input_stanza_names()
    input_type = helper.get_input_type()
    # ---------------------------------------------------------------------------------
    method1 = "POST"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    header1 = {
        "managerurl": managerurl,
        "user": opt_username,
        "pwd": opt_password
    }
    # ---------------------------------------------------------------------------------
    # showtests endpoint
    url1 = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/orchestration/showtests"
    body1 = {
        "componenttype": opt_component_type,
        "category": opt_category,
        "testtype": opt_test_type
    }
    # ---------------------------------------------------------------------------------
    # getTestData endpoint
    url2 = "https://" + opt_hostname_ip_address + \
        ":" + opt_port + "/api/eg/analytics/getTestData"
    # ---------------------------------------------------------------------------------
    # Query for All the Test Names
    response1 = httpReq(helper, url1, method1, body1, header1)
    r_status1 = response1.status_code
    if r_status1 == 200:
        r_json1 = response1.json()
        if "enabledTests" in r_json1.keys():
            enabledTests = r_json1['enabledTests']
        if "disabledTests" in r_json1.keys():
            disabledTests = r_json1['disabledTests']
    else:
        response1.raise_for_status()
    # ---------------------------------------------------------------------------------
    # Parse the Hostname and Port provided into List
    cName_port_list = hostnamePort_parsing(opt_component_name_and_test_port)
    # ---------------------------------------------------------------------------------
    # Checkpoint to avoid querying duplicate data
    state, endDate_str = checkpoint(helper, opt_checkpoint_initial_value)
    # ---------------------------------------------------------------------------------
    if len(enabledTests) > 0:
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
                    #
                except Exception as e:
                    message1 = "Exception=" + str(e)
                    message2 = "ExceptionInfo=" + str(sys.exc_info())
                    message3 = "Traceback=" + str(traceback.format_exc())
                    helper.log_debug(message1)
                    helper.log_debug(message2)
                    helper.log_debug(message3)

    else:
        message = "There is no test enabled for " + stanza_name
        helper.log_info(message)
