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

def validate_input(helper, definition):
    pass


def collect_events(helper, ew):
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
    opt_port = helper.get_arg('port')

    URL1 = "https://"
