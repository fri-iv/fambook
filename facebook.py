import httplib
import urllib2
import json

graph_url = "https://graph.facebook.com/2.9/me"

req = urllib2.Request('https://graph.facebook.com/v2.9/me')
req.add_header('Authorization', 'sdfs')
result = urllib2.urlopen(req)
print result
