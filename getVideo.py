import findLink
import urllib.request, json
import os
import sys


url = str(sys.argv[1])
output = ''
m3u8_address = ''
jsonLink = findLink.get(url)

for j in jsonLink:
    p = j.split('?')[1].split('.json')[0]
    p = p.split('=')[1]
    if not p:
        continue
    with urllib.request.urlopen(str(p) + '.json') as url:
        data = json.load(url)
        m3u8_address = data['source'][0]['src']
        output = data['title']
    if not m3u8_address:
        continue
    output = output.replace(" ", "_")

try:
    # print('get video from {}'.format(m3u8_address))
    os.system('ffmpeg -i {} -c copy -bsf:a aac_adtstoasc {}.mp4'.format(m3u8_address, output))
    print(f'file {os.path.dirname(os.path.realpath(__file__))}/{output}.mp4 saved')
except:
    print('Error')