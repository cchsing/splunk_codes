#!/bin/bash

echo "Final sync..."
rsync -au -vvv --delete --include='/*/' --include='/*/colddb/***' --exclude='*' /opt/splunk/var/lib/splunk/ /data/splunk
echo "...Done"

