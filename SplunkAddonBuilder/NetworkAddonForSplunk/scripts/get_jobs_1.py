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
    token = base64.b64encode(bytes(f"{username}:{password}","utf-8")).decode("ascii")
    return f'Basic {token}'

def checkpoint(helper, initialValue):
    """ Function for creating Checkpoint using the start and end datetime %Y-%m-%d %H:%M:%S
    Parameters
    ----------
    helper : Splunk Add-on Builder helper function
    initialValue : str
        The initial value for the checkpoint on the first run with empty checkpoint. Uses format "%Y-%m-%d %H:%M:%S"
    Returns
    -------
    state : str
        The start time or the previous checkpoint stored.
    endDate_str : str
        The end time or the new checkpoint updated. 
    """
    # CHECKPOINTING
    key = "startDate"
    endDate = datetime.datetime.now()
    endDate_str = endDate.strftime("%Y-%m-%dT%H:%M:%S")
    # # Retrieve datetime checkpoint
    state = helper.get_check_point(key)
    if state is None:
        state = initialValue
    # # Update the checkpoint
    helper.save_check_point(key, endDate_str)
    # helper.delete_check_point(key)
    return state, endDate_str

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # global_account = definition.parameters.get('global_account', None)
    pass

def collect_events(helper, ew):
    # Declare all variables for parameters
    opt_global_account = helper.get_arg('global_account')
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    opt_field_list_filter = helper.get_arg('field_list_filter')
    opt_checkpoint_initial_value = helper.get_arg('checkpoint_initial_value')
    username = opt_global_account['username']
    password = opt_global_account['password']
    # ---------------------------------------------------------------------------------
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    stanza_name = helper.get_input_stanza_names()
    input_type = helper.get_input_type()
    # ---------------------------------------------------------------------------------
    url1 = "https://" + opt_hostname_ip_address + ":" + opt_port + "/nwrestapi/v3/global/jobs"
    method1 = "GET"
    header1 = {
        "Authorization": basic_auth(username, password)
    }
    body1 = {}
    # ---------------------------------------------------------------------------------
    endTime_1, endTime_2 = checkpoint(helper, opt_checkpoint_initial_value)
    query_filter = f"q=endTime:['{endTime_1}' TO '{endTime_2}']"
    field_list_filter = f"fl={opt_field_list_filter}"
    parameters1 = f"?{query_filter}&{field_list_filter}"
    url1 += parameters1
    # ---------------------------------------------------------------------------------
    response1 = helper.send_http_request(url1, method1, parameters=None, payload=None, headers=header1, cookies=None, verify=False, cert=None, timeout=None, use_proxy=False)
    r_status1 = response1.status_code
    if r_status1 == 200:
        r_json1 = response1.json()
    else:
        response1.raise_for_status()
    if r_json1['count'] > 0:
        jobs_list = r_json1['jobs']
        for job in jobs_list:
            keys_list = list(job.keys())
            output = ""
            for key in keys_list:
            # keys = job.keys()
                output += str(key) + "=\"" + str(job[key]) + "\","
            output = output.rstrip(",")
            event = helper.new_event(source=source1, index=index1, sourcetype=sourcetype1, data=output)
            ew.write_event(event)
