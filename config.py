#!/usr/bin/python

#
# local settings
#
nodeName = 'webprobe1'

#
# elastic settings
#
elasticServer = '127.0.0.1'
elasticPort = 9200
elasticIndex = 'webprobes'

#
# url to supervise ( url, timeout, string to search)
#
urlList = [
  ['https://www.site1.fr/',2,'site1'],
  ['https://www.site2.fr/',2,'site2']
]

