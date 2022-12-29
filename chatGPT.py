from os import environ
from pyChatGPT import ChatGPT
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

Session_Token = environ.get("Session_Token", None)
if Session_Token != None: api = ChatGPT(Session_Token) 

def chatGPTget(question):
    if Session_Token == None: return "__chatGPT session is not set__"

    resp = api.send_message(question)
    return resp["message"]

