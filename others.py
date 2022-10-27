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
        return error.getvalue()
    else:
        return res
    

def timeanddate():
    utc = arrow.utcnow()
    times = f"\
**UTC**                  __{utc.format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Africa/Maseru**        __{utc.to('Africa/Maseru').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**America/NewYork**      __{utc.to('America/New_York').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Asia/Kolkata**         __{utc.to('Asia/Kolkata').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Asia/Shanghai**        __{utc.to('Asia/Shanghai').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Australia/Melbournea** __{utc.to('Australia/Melbourne').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Europe/Athens**        __{utc.to('Europe/Athens').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
**Europe/Moscow**        __{utc.to('Europe/Moscow').format('YYYY-MM-DD  HH:mm:ss  ZZ')}__\n\
"
    return times



