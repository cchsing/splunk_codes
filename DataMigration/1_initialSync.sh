#!/bin/bash

echo "Executing initial sync..."
rsync -au -vvv --include='/*/' --include='/*/colddb/***' --exclude='*' /opt/splunk/var/lib/splunk/ /data/splunk
echo "...Done"
