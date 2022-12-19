# encoding = utf-8
import os
import sys
import time
import datetime
import json
import re
import traceback


def parseHostnamePort(nameList_string):
    """ Function to parse the string of hostname and port to list 
    Parameters
    ----------
    nameList_string : str
        A string of hostname and port separated by comma. "<hostname1>:<port1>,<hostname2>:<port2>,..."
    Returns
    -------
    cName_port_list : list
        A list of list where hostname and port are stored.
        [
            [hostname1, port1],
            [hostname2, port2], ...
        ]
    """
    assert nameList_string is not None, 'Hostname and Port is not provided.'
    cName_list = nameList_string.split(",")
    cName_list = list(dict.fromkeys(cName_list))  # remove duplicate name
    cName_port_list = [None] * len(cName_list)
    for i in range(0, len(cName_list), 1):
        cName_port_list[i] = cName_list[i].split(":")
    return cName_port_list


def httpReq(helper, URL, Method, Body, Header):
    """ Function for HTTP Request
    Parameters
    ----------
    helper : Splunk Add-on Builder helper function
    URL : str
    Method : str
    Body : dict
    Header : dict

    Returns
    -------
    HTTP Response Object
    """
    return helper.send_http_request(URL, Method, parameters=None, payload=Body, headers=Header, cookies=None, verify=False, cert=None, timeout=None, use_proxy=False)


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
    pattern = "^(TRGT)"
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


def format_SplkDat(fields, values):
    """
    Parameters
    ----------
    Returns
    -------
    """


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
                    # Parse the data and determine whether it's a header
                    # If it's a header parse as header else as data.
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
