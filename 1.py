# Get the first 20 hits for: "Breaking Code" WordPress blog
from googlesearch import search
import urllib.request
from inscriptis import get_text
for url in search('"Breaking Code" WordPress blog', stop=1):
    print(url)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    print(html)
    print(get_text(html))
