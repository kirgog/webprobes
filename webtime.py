#!/usr/bin/python

# http://docs.python-requests.org/en/latest/api/

import requests
import time
from datetime import datetime
import re
import sys
import getopt
import socket
from elasticsearch import Elasticsearch
from config import *
import urllib3

# Disable verify warnings
urllib3.disable_warnings()

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"m")

# Functions
def getUrl (url,timeout,string):
  exception = False
  # Exception or not while getting url
  try:
    nf = requests.get(url, timeout=5, verify=False)
  except requests.exceptions.RequestException as e:
    exception = True
  if exception:
    res = '{ "nodeName":"%s", "url":"%s", "status":%s, "responseTime":%d, "responseSize":0, "string":%i, "globalResponse":%i }' % (nodeName, url, "503", int(timeout*1000), False, False)
    es.index(index = elasticIndex , doc_type = 'probe', body = res)
    print(res)
  else:
    # Results
    responseTime = int(nf.elapsed.total_seconds()*1000)
    if re.search(string, nf.text):
      stringResponse = True
    else:
      stringResponse = False
    if (responseTime < timeout*1000 and stringResponse ):
      globalResponse = True
    else:
      globalResponse = False
    # size
    responseSize = nf.headers.get('content-length', 0)
    res = '{ "nodeName":"%s", "url":"%s", "status":"%s", "responseTime":%d, "responseSize":%d, "string":%i, "globalResponse":%i }' % (nodeName, nf.url, nf.status_code, int(responseTime), int(responseSize), stringResponse, globalResponse)
    # close connection
    nf.close()
    es.index(index = elasticIndex , doc_type = 'probe', body = res)
    print(res)

def createMapping ():
  # index settings
  settings = {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    },
    "mappings": {
      "probe": {
        "_timestamp": { 
          "enabled": True
        },
        "properties": {
          "nodeName": {
            "type": "string"
          },
          "string": {
            "type": "boolean"
          },
          "responseTime": {
            "type": "short"
          },
          "responseSize": {
            "type": "short"
          },
          "globalResponse": {
            "type": "boolean"
          },
          "url": {
            "type": "string"
          },
          "status": {
            "type": "string"
          },
        }
      }
    }
  }
  # create index
  es.indices.create(index=elasticIndex, ignore=400, body=settings)

# opening elastic connection
es = Elasticsearch( hosts=[{'host': elasticServer, 'port': elasticPort}] )

# is nodeName empty
try:
  nodeName
except NameError:
  nodeName = socket.gethostname()

# Reading args
for o, a in myopts:
  if o == '-m':
    print('Creating mapping')
    createMapping()
    sys.exit(0)

for probe in urlList:
  getUrl(probe[0],probe[1],probe[2])

es.indices.refresh(index=elasticIndex)
sys.exit(0)

