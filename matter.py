import os
import re
import urllib.request
import collections
import json

my_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')
print(my_ip)

with open('/var/log/auth.log', 'r') as f:
    output = f.read()
ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)

firstcounter = collections.Counter(ip)
counter = [[k, v] for k, v in firstcounter.items()]
# print(counter)
# print(counter[0][0])

for i in range(len(counter)):
    url = 'http://ip-api.com/json/' + str(counter[i][0])
    response = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(response)
    print(data['city'])
