#!/usr/bin/python

#
# MODULES
#

import requests
import time
import re
import sys
import getopt
import socket
from Queue import Queue
from threading import Thread
import urllib3
from elasticsearch import Elasticsearch
from config import *

begin = time.time()

#
# VARIABLES
#

displayOnly = False
enclosure_queue = Queue()

#
# GLOBAL SETTINGS
#

urllib3.disable_warnings()

#
# READING ARGS
#

myopts, args = getopt.getopt(sys.argv[1:],"i,h,p")

#
# FUNCTIONS
#

def usage ():
  print("Usage : ")
  print("\t-h : display this help")
  print("\t-i : initialise elasticsearch index")
  print("\t-p : only display result instead of loading data into elasticsearch")
  sys.exit(0)

def getUrl (i,q):
  exception = False
  while True:
    tmp = q.get()
    url = tmp[0]
    timeout = tmp[1]
    string = tmp[2]
    try:
      nf = requests.get(url, timeout=5, verify=False)
    except requests.exceptions.RequestException as e:
      exception = True
    if exception:
      res = '{ "nodeName":"%s", "url":"%s", "status":%s, "responseTime":%d, "responseSize":0, "string":%i, "globalResponse":%i }' % (nodeName, url, "503", int(timeout*1000), False, False)
      if displayOnly == True:
        print(res)
      else:
        es.index(index = elasticIndex , doc_type = 'probe', body = res)
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
      if displayOnly:
        print(res)
      else:
        es.index(index = elasticIndex , doc_type = 'probe', body = res)
      # close connection
      nf.close()
    q.task_done()

def createMapping ():
  print("Creating elasticsearch index")
  # index settings
  settings = {
    "settings": {
      "number_of_shards": 4,
      "number_of_replicas": 2
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

#
# MAIN
#

# Set up some threads to fetch the enclosures
for i in range(num_fetch_threads):
    worker = Thread(target=getUrl, args=(i, enclosure_queue,))
    worker.setDaemon(True)
    worker.start()

# opening elastic connection
if displayOnly == False:
  es = Elasticsearch( hosts=[{'host': elasticServer, 'port': elasticPort}] )

# is nodeName empty
try:
  nodeName
except NameError:
  nodeName = socket.gethostname()

# Reading args
for o, a in myopts:
  if o == '-i':
    createMapping()
    sys.exit(0)
  elif o == '-h':
    usage()
  elif o == '-p':
    displayOnly = True
  else:
    usage()

for probe in urlList:
  #getUrl(probe[0],probe[1],probe[2])
  enclosure_queue.put([probe[0],probe[1],probe[2]])

# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
enclosure_queue.join()

# duration
end = time.time()
print("Duree totale : %s") % (end-begin)

if displayOnly == False:
  es.indices.refresh(index=elasticIndex)

# End
sys.exit(0)

