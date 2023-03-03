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


def collect_events(helper, ew):
    global_account = helper.get_arg('global_account')
    username = global_account['username']
    password = global_account['password']
    password_base64 = base64.b64encode(
        bytes(f"{password}", "utf-8")).decode("ascii")
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')
    # --------------------------------------------------------------------------------------------------------
    source1 = helper.get_input_stanza_names()
    index1 = helper.get_output_index()
    sourcetype1 = helper.get_sourcetype()
    # ---------------------------------------------------------------------------------
    url = "https://" + opt_hostname_ip_address + ":" + \
        opt_port + "/api/eg/analytics/getZoneMapping"
    managerurl = "https://" + opt_hostname_ip_address + ":" + opt_port
    method = "POST"
    header1 = {
        "managerurl": managerurl,
        "user": username,
        "pwd": password_base64
    }
    body1 = {}
    # ---------------------------------------------------------------------------------
    try:
        response = helper.send_http_request(url, method, parameters=None, payload=body1,
                                            headers=header1, cookies=None, verify=False, cert=None, timeout=None, use_proxy=False)
        r_status = response.status_code
        if r_status != 200:
            response.raise_for_status()
        else:
            r_json = response.json()
            for i in r_json:
                zone_name = i['zone']
                servers = i['Server']
                for server in servers:
                    output = "zone='{}',server='{}'".format(zone_name, server)
                    event = helper.new_event(
                        host=opt_hostname_ip_address, source=source1, index=index1, sourcetype=sourcetype1, data=output)
                    ew.write_event(event)
    except Exception as e:
        message1 = "Exception=" + "\"" + str(e) + "\""
        helper.log_debug(message1)
