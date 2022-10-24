from __future__ import print_function

from configs import *

import sys
import requests
import json


def main():

    API_ENDPOINT = BaseURL + getAlerts['rscPath']

    REQHEADER = HeadersPars
    REQHEADER['Content-Type'] = getAlerts['Content-Type']

    REQDATA = getAlerts['Body']

    try:
        DATA = requests.post(
            url=API_ENDPOINT, headers=REQHEADER, json=REQDATA, verify=False)
        DATA_DICT = json.loads(DATA.text)
        sys.stdout.write(json.dumps(DATA_DICT, indent=4))
    except requests.exceptions.RequestException as e:
        sys.stderr.write(" %s Request to %s endpoint error. HTTP Status Code: %s. Request Exception: %s" % (
            getAlerts['Method'], getAlerts['rscPath'], DATA.status_code, e))


if __name__ == "__main__":
    main()
