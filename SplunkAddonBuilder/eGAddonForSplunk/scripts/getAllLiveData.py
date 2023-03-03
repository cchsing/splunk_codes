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


def formatEvent(hostname, zone, metrics, tests, metricName, *dimension):
    event = "time=\"" + tests[list(tests.keys())[0]]['Last Measurement Time'] + "\" " + \
        "componentName=\"" + hostname + "\" " + \
        "componentType=\"" + zone + "\" " + \
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


def getDataLeaf(helper, ew, host, source, sourcetype, index, hostname, zone, metrics, tests, metricName, *dimension):
    for value in metrics:
        data = formatEvent(hostname, zone, metrics,
                           tests, metricName, *dimension)
        event = helper.new_event(
            host=host, source=source, index=index, sourcetype=sourcetype, data=data)
        ew.write_event(event)


def parseData(helper, ew, host, source, sourcetype, index, hostname, zone, data):
    for tests in data[0][list(data[0])[0]]:
        if (type(tests) == dict):
            # helper.log_debug(tests)
            for test in tests.items():
                for field, metrics in test[1].items():
                    if (type(metrics) == list):
                        if all(key in metrics[0] for key in ("State", "Value", "Unit")):
                            getDataLeaf(helper, ew, host, source, sourcetype,
                                        index, hostname, zone, metrics, tests, field)
                        else:
                            for name, metric in metrics[0].items():
                                if all(key in metric[0] for key in ("State", "Value", "Unit")):
                                    getDataLeaf(helper, ew, host, source, sourcetype, index, hostname,
                                                zone, metric, tests, name, field, metrics[0]['State'])


def zoneLookup(zone):
    # Lookup zone from host list to get zone in live measure
    lookup = {
        "Microsoft SQL": "MSSQL",
        "Microsoft SQL Cluster": "MSSQL",
        "Maria Database": "MariaDB",
        "Oracle Database": "Oracle",
        "Oracle Cluster": "Oracle",
        "Linux": "Linux",
        "Microsoft Windows": "Microsoft Windows",
        "MySQL": "MySQL",
        "Solaris": "Solaris",
        "DB2 UDB": "DB2"
    }
    return lookup[zone]


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
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    # --------------------------------------------------------------------------------------------------------
    url1 = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/analytics/getZoneMapping"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    method = "POST"
    header1 = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    body1 = {}
    url2 = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/analytics/getLiveMeasure"
    header2 = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    # body2 = {
    #     "servertype": component_type,
    #     "servername": component_name
    # }
    # --------------------------------------------------------------------------------------------------------
    try:
        response1 = helper.send_http_request(url1, method, parameters=None, payload=body1,
                                             headers=header1, cookies=None, verify=False, cert=None, timeout=None, use_proxy=False)
        r_status1 = response1.status_code
        if r_status1 != 200:
            response1.raise_for_status()
        else:
            zones = response1.json()
            for zone in zones:
                if (zone['zone'] == zoneLookup(opt_zone)):
                    zone_name = opt_zone
                    servers = zone['Server']
                    for server in servers:
                        body2 = {
                            "servertype": zone_name,
                            "servername": server
                        }
                        try:
                            response2 = helper.send_http_request(
                                url2, method, parameters=None, payload=body2, headers=header1, cookies=None, verify=False, cert=None, timeout=600, use_proxy=False)
                            r_status2 = response2.status_code
                            if r_status2 != 200:
                                response2.raise_for_status()
                            else:
                                LiveMeasure = response2.json()
                                parseData(helper, ew, opt_hostname_ip_address, source1,
                                          sourcetype1, index1, server, zone_name, LiveMeasure)
                        except Exception as e:
                            message1 = "Exception=" + "\"" + str(e) + "\""
                            helper.log_debug(message1)

    except Exception as e:
        message1 = "Exception=" + "\"" + str(e) + "\""
        helper.log_debug(message1)
