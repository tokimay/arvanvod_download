import findLink
import urllib.request, json
import os
import sys

url = str(sys.argv[1])
__output = ''
__m3u8_address = ''
__jsonLink = findLink.get(url)

for j in __jsonLink:
    __p = j.split('?')[1].split('.json')[0]
    __p = __p.split('=')[1]
    if not __p:
        continue
    with urllib.request.urlopen(str(__p) + '.json') as url:
        __data = json.load(url)
        __m3u8_address = __data['source'][0]['src']
        __output = __data['title']
    if not __m3u8_address:
        continue
    __output = __output.replace(" ", "_")

try:
    # print('get video from {}'.format(m3u8_address))
    os.system('ffmpeg -i {} -c copy -bsf:a aac_adtstoasc {}.mp4'.format(__m3u8_address, __output))
    print(f'file {os.path.dirname(os.path.realpath(__file__))}/{__output}.mp4 saved')
except Exception as er:
    print(f"{er}")