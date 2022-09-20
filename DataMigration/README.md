# Data Migration (rsync) - Some information or note:

1. dos2unix is used to change the file from windows file to unix format. Newline is different for Windows and causes error for the bash to run.

## From the forum -----------------------------

I would not suggest making any changes on a Indexer locally. Here is my suggestion:

Lets assume that the original Index is at /opt/splunk/var/lib/splunk/defaultdb, and the new location will be at /splunk/defaultdb.

In order to limit the down-time of each indexer to the minimum, we will do it in a few steps. First, while the service is still running, rsync the data from the old location to the new one:

Note: When running the rsync command, use a trailing slash only after the source path, and not after the destination path.

**_ Step 1 _**
rsync -auv /opt/splunk/var/lib/splunk/defaultdb/ /splunk/defaultdb.
This will create an initial copy of the data to the new location. The initial sync may take some time, depending on the size of your data, there also may be a lot of changes to the data when that process is done due to bucket rolling from hot/warm/cold.

**_ Step 2 _**
Now we want to do another rsync to send the recent changes, this will be a lot faster. But now we will add the --delete argument, so it deletes rolled buckets from the new location. like so:
rsync -auvv --delete /opt/splunk/var/lib/splunk/defaultdb/ /splunk/defaultdb
if you want to be able to look at what rsync did, you can send output to a log file by adding the --log-file=/tmp/rsync-`date %s`.out to the command.

**_ Step 3 _**
Put the CM in maintenance mode and stop Splunk, and do the final sync.
On the master:
$SPLUNK_HOME/bin/splunk enable maintenance-mode --answer-yes
On the Indexer:
$SPLUNK_HOME/bin/splunk stop

**_ Step 4 _**
Do the final sync:
rsync -auvv --delete /opt/splunk/var/lib/splunk/defaultdb/ /splunk/defaultdb

**_ Step 5 _**
Move away the old index data to a backup location:
mv /opt/splunk/var/lib/splunk/defaultdb /opt/splunk/var/lib/splunk/OLD.defaultdb

**_ Step 6 _**
Latstly, create a symlink from the new location to the old one:
ln -s /splunk/defaultdb /opt/splunk/var/lib/splunk/defaultdb.
Now you can start splunk, and not have to mess around with indexes.conf

**_ Step 7 _**
After you start the indexer, make sure that the buckets are visible by check the RF/SF on the CM, after that you can take the cluster out of maintenance mode, to fill in the few buckets that been rolled while that indexer was down.
$SPLUNK_HOME/bin/splunk disable maintenance-mode --answer-yes

Repeat the same process 1-7 on each indexer in the cluster, one indexer at a time.
After doing this on all indexers, you can change the path in indexes.conf on the master, and push out the new bundle.
A Indexer restart is required when changing the path of a index, so the master will initiate a restart.

After you did all that, and have confirmed that all the buckets are visible in Splunk, you can remove the old data, and delete the symlink:
rm -rf /opt/splunk/var/lib/splunk/OLD.defaultdb
rm /opt/splunk/var/lib/splunk/defaultdb

Please comment if I missed something.

## I hope this helps

---
