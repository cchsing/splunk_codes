# To document the CLI used

### Validate configuration

1. SPLUNK_HOME/bin/splunk btool \<conf_file\> list
2. SPLUNK_HOME/bin/splunk show config \<conf_file\>
3. SPLUNK_HOME/bin/splunk btool check
4. SPLUNK_HOME/bin/splunk btool inputs list monitor:///var/log --debug

### Force reload after editing conf

1. https://servername:webport/debug/refresh
2. restart splunk to reload all conf
3. Splunk refresh only valid for standalone search head
