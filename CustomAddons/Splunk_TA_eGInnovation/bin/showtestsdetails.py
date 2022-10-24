from __future__ import print_function

from configs import HeadersPars, showtestsdetails

import sys
import requests
import json


def main():
    API_ENDPOINT = HeadersPars['managerurl'] + showtestsdetails['rscPath']

    REQHEADER = HeadersPars
    REQHEADER['Content-Type'] = showtestsdetails['Content-Type']

    REQDATA = showtestsdetails['Body']

    try:
        DATA = requests.post(API_ENDPOINT, headers=REQHEADER, json=REQDATA)
        DATA_DICT = json.loads(DATA.text)
        sys.stdout.write(json.dumps(DATA_DICT, indent=4))
    except:
        sys.stderr.write(" %s Request to %s endpoint error." % (
            showtestsdetails['Method'], showtestsdetails['rscPath']))


if __name__ == "__main__":
    main()
