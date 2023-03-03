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
    pass


def formatEvent(metrics, tests, metricName, *dimension):
    event = "time=\"" + datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S') + \
        "\" " + "test=\"" + list(tests.keys())[0] + "\" "
    if (len(dimension) > 0):
        event = event + \
            "testInfo=\"" + dimension[0] + "\" " + \
            "testState=\"" + dimension[1] + "\" "

    event = event + \
        "metric_name=\"" + metricName + "\" " + \
        "State=\"" + metrics[0]['State'] + "\" " + \
        "Value=\"" + metrics[0]['Value'] + "\" " + \
        "Unit=\"" + metrics[0]['Unit'] + "\""
    return event


def getDataLeaf(helper, ew, host, source, sourcetype, index, metrics, tests, metricName, *dimension):
    for value in metrics:
        data = formatEvent(metrics, tests, metricName, *dimension)
        event = helper.new_event(
            host=host, source=source, index=index, sourcetype=sourcetype, data=data)
        ew.write_event(event)


def parseData(helper, ew, host, source, sourcetype, index, data):
    for tests in data[0][list(data[0])[0]]:
        if (type(tests) == dict):
            # helper.log_debug(tests)
            for test in tests.items():
                for field, metrics in test[1].items():
                    if (type(metrics) == list):
                        if all(key in metrics[0] for key in ("State", "Value", "Unit")):
                            getDataLeaf(helper, ew, host, source,
                                        sourcetype, index, metrics, tests, field)
                        else:
                            for name, metric in metrics[0].items():
                                if all(key in metric[0] for key in ("State", "Value", "Unit")):
                                    getDataLeaf(helper, ew, host, source, sourcetype, index,
                                                metric, tests, name, field, metrics[0]['State'])


def collect_events(helper, ew):
    global_account = helper.get_arg('global_account')
    username = global_account['username']
    password = global_account['password']
    password_base64 = base64.b64encode(
        bytes(f"{password}", "utf-8")).decode("ascii")
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    opt_server_type = helper.get_arg('server_type')
    opt_server_name = helper.get_arg('server_name')
    # --------------------------------------------------------------------------------------------------------
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    # ---------------------------------------------------------------------------------
    url = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/analytics/getLiveMeasure"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    method = "POST"
    header1 = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    body1 = {
        "servertype": opt_server_type,
        "servername": opt_server_name
    }
    # ---------------------------------------------------------------------------------
    try:
        response = helper.send_http_request(url, method, parameters=None, payload=body1,
                                            headers=header1, cookies=None, verify=False, cert=None, timeout=None, use_proxy=False)
        r_status = response.status_code
        if r_status != 200:
            response.raise_for_status()
        else:
            r_json = response.json()
            parseData(helper, ew, opt_hostname_ip_address,
                      source1, sourcetype1, index1, r_json)
            # event = helper.new_event(host=opt_hostname_ip_address, source=source1, index=index1, sourcetype=sourcetype1, data=json.dumps(r_json, indent=4))
            # ew.write_event(event)
    except Exception as e:
        message1 = "Exception=" + "\"" + str(e) + "\""
        helper.log_debug(message1)
