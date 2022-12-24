# Networker Add-on for Splunk Documentation

To document the design, development, and progress of the add-on.

Base URL: https://hostname:9090/nwrestapi/v3/global

## Endpoints

1. GET Returns a list of job groups with checkpointing done using the endTime of the job groups. - [get_jobgroups_1.py](./scripts/get_jobgroups_1.py)
2. GET Returns a list of jobs with checkpoint done using the endTime of the jobs - [get_jobs_1.py](./scripts/get_jobs_1.py)
3. GET Returns a list of job groups with parameters {query_filter} and {field_list_filter} - [get_jobgroups_2.py](./scripts/get_jobgroups_2.py)
4. GET Returns a list of job with parameters {query_filter} and {field_list_filter} - [get_jobs_2.py](./scripts/get_jobs_2.py)
5. GET Returns alerts with parameters {query_filter} and {field_list_filter} - [get_alerts_1.py](./scripts/get_alerts_1.py)
