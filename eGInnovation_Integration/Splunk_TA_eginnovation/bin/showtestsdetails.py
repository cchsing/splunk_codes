from asyncio.windows_events import NULL
import sys
import requests
from configs import HeadersPars, showtestsdetails

def main():
    # define api endpoint
    API_ENDPOINT = HeadersPars['managerurl'] + showtestsdetails['rscPath']
    # print (API_ENDPOINT)

    # header for the request
    reqHeader = HeadersPars
    reqHeader['Content-Type'] = showtestsdetails['Content-Type']
    # print (reqHeader)

    # body for the request
    reqData = showtestsdetails['Body']
    # print (reqData)

    # http post request
    response = requests.post(API_ENDPOINT, headers=reqHeader, json=reqData)
    print(response.json)

if __name__ == "__main__":
    main()