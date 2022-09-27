HeadersPars = {
    # "managerurl": "https://api.coindesk.com",
    "managerurl": "http://<IP address of the eG console:Port>",
    "user": "eG username or domain",
    "pwd": "Base64 encoded password"
}

showtestsdetails = {
    "rscPath": "/api/eg/orchestration/showtestsdetails",
    "Method": "POST",
    "Content-Type": "application/json",
    "Body": {
        "componenttype": "Component type",
        "componentname": "Component name",
        "testtype": "Performance / Configuration",
        "testname": "Test name"
    }
}

getAlerts = {
    # "rscPath": "/v1/bpi/currentprice.json",
    "rscPath": "/api/eg/analytics/getAlerts",
    "Method": "POST",
    "Content-Type": "application/json",
    "Body": {
        "type": "<zone/segment/service/componentType>",
        "name": "<comma-separated list of zone/segment/service/componentType"
    }
}