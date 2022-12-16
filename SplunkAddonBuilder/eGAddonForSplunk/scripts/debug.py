import os
import sys
import time
import datetime
import json
import re


def main():
    opt_component_name_list = "hostname1:22,hostname2:12,hostname4:111,hostname5:22,hostname4:21"
    cName_list = opt_component_name_list.split(",")
    # remove duplicates
    cName_list = list(dict.fromkeys(cName_list))
    cName_port_list = [None] * len(cName_list)
    for i in range(0, len(cName_list), 1):
        cName_port_list[i] = cName_list[i].split(":")
    print(json.dumps(cName_port_list, indent=4))


if __name__ == "__main__":
    main()
