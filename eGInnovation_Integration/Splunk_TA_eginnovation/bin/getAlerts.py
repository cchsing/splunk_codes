from __future__ import print_function

import sys, requests, configs, json, time

def main():
    # define api endpoint
    API_ENDPOINT = configs.HeadersPars['managerurl'] + configs.getAlerts['rscPath']
    # print (API_ENDPOINT)

    # header for the request
    REQHEADER = configs.HeadersPars
    REQHEADER['Content-Type'] = configs.getAlerts['Content-Type']
    # print (reqHeader)

    # body for the request
    REQDATA = configs.getAlerts['Body']
    # print (reqData)

    # http post request
    try: 
        # DATA = requests.get(API_ENDPOINT)
        DATA = requests.post(API_ENDPOINT, headers=REQHEADER, json=REQDATA)
        DATA_Dict = json.loads(DATA.text)
        sys.stdout.write(json.dumps(DATA_Dict, indent=3))
    except:
        sys.stderr.write("POST Request to getAlerts endpoint error. ")
        
if __name__ == "__main__":
    main()