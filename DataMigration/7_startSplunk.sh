#!/bin/bash

echo "Start the Splunkd service..."
sudo -u splunk -H sh -c "/opt/splunk/bin/splunk start"
echo "...Done. Proceed to disable the maintenance mode on Cluster Master."
