import requests
import os
from bs4 import BeautifulSoup
import hashlib
import urllib.parse

# bencode #####

import collections

def bencode(elem):
    if type(elem) == str:
        elem = str.encode(elem)

    if type(elem) == bytes:
        result = str.encode(str(len(elem)))+b":"+elem
    elif type(elem) == int:
        result = str.encode("i"+str(elem)+"e")
    elif type(elem) == list:
        result = b"l"
        for item in elem:
            result += bencode(item)
        result += b"e"
    elif type(elem) in [dict, collections.OrderedDict]:
        result = b"d"
        for key in elem:
            result += bencode(key)+bencode(elem[key])
        result += b"e"
    return result

def bdecode(bytestr, recursiveCall=False):
    startingChars = dict({
            b"i" : int,
            b":" : str,
            b"l" : list,
            b"d" : dict
            })
    digits = [b"0", b"1", b"2", b"3", b"4", b"5", b"6", b"7", b"8", b"9"]

    started = ended = False
    curtype = None

    numstring = b"" # for str, int
    result = None   # for list, dict
    key = None      # for dict

    while len(bytestr) > 0:
        # reading and popping from the beginning
        char = bytestr[:1]

        if not started:

            bytestr = bytestr[1:]

            if char in digits:
                numstring += char

            elif char in startingChars:

                started = True
                curtype = startingChars[char]

                if curtype == str:
                    size = int(bytes.decode(numstring))
                    # try to decode strings
                    try:
                        result = bytes.decode(bytestr[:size])
                    except UnicodeDecodeError:
                        result = bytestr[:size]
                    bytestr = bytestr[size:]
                    ended = True
                    break

                elif curtype == list:
                    result = []

                elif curtype == dict:
                    result = collections.OrderedDict()
            else:
                raise ValueError("Expected starting char, got ‘"+bytes.decode(char)+"’")

        else: # if started

            if not char == b"e":

                if curtype == int:
                    bytestr = bytestr[1:]
                    numstring += char

                elif curtype == list:
                    item, bytestr = bdecode(bytestr, recursiveCall=True)
                    result.append(item)

                elif curtype == dict:

                    if key == None:
                        key, bytestr = bdecode(bytestr, recursiveCall=True)

                    else:
                        result[key], bytestr = bdecode(bytestr, recursiveCall=True)
                        key = None

            else: # ending: char == b"e"
                bytestr = bytestr[1:]
                if curtype == int:
                    result = int(bytes.decode(numstring))
                ended = True
                break
    if ended:
        if recursiveCall:
            return result, bytestr
        else:
            return result
    else:
        raise ValueError("String ended unexpectedly")

############

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


def getTorFile(maglink):
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
    torrentdic = bdecode(byte_stream)

    result = []
    if "info" not in torrentdic:
        return ("No info dict in torrent file")
    encodedInfo = bencode(torrentdic["info"])
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
