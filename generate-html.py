#!/usr/bin/env python
#
# fetch the most recent pouchdb builds, update travis badges
#
# outputs the HTML to stdout
#

import requests

envs = {
  "CLIENT=node COMMAND=test": {
    "name": "Node.js",
    "adapter": "LevelDB",
    "note": "",
    "img": "nodejs_32x32.png"
  },
  "AUTO_COMPACTION=true CLIENT=node COMMAND=test": {
    "name": "Node.js",
    "adapter": "LevelDB",
    "note": "Using auto-compaction",
    "img": "nodejs_32x32.png"
  },
  "CLIENT=node SERVER=pouchdb-server COMMAND=test": {
    "name": "Node.js",
    "adapter": "LevelDB",
    "note": "Using PouchDB Server",
    "img": "nodejs_32x32.png"
  },
  "CLIENT=selenium:firefox COMMAND=test": {
    "name": "Firefox",
    "adapter": "IndexedDB",
    "note": "",
    "img": "firefox_32x32.png"
  },
  "AUTO_COMPACTION=true CLIENT=selenium:firefox COMMAND=test": {
    "name": "Firefox",
    "adapter": "IndexedDB",
    "note": "Using auto-compaction",
    "img": "firefox_32x32.png"
  },
  "CLIENT=selenium:firefox SERVER=pouchdb-server COMMAND=test": {
    "name": "Firefox",
    "adapter": "IndexedDB",
    "note": "Using PouchDB Server",
    "img": "firefox_32x32.png"
  },
  "CLIENT=saucelabs:chrome COMMAND=test": {
    "name": "Chrome",
    "adapter": "IndexedDB",
    "note": "",
    "img": "chrome_32x32.png"
  },
  "CLIENT=saucelabs:chrome:37 COMMAND=test": {
    "name": "Chrome",
    "adapter": "IndexedDB",
    "note": "Chrome 37",
    "img": "chrome_32x32.png"
  },
  "CLIENT=saucelabs:chrome ADAPTERS=websql COMMAND=test": {
    "name": "Chrome",
    "adapter": "WebSQL",
    "note": "",
    "img": "chrome_32x32.png"
  },
  "CLIENT=saucelabs:safari:6 COMMAND=test": {
    "name": "Safari",
    "adapter": "WebSQL",
    "note": "Safari 6",
    "img": "safari_32x32.png"
  },
  "CLIENT=\"saucelabs:iphone:7.1:OS X 10.9\" COMMAND=test": {
    "name": "iOS Safari",
    "adapter": "WebSQL",
    "note": "iOS 7.1",
    "img": "safari-ios_32x32.png"
  },
  "CLIENT=\"saucelabs:internet explorer:10:Windows 8\" COMMAND=test": {
    "name": "Internet Explorer",
    "adapter": "IndexedDB",
    "note": "IE 10 on Windows 8",
    "img": "internet-explorer_32x32.png"
  },
  "CLIENT=selenium:phantomjs ES5_SHIM=true COMMAND=test": {
    "name": "PhantomJS",
    "adapter": "WebSQL",
    "note": "",
    "img": "webkit_32x32.png"
  },
  "AUTO_COMPACTION=true CLIENT=selenium:phantomjs ES5_SHIM=true COMMAND=test": {
    "name": "PhantomJS",
    "adapter": "WebSQL",
    "note": "Using auto-compaction",
    "img": "webkit_32x32.png"
  },
  "SERVER_ADAPTER=memory LEVEL_ADAPTER=memdown SERVER=pouchdb-server COMMAND=test": {
    "name": "Node.js",
    "adapter": "MemDOWN",
    "note": "Using MemDOWN in PouchDB Server and on the client",
    "img": "nodejs_32x32.png"
  },
  "CLIENT=selenium:firefox ADAPTERS=memory COMMAND=test": {
    "name": "Firefox",
    "adapter": "MemDOWN",
    "note": "Using the in-memory plugin (pouchdb.memory.js)",
    "img": "firefox_32x32.png"
  },
  "CLIENT=selenium:firefox ADAPTERS=localstorage COMMAND=test": {
    "name": "Firefox",
    "adapter": "LocalStorage",
    "note": "Using the LocalStorage plugin (pouchdb.localstorage.js)",
    "img": "firefox_32x32.png"
  },
  "CLIENT=selenium:firefox ADAPTERS=idb-alt COMMAND=test": {
    "name": "Firefox",
    "adapter": "IndexedDB",
    "note": "Using the idb-alt plugin based on level.js (pouchdb.idb-alt.js)",
    "img": "firefox_32x32.png"
  },
  "CLIENT=node SERVER=couchdb-master COMMAND=test": {
   "name": "Node.js",
   "adapter": "MemDOWN",
   "note": "Using CouchDB master",
   "img": "nodejs_32x32.png" 
  },
  "CLIENT=selenium:firefox SERVER=couchdb-master COMMAND=test": {
    "name": "Firefox",
    "adapter": "IndexedDB",
    "note": "Using CouchDB master",
    "img": "firefox_32x32.png"
  }
}

def getResultImg(result):
  return 'passing.svg' if result == 0 else 'failing.svg' if result != None else 'unknown.svg'

builds = requests.get('https://api.travis-ci.org/pouchdb/pouchdb/builds?event_type=push').json();

last_build_id = builds[0]['id'];

status = requests.get('https://api.travis-ci.org/pouchdb/pouchdb/builds/' + str(last_build_id)).json();

print '''
<html>
  <head>
    <title>
      PouchDB build status
    </title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <table>
      <h1>PouchDB build status</h1>
      <h2>
        Build <a href='https://travis-ci.org/pouchdb/pouchdb/builds/%s'>#%s</a> 
        <a href='https://travis-ci.org/pouchdb/pouchdb'>
          <img alt="Build Status" src='https://travis-ci.org/pouchdb/pouchdb.svg'/>
        </a>
      </h2>
''' % (last_build_id, last_build_id)
for i in range(len(status['matrix'])):
  matrix = status['matrix'][i]
  job_id = matrix['id']
  try: 
    config = envs[matrix['config']['env']]
  except KeyError: 
    continue
  result = getResultImg(matrix['result'])
  print '''
  <tr>
    <td><img src="img/%s"/></td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>
      <a href="https://travis-ci.org/pouchdb/pouchdb/jobs/%s">
        <img src="img/%s"/>
      </a>
    </td>
  </tr>
  ''' % (config['img'], config['name'], config['adapter'], config['note'], job_id, result)

print '</table></body></html>'