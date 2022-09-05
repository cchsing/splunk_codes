#!/bin/bash

curPath=$(pwd)
echo $curPath
if [[ "${curPath}" == "/opt/splunk/var/lib/splunk" ]]; then
	for f in */colddb; do
        	if [ -d "${f}" ]; then
	                mv $f $f.OLD
                	echo "${f}"
        	fi
	done
else
	echo "Please run the script in the SPLUNK_DB directory."
fi
