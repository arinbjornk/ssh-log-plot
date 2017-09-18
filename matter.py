import os
import binascii
import re
import urllib
import datetime
import time
import collections
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys


def tochunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# Get current external IP
# my_ip = urllib.urlopen('http://ident.me').read().decode('utf8')
# print(my_ip)

# Get list of all IPs in authentication log
with open('/var/log/auth.log', 'r') as f:
    output = f.read()
ip_log = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)

# Convert to counter to get frequencies of each IP
counter = collections.Counter(ip_log)
iplist = [[k, v] for k, v in counter.items()]

# Create batches of ip address queries
chunk = []
for item in iplist:
    chunk.append(json.dumps({'query': item[0]}))
batch = list(tochunks(chunk, 100))

sys.exit()

# Get lat an lon of each IP
coord = []
for i in range(len(iplist)):
    url = 'http://ip-api.com/json/' + str(iplist[i][0])
    response = urllib.urlopen(url).read().decode('utf-8')
    data = json.loads(response)
    # print(data['lat'])
    if(data['status'] == 'success'):
        coord.append([data['lat'], data['lon'], data['city'], 2 + (iplist[i][1] / 10)])
    if i % 130 == 0:  # To prevent api server block
        time.sleep(60)

# Create map
m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, resolution='l')
x, y = m([int(i[1]) for i in coord], [int(i[0]) for i in coord])
m.drawmapboundary(fill_color='w')
m.fillcontinents(color='#424242', lake_color='w')
m.scatter(x, y, [int(i[3]) for i in coord], marker='o', color='#FF5722', alpha=0.7, zorder=10)
plt.axis('off')
plt.savefig("now.svg", format='svg', transparent=True, bbox_inches='tight')

# Save in www folder
oldfilename = "connections_" + binascii.b2a_hex(os.urandom(6)) + ".svg"
os.rename("/var/www/logplots/now.svg", "/var/www/logplots/" + oldfilename)
os.rename("now.svg", "/var/www/logplots/now.svg")
