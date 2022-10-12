#! /usr/bin/python3

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
