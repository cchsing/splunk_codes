
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
    # component_test_name = definition.parameters.get('component_test_name', None)
    # component_host_name = definition.parameters.get('component_host_name', None)
    # component_test_port = definition.parameters.get('component_test_port', None)
    # checkpoint_initial_value = definition.parameters.get('checkpoint_initial_value', None)
    pass


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
    endDate_str = endDate.strftime("%Y-%m-%d %H:%M:%S")
    # # Retrieve datetime checkpoint
    state = helper.get_check_point(key)
    if state is None:
        state = initialValue
    # # Update the checkpoint
    helper.save_check_point(key, endDate_str)
    # helper.delete_check_point(key)
    return state, endDate_str


def isHeader(data):
    """ Function to check the first 4 characters of the data and determine the type of data (header or metrics)
    Parameters
    ----------
    data : str
        The data obtained from the REST API. Analyse for header or metrics data.
    Returns
    -------
    bool
        True - data is a header, False - data is metrics data. 
    """
    pattern = "^(TRGT_HOST)"
    return bool(re.match(pattern, data))


def parseHeaDat(data):
    """ Function to parse the data and return the header and metrics data. 
    Parameters
    ----------
    data : str
        The data obtained from the REST API.
    Returns
    -------
    hea : list
        The header of the data which is the attribute name or field name. 
    dat : list
        The body of the data which holds the corresponding value for the header.  
    """
    assert data is not None, "There is no data to parse. "
    hea = dat = []
    if isHeader(data):
        hea = data.split()
    else:
        match = re.search(
            r"^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(.+)", data)
        dat = []
        for i in range(1, 7, 1):
            dat.append(match.group(i))
        temp = match.group(7).split()
        dat = dat + temp
    return hea, dat


def splkData_format(fields, values):
    """ Function to format the data into string with the fields and values pair separated by comma. "<field1>=<value1>,<field2>=<value2>,...."
    Parameters
    ----------
    fields : list
        The attribute names / field names.
    values : list
        The value of the attribute / field.
    Returns
    -------
    splkData : str
        string data in format of "<field1>=<value1>,<field2>=<value2>,...."
    """
    assert len(fields) == len(values), "Fields and Values mismatched."
    splkData = ""

    for i in range(0, len(fields) - 1, 1):
        splkData += fields[i] + "=\"" + values[i] + "\","

    splkData += fields[len(fields) - 1] + \
        "=\"" + values[len(fields) - 1] + "\""

    return splkData


def collect_events(helper, ew):
    global_account = helper.get_arg('global_account')
    username = global_account['username']
    password = global_account['password']
    password_base64 = base64.b64encode(
        bytes(f"{password}", "utf-8")).decode("ascii")
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    # opt_username = helper.get_arg('username')
    # opt_password = helper.get_arg('password')
    opt_test_name = helper.get_arg('test_name')
    opt_component_name = helper.get_arg('component_name')
    # opt_component_test_port = helper.get_arg('component_test_port')
    opt_checkpoint_initial_value = helper.get_arg('checkpoint_initial_value')
    # --------------------------------------------------------------------------------------------------------
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    # --------------------------------------------------------------------------------------------------------
    # Checkpoint to avoid querying duplicate data
    state, endDate_str = checkpoint(helper, opt_checkpoint_initial_value)
    # ---------------------------------------------------------------------------------
    url = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/analytics/getTestData"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    method = "POST"
    header1 = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    body1 = {
        "test": opt_test_name,
        "orderby": "desc",
        "componentName": opt_component_name,
        "showData": "test",
        "lastmeasure": "false",
        "startDate": state,
        "endDate": endDate_str
    }
    # ---------------------------------------------------------------------------------
    try:
        response = helper.send_http_request(url, method, parameters=None, payload=body1,
                                            headers=header1, cookies=None, verify=False, cert=None,
                                            timeout=None, use_proxy=False)

        r_status = response.status_code
        if r_status != 200:
            response.raise_for_status()
        else:
            r_json = response.json()
            curFields = []
            curValues = []
            for row in r_json:
                fields, values = parseHeaDat(row)
                if len(fields) > 1:
                    curFields = fields
                if len(values) > 1:
                    curValues = values
                if len(curFields) == len(curValues):
                    output2Splk = splkData_format(curFields, curValues)
                    output2Splk += ",test=\"" + opt_test_name + "\""
                    event = helper.new_event(
                        host=opt_hostname_ip_address, source=source1, index=index1, sourcetype=sourcetype1, data=output2Splk)
                    ew.write_event(event)
                else:
                    continue
    except Exception as e:
        message1 = "Exception= " + "\"" + str(e) + "\""
        helper.log_debug(message1)
