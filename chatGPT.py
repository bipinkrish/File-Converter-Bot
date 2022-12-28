from revChatGPT.ChatGPT import Chatbot
from os import environ

Session_Token = environ.get("Session_Token", None)
if Session_Token != None: chatbot = Chatbot({"session_token": Session_Token})
GPT = {}

def chatGPTget(question, prevResp=None):
    if Session_Token == None: return {"message":"__chatGPT session is not set__"}

    if prevResp == None:
        response = chatbot.ask(question, conversation_id=None, parent_id=None)
    else:
        response = chatbot.ask(
            question,
            conversation_id=prevResp["conversation_id"],
            parent_id=prevResp["parent_id"],
        )

    return response
