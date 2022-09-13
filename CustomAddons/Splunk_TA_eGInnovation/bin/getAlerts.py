from __future__ import print_function

from configs import HeadersPars, getAlerts

import sys
import requests
import json
import time


def main():
    # define api endpoint
    API_ENDPOINT = HeadersPars['managerurl'] + getAlerts['rscPath']
    # print (API_ENDPOINT)

    # header for the request
    REQHEADER = HeadersPars
    REQHEADER['Content-Type'] = getAlerts['Content-Type']
    # print (reqHeader)

    # body for the request
    REQDATA = getAlerts['Body']
    # print (reqData)

    # http post request
    try:
        # DATA = requests.get(API_ENDPOINT)
        DATA = requests.post(API_ENDPOINT, headers=REQHEADER, json=REQDATA)
        DATA_DICT = json.loads(DATA.text)
        sys.stdout.write(json.dumps(DATA_DICT, indent=3))
    except:
        sys.stderr.write(" %s Request to %s endpoint error." % (
            getAlerts['Method'], getAlerts['rscPath']))


if __name__ == "__main__":
    main()
