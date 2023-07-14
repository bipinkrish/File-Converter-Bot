import requests
import os

# setting
c4go = 'c4go'


def c2Go(cfile):
    cmd = f'{c4go} transpile {cfile}'
    os.system(cmd)
    gofile = cfile.split("/")[-1].replace(".c",".go")
    return gofile


def py2Many(pyfile,lang="cpp"):
    langs = ['cpp','rust','julia','kotlin','nim','dart','go']
    extensions = ['.cpp','.rs','.jl','.kt','.nim','.dart','.go']
    for i in range(len(langs)):
        if lang == langs[i]:
            ext = extensions[i]
  
    cmd = f'py2many --{lang}=1 {pyfile}'
    os.system(cmd)
    file = pyfile.replace(".py", ext)
    return file


def java2JSandTS(javacode,lang="JS"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'multipart/form-data; boundary=---------------------------373487287711602769823423273183',
        'Origin': 'https://sandbox.jsweet.org',
        'Connection': 'keep-alive',
        'Referer': 'https://sandbox.jsweet.org/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    data = f'-----------------------------373487287711602769823423273183\r\nContent-Disposition: form-data; name="javaCode"\r\n\r\n{javacode}\
    \r\n-----------------------------373487287711602769823423273183\r\nContent-Disposition: form-data; name="tid"\r\n\r\nbc21573e-c72e-4cf7-180d-c551256e2055\r\n-----------------------------373487287711602769823423273183\r\nContent-Disposition: form-data; name="tsout"\r\n\r\ntrue\r\n-----------------------------373487287711602769823423273183--\r\n'

    res = requests.post('https://sandbox.jsweet.org/transpile',  headers=headers, data=data).json()
    if res["success"] == True:
        if lang == "JS":
            return 1,res["jsout"]
        else:
            return 1,res["tsout"]
    else:
        return 0,res["errors"]
