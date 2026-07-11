import urllib.request
import json

try:
    api_url = 'https://en.wikipedia.org/w/api.php?action=query&titles=File:DRDO-logo.png&prop=imageinfo&iiprop=url&format=json'
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        pages = data['query']['pages']
        page = next(iter(pages.values()))
        image_url = page['imageinfo'][0]['url']
        print('Found URL:', image_url)
        
        req2 = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req2) as resp2, open('assets/drdo_logo_clean.png', 'wb') as out_file:
            out_file.write(resp2.read())
        print('Download successful!')
except Exception as e:
    print('Error:', e)
