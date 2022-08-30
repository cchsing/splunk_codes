#!/bin/bash

sudo -u splunk -H sh -c "cd ~;/opt/splunk/bin/splunk list peer-info > checkMainten.output"
cp /home/splunk/checkMainten.output ~
MaintenMode=$(cat ~/checkMainten.output | grep -oP 'maintenance_mode:\K\S+')
echo "Maintenance Mode:" $MaintenMode
if [[ $MaintenMode -eq 1 ]];
then
	echo "Cluster Master is in Maintenance Mode. Taking the current indexer offline..."
	sudo -u splunk -H sh -c "/opt/splunk/bin/splunk offline"
else
	echo "Cluster Master is NOT in Maintenance Mode. Abort operation..."
fi
