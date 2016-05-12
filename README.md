# webprobes
Request a website and send information into elasticsearch (status, response time, response size ...)

## Prerequisite

# apt-get update
    # apt-get install oython-pip
    # pip install elasticsearch requests

## Install
    # mkdir -p /data/scripts/webprobes
    # cd /data/scripts/webprobes
    # git pull https://github.com/kirgog/webprobes

## Use contab to automate probes
    # vim /etc/cron.d/uptime 

```
#
# UPTIME CRONTAB
#
* * * * * root /data/scripts/uptime/webtime.py
```

You can also use an alternative user.
