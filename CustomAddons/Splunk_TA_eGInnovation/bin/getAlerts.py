from __future__ import print_function

from configs import HeadersPars, getAlerts

import sys
import requests
import json


def main():
    # define api endpoint
    API_ENDPOINT = "https://10.111.33.10:7077" + getAlerts['rscPath']
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
        DATA = requests.post(
            url=API_ENDPOINT, headers=REQHEADER, json=REQDATA, verify=False)
        DATA_DICT = json.loads(DATA.text)
        sys.stdout.write(json.dumps(DATA_DICT, indent=4))
    except requests.exceptions.RequestException as e:
        sys.stderr.write(" %s Request to %s endpoint error. HTTP Status Code: %s. Request Exception: %s" % (
            getAlerts['Method'], getAlerts['rscPath'], DATA.status_code, e))


if __name__ == "__main__":
    main()
