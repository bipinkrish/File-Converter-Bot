from os import environ
from threading import Semaphore
from pyChatGPT import ChatGPT
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

Session_Token = environ.get("Session_Token", None)
semaphore = Semaphore(1)

def chatGPTget(question):
    if Session_Token == None: return "__chatGPT session is not set__"

    semaphore.acquire()
    try:
        api = ChatGPT(Session_Token, verbose=True) 
        resp = api.send_message(question)
        api.clear_conversations()
        return resp["message"]
    except Exception as e:
        return e
    finally:
        semaphore.release()
