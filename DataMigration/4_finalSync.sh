#!/bin/bash

echo "Final sync..."
rsync -auvv --delete --include='/*/' --include='/*/colddb/***' --exclude='*' /opt/splunk/var/lib/splunk/ /data/splunk
echo "...Done"

