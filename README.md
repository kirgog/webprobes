# webprobes
Request a website and send information into elasticsearch (status, response time, response size ...)

## Prerequisite

# apt-get update
    # apt-get install python-pip
    # pip install elasticsearch requests

## Install
    # mkdir -p /data/scripts/webprobes
    # cd /data/scripts/webprobes
    # git pull https://github.com/kirgog/webprobes

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
