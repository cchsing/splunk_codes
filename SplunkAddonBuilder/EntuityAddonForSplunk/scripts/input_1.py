# encoding = utf-8
import os
import sys
import time
import datetime
import json
import re
import traceback


def collect_events(helper, ew):
    opt_hostname_ip_address = helper.get_arg('hostname_ip_address')
