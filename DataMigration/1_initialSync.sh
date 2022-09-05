#!/bin/bash

echo "Executing initial sync..."
rsync -auv --include='/*/' --include='/*/colddb/***' --exclude='*' /opt/splunk/var/lib/splunk/ /data/splunk
echo "...Done"
