#!/bin/bash

echo "Update new database with recent changes using rsync..."
rsync -au -vvv --delete --include='/*/' --include='/*/colddb/***' --exclude='*' /opt/splunk/var/lib/splunk/ /data/splunk --log-file=/tmp/rsync-`date %s`.out
echo "...Done"
echo "Operation log written to /tmp/rsync*"
