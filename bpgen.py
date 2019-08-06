#!/usr/bin/env python3
import json
import os
from pprint import pprint

days = {}
circleInfos = {
  1: [], 2: [], 3: [], 4: []
}
artists = []
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


for i in range(1, 5):
  with open(os.path.join(__location__, 'lkrxy' + str(i) + '.json')) as f:
    days[i] = json.load(f)
    f.close()

with open(os.path.join(__location__, 'artist.url')) as f:
  lines = f.read().splitlines()
  f.close()
  
# pprint(lines)

for key, day in days.items():
  for circle in day:
    if not 'url' in circle:
      continue
    for url in circle['url']:
      for line in lines:
        if line == '' or line[0] == '#':
          lines.remove(line)
          continue
        arr = line.split()
        priority = 8
        artist = arr[0]
        if len(arr) >= 2:
          priority = arr[1]
        
        clean_artist = artist.lower().replace('http:', '').replace('https:', '').replace('//', '').strip()
        if clean_artist[0] == '@':
          clean_artist = clean_artist[1:]

        if clean_artist in url.lower().strip():
          circleInfos[key].append({
              'circle': circle, 
              'priority': priority
          })
          lines.remove(line)

data = {
  'c96sel1': [], 'c96sel2': [], 'c96sel3': [], 'c96sel4': []
}
# {"sel1":[{"loc":"1西よ35a","sc":"8"}]}
for key, circles in circleInfos.items():
  for circle in circles:
    # pprint(circle)
    data['c96sel' + str(key)].append({
      'loc': circle['circle']['loc'],
      'sc': circle['priority']
    })

with open(os.path.join(__location__, 'result.json'), 'w') as f:
  f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
  f.close()

print('Not found:')
pprint(lines)