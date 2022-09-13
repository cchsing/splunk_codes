from __future__ import print_function

from configs import HeadersPars, showtestsdetails

import sys
import requests
import json
import time


def main():
    # define api endpoint
    API_ENDPOINT = HeadersPars['managerurl'] + showtestsdetails['rscPath']
    # print (API_ENDPOINT)

    # header for the request
    REQHEADER = HeadersPars
    REQHEADER['Content-Type'] = showtestsdetails['Content-Type']
    # print (REQHEADER)

    # body for the request
    REQDATA = showtestsdetails['Body']
    # print (REQDATA)

    # http post request
    try:
        DATA = requests.post(API_ENDPOINT, headers=REQHEADER, json=REQDATA)
        DATA_DICT = json.loads(DATA.text)
        sys.stdout.write(json.dumps(DATA_DICT, indent=3))
    except:
        sys.stderr.write(" %s Request to %s endpoint error." % (
            showtestsdetails['Method'], showtestsdetails['rscPath']))


if __name__ == "__main__":
    main()
