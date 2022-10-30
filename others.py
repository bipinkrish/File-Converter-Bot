from asteval import Interpreter
from io import StringIO
import arrow
import base64


def maths(exp):
    output = StringIO()
    error = StringIO()
    aeval = Interpreter(writer=output,err_writer=error)
    aeval(f'x = {exp}')
    aeval('print(x)')
    res = output.getvalue()
    if res == "":
        return None
    else:
        return res
    

def timeanddate():
    utc = arrow.utcnow()
    return f"\
**UTC** __{utc.format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
**Athens** __{utc.to('Europe/Athens').format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
**Kolkata** __{utc.to('Asia/Kolkata').format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
**Maseru** __{utc.to('Africa/Maseru').format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
**Moscow** __{utc.to('Europe/Moscow').format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
**Melbourne** __{utc.to('Australia/Melbourne').format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
**NewYork** __{utc.to('America/New_York').format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
**Shanghai** __{utc.to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss ZZ')}__\n\
"
   

def pyrun(code):
    output = StringIO()
    error = StringIO()
    aeval = Interpreter(writer=output,err_writer=error)
    aeval(code)
    res = output.getvalue()
    if res == "":
        er = error.getvalue()
        if er == "":
            return "__Nothing is Printed to STDOUT__"
        else:
            return er
    else:
        return res


def b64e(string):
    return base64.b64encode(string.encode("ascii")).decode("ascii")


def b64d(string):
    return base64.b64decode(string.encode("ascii")).decode("ascii")


def b2img(data,name):
    ima = base64.b64decode(data.split('base64,')[-1])
    with open(name,"wb") as file:
            file.write(ima)
    return name


def img2b(file):
    with open(file, "rb") as ima:
        return base64.b64encode(ima.read()).decode('utf-8')
