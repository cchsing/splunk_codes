#!/bin/bash

curPath=$(pwd)
echo $curPath
if [ "$curPath" == "/opt/splunk/var/lib/splunk" ]; then
	# in the current/originating folder loop through the directories within
	for f in */; do
		# at the destination folder loop through directories with colddb and do
		for l in /data/splunk/*/colddb; do 
			if [[ "$l" == *"/$f"* && $f != 'splunk/' ]]; then
				# create symbolic link from $l destination to $f originating folder
				ln -s "${l}" "/opt/splunk/var/lib/splunk/${f}colddb"
				echo $f && ls $f
			fi
		done
	done
else
	echo "Please run the script in the SPLUNK_DB directory."
fi

#ln -s /data/splunk /opt/splunk/var/lib/splunk


