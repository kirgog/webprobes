# webprobes
Request a website and send information into elasticsearch (status, response time, response size ...)

## Prerequisite

# apt-get update
    # apt-get install python-pip
    # pip install elasticsearch requests

## Install
    # mkdir -p /data/scripts/
    # cd /data/scripts/
    # git clone https://github.com/kirgog/webprobes

## Setup

    # vim /data/scripts/webprobes/config.py

    nodeName = Name of the node
    elasticServer = ip or fqdn for elasticsearch server
    elasticPort = port of elasticsearch server
    elasticIndex = Name of the index
    urlList = list of url to supervise 
      [0]: url
      [1]: timeout for responsiveness
      [2]: string to search

## Initialise

You just need to do that the first time to initialize elasticsearch index

    # /data/scripts/webprobes/webtime.py -m

## Use contab to automate probes
    # vim /etc/cron.d/webprobes

```
#
# WEBPROBES CRONTAB
#
* * * * * root /data/scripts/webprobes/webtime.py
```
    # service cron restart

You can also use an alternative user.
