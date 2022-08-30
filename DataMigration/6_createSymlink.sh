#!/bin/bash

curPath=$(pwd)
echo $curPath
if [ "$curPath" == "/opt/splunk/var/lib/splunk" ]; then
	for f in */; do
		#mkdir test
		for l in /data/splunk/*/colddb; do
			if [[ "$l" == *"$f"* && $f != 'splunk/' ]]; then
				#echo "${l}"
				#echo "/opt/splunk/var/lib/splunk/${f}colddb"
				ln -s "${l}" "/opt/splunk/var/lib/splunk/${f}colddb"
			fi
		done
		#echo "${f}"
		#ls $f | grep 'colddb'
	done
else
	echo "Please run the script in the SPLUNK_DB directory."
fi

#ln -s /data/splunk /opt/splunk/var/lib/splunk


