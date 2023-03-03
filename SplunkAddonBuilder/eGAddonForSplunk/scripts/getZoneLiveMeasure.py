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


def formatEvent(componentName, componentType, metrics, tests, metricName, *dimension):
    event = "time=\"" + tests[list(tests.keys())[0]]['Last Measurement Time'] + "\" " + \
        "componentName=\"" + componentName + "\" " + \
        "componentType=\"" + componentType + "\" " + \
        "test=\"" + list(tests.keys())[0] + "\" "

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


def getDataLeaf(helper, ew, host, source, sourcetype, index, componentName, componentType, metrics, tests, metricName, *dimension):
    for value in metrics:
        data = formatEvent(componentName, componentType, metrics,
                           tests, metricName, *dimension)
        event = helper.new_event(
            host=host, source=source, index=index, sourcetype=sourcetype, data=data)
        ew.write_event(event)


def parseData(helper, ew, host, source, sourcetype, index, componentName, componentType, data):
    for tests in data[0][list(data[0])[0]]:
        if (type(tests) == dict):
            # helper.log_debug(tests)
            for test in tests.items():
                for field, metrics in test[1].items():
                    if (type(metrics) == list):
                        if all(key in metrics[0] for key in ("State", "Value", "Unit")):
                            getDataLeaf(helper, ew, host, source, sourcetype,
                                        index, componentName, componentType, metrics, tests, field)
                        else:
                            for name, metric in metrics[0].items():
                                if all(key in metric[0] for key in ("State", "Value", "Unit")):
                                    getDataLeaf(helper, ew, host, source, sourcetype, index, componentName,
                                                componentType, metric, tests, name, field, metrics[0]['State'])


def collect_events(helper, ew):
    global_account = helper.get_arg('global_account')
    username = global_account['username']
    password = global_account['password']
    password_base64 = base64.b64encode(
        bytes(f"{password}", "utf-8")).decode("ascii")
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    opt_zone = helper.get_arg('zone')
    # --------------------------------------------------------------------------------------------------------
    source = helper.get_input_stanza_names()
    index = helper.get_output_index()
    sourcetype = helper.get_sourcetype()
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    method = "POST"
    header = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    timeout_60s = 60
    timeout_120s = 120
    timeout_240s = 240
    timeout_300s = 300
    # --------------------------------------------------------------------------------------------------------
    # Get the corresponding inventory information for component type and component name
    url2 = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/analytics/getZoneDetails"
    components_list = []
    body2 = {
        "zone": opt_zone
    }
    try:
        response2 = helper.send_http_request(url2,
                                             method,
                                             parameters=None,
                                             payload=body2,
                                             headers=header,
                                             cookies=None,
                                             verify=False,
                                             cert=None,
                                             timeout=timeout_60s,
                                             use_proxy=False)
        r_status2 = response2.status_code
        if r_status2 != 200:
            response2.raise_for_status()
        else:
            r_json2 = response2.json()
            for item in r_json2['Components']['Details']:
                components_list.append(item)
    except Exception as e:
        message2 = "Get Zone Details Failed for {}, Exception={}".format(
            opt_zone, str(e))
        helper.log_debug(message2)
    # --------------------------------------------------------------------------------------------------------
    url3 = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/analytics/getLiveMeasure"
    for component in components_list:
        body3 = {
            "servertype": component['type'],
            "servername": component['name']
        }
        try:
            response3 = helper.send_http_request(url3,
                                                 method,
                                                 parameters=None,
                                                 payload=body3,
                                                 headers=header,
                                                 cookies=None,
                                                 verify=False,
                                                 cert=None,
                                                 timeout=timeout_300s,
                                                 use_proxy=False)
            r_status3 = response3.status_code
            if r_status3 != 200:
                response3.raise_for_status()
            else:
                LiveMeasure = response3.json()
                parseData(helper,
                          ew,
                          opt_hostname_ip_address,
                          source,
                          sourcetype,
                          index,
                          component['name'],
                          component['type'],
                          LiveMeasure)
        except Exception as e:
            message3 = "Get Live Measures Failed for {}, {}, Exception={}".format(
                component['type'], component['name'], str(e))
            helper.log_debug(message3)
