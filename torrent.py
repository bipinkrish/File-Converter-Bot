import requests
import os
from bs4 import BeautifulSoup
import hashlib
import urllib.parse
import bencode


def decodeurl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.url-encode-decode.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.url-encode-decode.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = { 'string': url, 'action': 'Decode'}
    response = requests.post('https://www.url-encode-decode.com/', headers=headers, data=data)
    soup = BeautifulSoup(response.text,"html.parser")
    return soup.find("textarea",id="string2").string


def getTorrent(maglink):
    id = maglink.split("magnet:?xt=urn:btih:")[1].split('&')[0]
    try:
        name = maglink.split('&dn=')[1].split("&tr=")[0]
        name = decodeurl(name) + ".torrent"
        name = "".join( x for x in name if (x.isalnum() or x in "._-@ "))
    except:
        name = id + ".torrent"
    os.system(f"wget https://itorrents.org/torrent/{id}.torrent")
    os.rename(f'{id}.torrent',name)
    return name


def getMagnet(filename):
    file = open(filename, "br")
    byte_stream = file.read()
    file.close()
    torrentdic = bencode.bdecode(byte_stream)

    result = []
    if "info" not in torrentdic:
        return ("No info dict in torrent file")
    encodedInfo = bencode.bencode(torrentdic["info"])
    sha1 = hashlib.sha1(encodedInfo).hexdigest()
    result.append("xt=urn:btih:"+sha1)

    if "name" in torrentdic["info"]:
        quoted = urllib.parse.quote(torrentdic["info"]["name"], safe="")
        result.append("dn="+quoted)

    trackers = []
    if "announce-list" in torrentdic:
        for urllist in torrentdic["announce-list"]:
            trackers += urllist
    elif "announce" in torrentdic:
        trackers.append(torrentdic["announce"])

    seen_urls = []
    for url in trackers:
        if [url] not in seen_urls:
            seen_urls.append([url])
            quoted = urllib.parse.quote(url, safe="")
            result.append("tr="+quoted)
    torrentdic["announce-list"] = seen_urls

    return "magnet:?" + "&".join(result)
