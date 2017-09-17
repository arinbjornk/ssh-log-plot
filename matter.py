import os
import re
import urllib
import collections
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Get current external IP
my_ip = urllib.urlopen('http://ident.me').read().decode('utf8')
print(my_ip)

# Get list of all IPs in authentication log
with open('/var/log/auth.log', 'r') as f:
    output = f.read()
ip_log = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)

# Convert to counter to get frequencies of each IP
counter = collections.Counter(ip_log)
iplist = [[k, v] for k, v in counter.items()]

# Get lat an lon of each IP
coord = []
for i in range(len(iplist)):
    url = 'http://ip-api.com/json/' + str(iplist[i][0])
    response = urllib.urlopen(url).read().decode('utf-8')
    data = json.loads(response)
    # print(data['lat'])
    coord.append([data['lat'], data['lon'], data['city'], 2 + (iplist[i][1] / 10)])

# Create map
m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, resolution='l')
x, y = m([int(i[1]) for i in coord], [int(i[0]) for i in coord])
m.drawmapboundary(fill_color='w')
m.fillcontinents(color='#424242', lake_color='w')
m.scatter(x, y, [int(i[3]) for i in coord], marker='o', color='#FF5722', alpha=0.7, zorder=10)
plt.savefig('image.svg', format='svg', bbox_inches='tight')
