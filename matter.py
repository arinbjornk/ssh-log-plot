import os
import re
import urllib.request
import collections
import json

# Get current external IP
my_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')
print(my_ip)

# Get list of all IPs in authentication log
with open('/var/log/auth.log', 'r') as f:
    output = f.read()
ip_log = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)

# Convert to counter to get frequencies of IPs
counter = collections.Counter(ip_log)
iplist = [[k, v] for k, v in counter.items()]

# Get lat an lon of each IP
coord = []
for i in range(len(iplist)):
    url = 'http://ip-api.com/json/' + str(iplist[i][0])
    response = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(response)
    # print(data['lat'])
    coord.append([data['lat'], data['lon']])

print(coord)
