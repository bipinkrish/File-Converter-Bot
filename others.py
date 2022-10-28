from asteval import Interpreter
from io import StringIO
import arrow

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
**UTC** - __{utc.format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Athens** - __{utc.to('Europe/Athens').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Kolkata** - __{utc.to('Asia/Kolkata').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Maseru** - __{utc.to('Africa/Maseru').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Moscow** - __{utc.to('Europe/Moscow').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Melbourne** - __{utc.to('Australia/Melbourne').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**NewYork** - __{utc.to('America/New_York').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Shanghai** - __{utc.to('Asia/Shanghai').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
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
