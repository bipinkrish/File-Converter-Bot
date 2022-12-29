import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton

import os
import shutil
import threading
import pickle
import time
import random

from buttons import *
import aifunctions
import helperfunctions
import mediainfo
import guess
import tormag
import progconv
import others
import tictactoe
from chatGPT import *


# env
bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")


# bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)
os.system("chmod 777 c41lab.py negfix8 tgsconverter")


# main function to follow
def follow(message,inputt,new,old,oldmessage):
    output = helperfunctions.updtname(inputt,new)


    # ffmpeg videos audios
    if (output.upper().endswith(VIDAUD) or new == "gif") and inputt.upper().endswith(VIDAUD):

        print("It is VID/AUD option")

        file,msg = down(message)
        srclink = helperfunctions.videoinfo(file)
        cmd = helperfunctions.ffmpegcommand(file,output,new)

        if msg != None:
            app.edit_message_text(message.chat.id, msg.id, '__Converting__')

        os.system(cmd)
        os.remove(file)
        conlink = helperfunctions.videoinfo(output)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            caption=f'**Source File** : __{srclink}__\n\n**Converted File** : __{conlink}__'
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            up(message,output,msg,capt=caption)
        else:
            app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)
            
        if os.path.exists(output):
            os.remove(output)   


    # images
    elif output.upper().endswith(IMG) and inputt.upper().endswith(IMG):

        print("It is IMG option")
        file = app.download_media(message)
        srclink = helperfunctions.imageinfo(file)
        cmd = helperfunctions.magickcommand(file,output,new)
        os.system(cmd)
        conlink = helperfunctions.imageinfo(output)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, caption=f'**Source File** : __{srclink}\n\n**Converted File** : __{conlink}__', reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)

        if os.path.exists(output):
            os.remove(output) 

        if new == "ocr":
            cmd = helperfunctions.tesrctcommand(file,message.id)
            os.system(cmd)
            with open(f"{message.id}.txt","r") as ocr:
                text = ocr.read()
            os.remove(f"{message.id}.txt")
            if text != "":
                app.send_message(message.chat.id, text, reply_to_message_id=message.id)
            
        if new == "ico":
            slist = ["256", "128", "96", "64", "48", "32", "16"]
            for ele in slist:
                toutput = helperfunctions.updtname(inputt,f"{ele}.png")
                os.remove(toutput)
        
        os.remove(file)


    # stickers
    elif output.upper().endswith(IMG) and inputt.upper().endswith("TGS"):

        if new == "webp" or new == "gif" or new == "png":

            print("It is Animated Sticker option")
            file = app.download_media(message)
            srclink = helperfunctions.imageinfo(file)        
            os.system(f'./tgsconverter "{file}" "{new}"')
            os.remove(file)
            output = helperfunctions.updtname(file,new)
            conlink = helperfunctions.imageinfo(output)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, caption=f'**Source File** : __{srclink}\n\n**Converted File** : __{conlink}__', reply_to_message_id=message.id)
            else:
                app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)

            if os.path.exists(output):
                os.remove(output) 
            
        else:
            app.send_message(message.chat.id,"__Only Availble Conversions for Animated Stickers are **GIF, PNG** and **WEBP**__", reply_to_message_id=message.id)


    # ebooks
    elif output.upper().endswith(EB) and inputt.upper().endswith(EB):

        print("It is Ebook option")
        file = app.download_media(message)
        cmd = helperfunctions.calibrecommand(file,output)
        os.system(cmd)
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id, document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)
            
        if os.path.exists(output):
            os.remove(output) 


    # libreoffice documents
    elif (output.upper().endswith(LBW) and inputt.upper().endswith(LBW)) or (output.upper().endswith(LBI) and inputt.upper().endswith(LBI)) or (output.upper().endswith(LBC) and inputt.upper().endswith(LBC)):
        
        print("It is LibreOffice option")
        file = app.download_media(message)
        cmd = helperfunctions.libreofficecommand(file,new)
        os.system(cmd)
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)
        
        if os.path.exists(output):
            os.remove(output) 


    # fonts
    elif output.upper().endswith(FF) and inputt.upper().endswith(FF):
        
        print("It is FontForge option")
        file = app.download_media(message)
        cmd = helperfunctions.fontforgecommand(file,output,message)
        os.system(cmd)
        os.remove(f"{message.id}-convert.pe")
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)
            
        if os.path.exists(output):
            os.remove(output) 

    
    # subtitles
    elif output.upper().endswith(SUB) and inputt.upper().endswith(SUB):

        if not ((old.upper() in ["TTML", "SCC", "SRT"]) and (new.upper() in ["TTML","SRT", "VTT"])):
            app.send_message(message.chat.id,f"__**{old.upper()}** to **{new.upper()}** is not Supported.\n\n**Supported Formats**\n**Inputs**: TTML, SCC & SRT\n**Outputs**: TTML, SRT & VTT__", reply_to_message_id=message.id)

        else:
            print("It is Subtitles option")
            file = app.download_media(message)
            cmd = helperfunctions.subtitlescommand(file,output)
            os.system(cmd)
            os.remove(file)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
            else:
                app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)
                
            if os.path.exists(output):
                os.remove(output)


    # programs
    elif output.upper().endswith(PRO) and inputt.upper().endswith(PRO):

        flag = 0
        if ((old.upper() == "C") and (new.upper() == "GO")):
            flag = 1

        elif ((old.upper() == "PY") and (new.upper() in ['CPP','RS','JL','KT','NIM','DART','GO'])):
            flag = 2
            extens = ['CPP','RS','JL','KT','NIM','DART','GO']
            langs = ['cpp','rust','julia','kotlin','nim','dart','go']
            for i in range(len(langs)):
                if new.upper() == extens[i]:
                    lang = langs[i]

        elif ((old.upper() == "JAVA") and (new.upper() in ["JS","TS"])):
            flag = 3
            lang = new.upper()

        if not flag:
            app.send_message(message.chat.id,f"__**{old.upper()}** to **{new.upper()}** is not Supported.\n\
            \n**Supported Formats:**\nC -> GO\nPY -> CPP, RS, JL, KT, NIM, DART & GO\nJAVA -> JS & TS__", reply_to_message_id=message.id)

        else:
            print("It is Programs option")
            file = app.download_media(message)

            if flag == 1:
                output = progconv.c2Go(file)
            elif flag == 2:
                output = progconv.py2Many(file,lang)
            elif flag == 3:
                with open(file,"r") as jfile:
                    javacode = jfile.read()
                info = progconv.java2JSandTS(javacode,lang)
                if info[0] == 1:
                    with open(output,"w") as pfile:
                        pfile.write(info[1])
                else:
                    errormessage = ""
                    for ele in info[1]:
                        errormessage = errormessage + ele + "\n"

            os.remove(file)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
            else:
                if flag != 3:
                    errormessage = "Error while Conversion"
                app.send_message(message.chat.id,f"__{errormessage}__", reply_to_message_id=message.id)
                
            if os.path.exists(output):
                os.remove(output)


    # 3D files
    elif output.upper().endswith(T3D) and inputt.upper().endswith(T3D):

        if (old.upper() == "WRL"):
            app.send_message(message.chat.id,f"__**{old.upper()}** is Export Only, cannot be used to Convert from__", reply_to_message_id=message.id)

        else:
            print("It is 3D files option")
            file = app.download_media(message)
            cmd = helperfunctions.ctm3dcommand(file,output)
            os.system(cmd)
            os.remove(file)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
            else:
                app.send_message(message.chat.id,"__Error while Conversion__", reply_to_message_id=message.id)
                
            if os.path.exists(output):
                os.remove(output)


    # or else
    else:
        app.send_message(message.chat.id,"__Choose a Valid Extension, don't Type it__", reply_to_message_id=message.id)


    # deleting message    
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# negative to positive
def negetivetopostive(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    print("using c41lab")
    os.system(f'./c41lab.py "{file}" "{output}"')
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **c41lab**", reply_to_message_id=message.id)
    os.remove(output)
    
    print("using simple tool")
    aifunctions.positiver(file,output)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **simple tool**", reply_to_message_id=message.id)
    os.remove(output)
    
    print("using negfix8")
    os.system(f'./negfix8 "{file}" "{output}"')
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **negfix8**", reply_to_message_id=message.id)
    os.remove(output)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# color image
def colorizeimage(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    aifunctions.deoldify(file,output)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **Deoldify**", reply_to_message_id=message.id)
    os.remove(output)

    aifunctions.colorize_image(output,file)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **simple tool**", reply_to_message_id=message.id)
    os.remove(output)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# dalle
def genrateimages(message,prompt):
    
    # requsting
    # mdhash = aifunctions.mindalle(prompt,AutoCall=False) # min dalle
    # ldhash = aifunctions.latdif(prompt,AutoCall=False) # latent 
    filelist = aifunctions.dallemini(prompt) # dalle mini
    # latfile = aifunctions.latentdiff(prompt) # latent direct
    # imagelist = aifunctions.latdifstatus(ldhash,prompt) # latent get
    # mdfile = aifunctions.mindallestatus(mdhash,prompt) # min dalle get
    # sdhash = aifunctions.stablediff(prompt,AutoCall=False) # stable diff
    # sdfile = aifunctions.stablediffstatus(sdhash,prompt) # stable diff get

    # dalle mini
    app.send_message(message.chat.id,"**DALLE MINI**", reply_to_message_id=message.id)
    for ele in filelist:
        app.send_document(message.chat.id,document=ele,force_document=True)
        os.remove(ele)
    os.rmdir(prompt)

    # stable diffusion
    # if sdfile !=  None:
    #     app.send_message(message.chat.id,"**STABLE DIFFUSION**", reply_to_message_id=message.id)
    #     app.send_document(message.chat.id,document=sdfile,force_document=True)
    #     os.remove(sdfile)

    # latent diffusion
    # app.send_message(message.chat.id,f"__LATENT DIFFUSION :__ **{prompt}**", reply_to_message_id=message.id)
    # app.send_document(message.chat.id,document=latfile,force_document=True)
    # os.remove(latfile)
    # for ele in imagelist:
        # app.send_document(message.chat.id,document=ele,force_document=True)
        # os.remove(ele)
        
    # min dalle
    # app.send_message(message.chat.id,f"__MIN-DALLE :__ **{prompt}**", reply_to_message_id=message.id)
    # app.send_document(message.chat.id,document=mdfile,force_document=True)
    # os.remove(mdfile)

    # delete msg
    app.delete_messages(message.chat.id,message_ids=[message.id+1])


# cog video
def genratevideos(message,prompt):

    hash, queuepos = aifunctions.cogvideo(prompt,AutoCall=False)
    msg = app.send_message(message.chat.id,f"**Prompt received and Request is sent. Expected waiting time is {(queuepos+1)*3} mins**", reply_to_message_id=message.id)

    file = aifunctions.cogvideostatus(hash,prompt)
    app.send_video(message.chat.id, video=file, reply_to_message_id=message.id) #,caption=f"COGVIDEO : {prompt}")
    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[msg.id])


# delete msg
def dltmsg(umsg,rmsg,sec=15):
    time.sleep(sec)
    app.delete_messages(umsg.chat.id,message_ids=[umsg.id,rmsg.id])


# read file
def readf(message,oldmessage):
    file = app.download_media(message)
    
    try:
        with open(file,"r") as rf:
            txt = rf.read()
        n = 4096
        split = [txt[i:i+n] for i in range(0, len(txt), n)]

        if len(split) > 10:
            app.send_message(message.chat.id, "__File Contents is too Long__", reply_to_message_id=message.id)
            return

        for ele in split:
            app.send_message(message.chat.id, ele, disable_web_page_preview=True, reply_to_message_id=message.id)
            time.sleep(3)   
    except:
            app.send_message(message.chat.id, "__Error in Reading File__", reply_to_message_id=message.id)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# send video
def sendvideo(message,oldmessage):
    file, msg = down(message)
    thumb,duration,width,height = mediainfo.allinfo(file)
    up(message, file, msg, video=True, capt=f'**{file.split("/")[-1]}**' ,thumb=thumb, duration=duration, height=height, widht=width)

    app.delete_messages(message.chat.id, message_ids=[oldmessage.id])
    os.remove(file)


# send document
def senddoc(message,oldmessage):
    file, msg = down(message)
    up(message, file, msg)

    app.delete_messages(message.chat.id, message_ids=[oldmessage.id])
    os.remove(file)


# send photo
def sendphoto(message,oldmessage):
    file = app.download_media(message)
    app.send_photo(message.chat.id, photo=file, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)


# extract file
def extract(message,oldm):
    file, msg = down(message)
    cmd,foldername,infofile = helperfunctions.zipcommand(file,message)
    if msg != None:
        app.edit_message_text(message.chat.id, msg.id, '__Extracting__')
    os.system(cmd)
    os.remove(file)

    with open(infofile, 'r') as f:
        lines = f.read()
    last = lines.split("Everything is Ok\n\n")[-1].replace("      ","")
    os.remove(infofile)

    if os.path.exists(foldername):
        dir_list = helperfunctions.absoluteFilePaths(foldername)
        if len(dir_list) > 30:
            if msg != None:
                app.delete_messages(message.chat.id,message_ids=[msg.id])
            app.send_message(message.chat.id, f"__Number of files is **{len(dir_list)}** which is more than the limit of **30**__", reply_to_message_id=message.id)     
        else:
            for ele in dir_list:
                if os.path.getsize(ele) > 0:
                    up(message, ele, msg, multi=True)
                    os.remove(ele)
                else:
                    app.send_message(message.chat.id, f'**{ele.split("/")[-1]}** __is Skipped because it is 0 bytes__', reply_to_message_id=message.id)
            
            app.delete_messages(message.chat.id,message_ids=[msg.id])
            app.send_message(message.chat.id, f'__{last}__', reply_to_message_id=message.id)

        shutil.rmtree(foldername)
    else:
        app.send_message(message.chat.id, "**Unable to Extract**", reply_to_message_id=message.id)

    app.delete_messages(message.chat.id, message_ids=[oldm.id])


# getting magnet
def getmag(message,oldm):
    file = app.download_media(message)
    maglink = tormag.getMagnet(file)
    app.send_message(message.chat.id, f'__{maglink}__', reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldm.id])
    os.remove(file)


# getting tor file
def gettorfile(message,oldm):
    file = tormag.getTorFile(message.text)
    app.send_document(message.chat.id, file, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldm.id])
    os.remove(file)


# compiling
def compile(message,oldm):
    ext = message.document.file_name.split(".")[-1]

    # jar compilation
    if ext.upper() == "JAR":
        file = app.download_media(message)
        cmd,folder,files = helperfunctions.warpcommand(file,message)
        os.system(cmd)
        if not os.path.exists(folder):
            cmd,folder,files = helperfunctions.warpcommand(file,message,True)
            os.system(cmd)

        os.remove(file)
        if os.path.exists(folder):
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            for ele in files:
                if os.path.exists(ele) and os.path.getsize(ele) > 0:
                    app.send_document(message.chat.id,document=ele, force_document=True, reply_to_message_id=message.id)
                os.remove(ele)
            shutil.rmtree(folder)
        else:
            app.send_message(message.chat.id,"__Error while Compiling__", reply_to_message_id=message.id)


    # c and c++ compilation
    elif ext.upper() in ['C','CPP']:
        file = app.download_media(message)
        cmd,output = helperfunctions.gppcommand(file)
        os.system(cmd)
        os.remove(file)
        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_document(message.chat.id,document=output, caption="__Linux Executable__", force_document=True, reply_to_message_id=message.id)
            os.remove(output)
        else:
            app.send_message(message.chat.id,"__Error while Compiling__", reply_to_message_id=message.id)
        

    # python compile
    if ext.upper() == "PY":
        file = app.download_media(message)
        cmd, output, ofold, tfold, temp = helperfunctions.pyinstallcommand(message,file)
        os.system(cmd)
        os.remove(file)
        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_document(message.chat.id,document=output, caption="__Linux Executable__", force_document=True, reply_to_message_id=message.id)
            os.remove(output)
        else:
            app.send_message(message.chat.id,"__Error while Compiling__", reply_to_message_id=message.id)
        
        if os.path.exists(temp):
            os.remove(temp)
        if os.path.exists(ofold):
            shutil.rmtree(ofold)
        if os.path.exists(tfold):
            shutil.rmtree(tfold)


    # not supported yet
    else:
        app.send_message(message.chat.id,"__At this time Compilation only supports from JAR, PY, C and CPP Files__", reply_to_message_id=message.id)


    # delete message
    app.delete_messages(message.chat.id,message_ids=[oldm.id])


# running a program
def runpro(message,oldm):
    ext = message.document.file_name.split(".")[-1]

    # python run
    if ext.upper() == "PY":
        file = app.download_media(message)
        code = open(file,"r").read()
        os.remove(file)
        info = others.pyrun(code)
        app.send_message(message.chat.id, info, reply_to_message_id=message.id)
        app.delete_messages(message.chat.id,message_ids=[oldm.id])
        

    # not supported yet
    else:
        app.send_message(message.chat.id,"__At this time Running only supports from PY Files__", reply_to_message_id=message.id)


# scanning
def scan(message,oldm):
    file = app.download_media(message)
    info = helperfunctions.scanner(file)
    app.send_message(message.chat.id,f"__{info}__", reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldm.id])
    os.remove(file)


# make file
def makefile(message,mtext,oldmessage):
    text = mtext.split("\n")
    if len(text) == 1:
        app.send_message(message.chat.id, "__Make-File takes First line of your Text as Filename and File content will start from Second line__", reply_to_message_id=message.id)
        return

    firstline = text[0]
    firstline = "".join( x for x in firstline if (x.isalnum() or x in "._-@ "))
    text.remove(text[0])
    
    mtext = ""
    for ele in text: 
        mtext = mtext + f"{ele}\n"
    
    with open(firstline,"w") as file:
        file.write(mtext)

    if os.path.exists(firstline) and os.path.getsize(firstline) > 0:
        app.send_document(message.chat.id, document=firstline, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, "__Error while making file__", reply_to_message_id=message.id)

    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(firstline)      	    


# transcript speech to text
def transcript(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
    output = helperfunctions.updtname(inputt,"wav")
    temp = helperfunctions.updtname(inputt,"txt")
        
    if file.endswith("wav"):
        aifunctions.splitfn(file,message,temp)
    else:
        cmd = helperfunctions.ffmpegcommand(file,output,"wav")
        os.system(cmd)
        aifunctions.splitfn(output,message,temp)
        os.remove(output)

    if os.path.getsize(temp) > 0:
        app.send_document(message.chat.id, document=temp,caption="**Google Engine**", reply_to_message_id=message.id)
    os.remove(temp)

    data = aifunctions.whisper(file)
    with open(temp,"w") as wfile:
        wfile.write(data)
    if os.path.getsize(temp) > 0:
        app.send_document(message.chat.id, document=temp,caption="**OpenAI Engine** __(whisper)__", reply_to_message_id=message.id)
    os.remove(temp)

    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)
    

# chat gpt
def chatai(qes,message,msg):
    ans = chatGPTget(qes)
    app.edit_message_text(message.chat.id, msg.id, ans, disable_web_page_preview=True)


# text to speech 
def speak(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
    output = helperfunctions.updtname(inputt,"mp3")
   
    aifunctions.texttospeech(file,output)
    os.remove(file)

    app.send_document(message.chat.id, document=output, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(output)


# upscaling
def increaseres(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
   
    aifunctions.upscale(file,inputt)
    os.remove(file)

    app.send_document(message.chat.id, document=inputt, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(inputt)


# renaming
def rname(message,newname,oldm):
    app.delete_messages(message.chat.id,message_ids=[message.id+1])
    file, msg = down(message)
    os.rename(file,newname)
    up(message, newname, msg)
    app.delete_messages(message.chat.id,message_ids=[oldm.id])
    os.remove(newname)


# save restricted
def saverec(message):
    
    if "https://t.me/c/" in message.text:
        app.send_message(message.chat.id, "**Send me only Public Channel Links**", reply_to_message_id=message.id)
        return

    datas = message.text.split("/")
    msgid = int(datas[-1])
    username = datas[-2]
    msg  = app.get_messages(username,msgid)
    app.copy_message(message.chat.id, msg.chat.id, msg.id)


# others
def other(message):

    # time date
    if message.text in ["time","Time",'date','Date']:
        app.send_message(message.chat.id, others.timeanddate(), reply_to_message_id=message.id)
    
    # b64 decode
    elif message.text[:5] == "b64d ":
        try:
            app.send_message(message.chat.id, f'__{others.b64d(message.text[5:])}__', reply_to_message_id=message.id)
        except:
            app.send_message(message.chat.id, "__Invalid__", reply_to_message_id=message.id)

    # b64 encode
    elif message.text[:5] == "b64e ":
        try:
            app.send_message(message.chat.id, f'__{others.b64e(message.text[5:])}__', reply_to_message_id=message.id)
        except:
            app.send_message(message.chat.id, "__Invalid__", reply_to_message_id=message.id)

    # maths
    elif not message.text.isalnum():
        info = others.maths(message.text)
        if info != None:
            app.send_message(message.chat.id, info, reply_to_message_id=message.id)


# download with progress
def down(message):

    try:
        size = int(message.document.file_size)
    except:
        try:
            size = int(message.video.file_size)
        except:
            size = 1

    if size > 25000000:
        msg = app.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
        dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',msg),daemon=True)
        dosta.start()
    else:
        msg = None

    file = app.download_media(message,progress=dprogress, progress_args=[message])
    os.remove(f'{message.id}downstatus.txt')
    return file,msg


# uploading with progress
def up(message, file, msg, video=False, capt="", thumb=None, duration=0, widht=0, height=0, multi=False):

    if msg != None:
        try:
            app.edit_message_text(message.chat.id, msg.id, '__Uploading__')
        except:
            pass
        
    if os.path.getsize(file) > 25000000:
        upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',msg),daemon=True)
        upsta.start()

    if not video:
        app.send_document(message.chat.id, document=file, caption=capt, force_document=True ,reply_to_message_id=message.id, progress=uprogress, progress_args=[message])    
    else:
        app.send_video(message.chat.id, video=file, caption=capt, thumb=thumb, duration=duration, width=widht, height=height, reply_to_message_id=message.id, progress=uprogress, progress_args=[message]) 

    if thumb != None:
        os.remove(thumb)
    if os.path.exists(f'{message.id}upstatus.txt'):   
        os.remove(f'{message.id}upstatus.txt')

    if msg != None and not multi:
        app.delete_messages(message.chat.id,message_ids=[msg.id])


# up progress
def uprogress(current, total, message):
    with open(f'{message.id}upstatus.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# down progress
def dprogress(current, total, message):
    with open(f'{message.id}downstatus.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# upload status
def upstatus(statusfile,message):

    while True:
        if os.path.exists(statusfile):
            break
        
    time.sleep(5)
    while os.path.exists(statusfile):

        with open(statusfile,"r") as upread:
            txt = upread.read()

        #if "%" not in txt:
                #txt = "0.0%"

        try:
            app.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            #if txt == "100.0%":
                #break
            time.sleep(10)
        except:
            time.sleep(5)


# download status
def downstatus(statusfile,message):

    while True:
        if os.path.exists(statusfile):
            break
        
    time.sleep(5)
    while os.path.exists(statusfile):

        with open(statusfile,"r") as upread:
            txt = upread.read()
        
        #if "%" not in txt:
                #txt = "0.0%"

        try:
            app.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            #if txt == "100.0%":
                #break
            time.sleep(10)
        except:
            time.sleep(5)


# app messages
@app.on_message(filters.command(['start']))
def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id, f"Welcome {message.from_user.mention}\nSend a **File** first and then **Extension**\n\n{START_TEXT}", reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(message,oldm,30),daemon=True)
    dm.start()                        


# help
@app.on_message(filters.command(['help']))
def help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id,
                     "**/start - To Check Availabe Conversions\n/help - This Message\n/imagegen - Text to Image\n/videogen - Text to Video\n/cancel - To Cancel\n/rename - To Rename File\n/read - To Read File\n/make - To Make File\n/chatGPT - Interact with chatGPT\n/guess - To Guess\n/tictactoe - To Play Tic Tac Toe\n/source - Github Source Code\n**", reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(message,oldm),daemon=True)
    dm.start() 


#source
@app.on_message(filters.command(['source']))
def source(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id, "**__GITHUB__ - https://github.com/bipinkrish/File-Converter-Bot**", disable_web_page_preview=True, reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(message,oldm),daemon=True)
    dm.start() 


# rename
@app.on_message(filters.command(['rename']))
def rename(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    try:
        newname = message.text.split("/rename ")[1]
    except:
        app.send_message(message.chat.id, "__Usage: **/rename new-file-name**\n(with extension)__", reply_to_message_id=message.id)
        return

    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        oldm = app.send_message(message.chat.id, "__**Renaming**__", reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
        rn = threading.Thread(target=lambda:rname(nmessage,newname,oldm),daemon=True)
        rn.start() 
        os.remove(f'{message.from_user.id}.json')
    else:
        app.send_message(message.chat.id, "__You need to send me a File first__", reply_to_message_id=message.id)   



# cancel
@app.on_message(filters.command(['cancel']))
def cancel(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')
        app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
        app.send_message(message.chat.id,"__Your job was **Canceled**__",reply_markup=ReplyKeyboardRemove(), reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id,"__No job to Cancel__", reply_to_message_id=message.id)     


# imagen command
@app.on_message(filters.command(["imagegen"]))
def getpompt(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
	# getting prompt from the text
	try:
		prompt = message.text.split("/imagegen ")[1]
	except:
		app.send_message(message.chat.id,'__Send Prompt with Command,\nUsage :__ **/imagegen dog with funny hat**', reply_to_message_id=message.id)
		return	

	# threding	
	app.send_message(message.chat.id,"__Prompt received and Request is sent. Waiting time is 1-2 mins__", reply_to_message_id=message.id)
	ai = threading.Thread(target=lambda:genrateimages(message,prompt),daemon=True)
	ai.start()


# videogen command
@app.on_message(filters.command(["videogen"]))
def videocog(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    app.send_message(message.chat.id,'__Currently Not Working__', reply_to_message_id=message.id)
    return


# read command
@app.on_message(filters.command(['read']))
def readcmd(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')

    else:
        app.send_message(message.chat.id,'__First send me a File__', reply_to_message_id=message.id)
        return

    oldm = app.send_message(message.chat.id,'__Reading File__', reply_to_message_id=message.id)
    rf = threading.Thread(target=lambda:readf(nmessage,oldm),daemon=True)
    rf.start()


# make command
@app.on_message(filters.command(['make']))
def makecmd(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')
        text = nmessage.text
    else:
        try:
            text = str(message.reply_to_message.text)
        except:
            app.send_message(message.chat.id,'__You need to either first send me a Text message or reply to a Text message__', reply_to_message_id=message.id)
            return 

    oldm = app.send_message(message.chat.id,'__Making File__', reply_to_message_id=message.id)
    mf = threading.Thread(target=lambda:makefile(message,text,oldm),daemon=True)
    mf.start()


# chatGpt
@app.on_message(filters.command(["chatgpt"]))
def send_gpt(client: pyrogram.client.Client,message: pyrogram.types.messages_and_media.message.Message,):
    try: qes = message.text.split("/chatGPT ")[1]
    except:
        message.reply_text("__use like this : __ **/chatGPT question**", reply_to_message_id=message.id)
        return

    msg = message.reply_text("__answering__", reply_to_message_id=message.id)
    cgpt = threading.Thread(target=lambda:chatai(qes,message,msg),daemon=True)
    cgpt.start()


# Tic Tac Toe Game
@app.on_message(filters.command("tictactoe"))
def startTTT(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	if message.chat.id == message.from_user.id: 
		return tictactoe.TTTgame(app,None,message,1)

	else:
		msg = app.send_message(message.chat.id, f'__Player 1 (X) : **{message.from_user.first_name}**__',
		reply_markup=InlineKeyboardMarkup(
		[[ InlineKeyboardButton( text='🤵 Player 2', callback_data="TTT P2")],
		 [ InlineKeyboardButton( text='🤖 v/s AI', callback_data="TTT AI")]]))
		tictactoe.TTTstoredata(msg.id, p1=message.from_user.id)


# Guess Game
@app.on_message(filters.command(['guess']))
def startG(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

    try:
        N = int(message.text.split("/guess ")[1])
        if N > 1000:
            app.send_message(message.chat.id,"**Not more than 1000**",reply_to_message_id=message.id)
            return
    except: N = 100

    size = len(bin(N).replace("0b", ""))
    app.send_message(message.chat.id,f"__Take a Number between__ **1 - {N}**\n__I will guess it in__ **{size} steps**\n__are you__ **ready ?**",reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton( text='Yes', callback_data='G ready'),
                    InlineKeyboardButton( text='No', callback_data='G not')
                ]]))
    
# callback
@app.on_callback_query()
def inbtwn(client: pyrogram.client.Client, call: pyrogram.types.CallbackQuery):
	if call.data[:4] == "TTT ": return tictactoe.TTTgame(app,call,call.message)
	elif call.data[:2] == "G ": return guess.Ggame(app,call)


# document
@app.on_message(filters.document)
def documnet(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
    dext = message.document.file_name.split(".")[-1].upper()

    # VID / AUD
    if message.document.file_name.upper().endswith(VIDAUD):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 📹 / 🔊\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=VAboard, reply_to_message_id=message.id)

    # IMG
    elif message.document.file_name.upper().endswith(IMG):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 📷\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__Colorize, Positive, Upscale & Scan__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=IMGboard, reply_to_message_id=message.id)

    # LBW
    elif message.document.file_name.upper().endswith(LBW):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 💼 \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{LBW_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=LBWboard, reply_to_message_id=message.id)

    # LBC
    elif message.document.file_name.upper().endswith(LBC):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 💼 \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{LBC_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=LBCboard, reply_to_message_id=message.id)

    # LBI
    elif message.document.file_name.upper().endswith(LBI):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 💼 \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{LBI_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=LBIboard, reply_to_message_id=message.id)

    # FF
    elif message.document.file_name.upper().endswith(FF):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 🔤 \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{FF_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=FFboard, reply_to_message_id=message.id)

    # EB
    elif message.document.file_name.upper().endswith(EB):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 📚 \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{EB_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=EBboard, reply_to_message_id=message.id)
    
    # ARC
    elif message.document.file_name.upper().endswith(ARC):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 🗄\n__Do you want to Extract ?__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=ARCboard, reply_to_message_id=message.id)

    # TOR
    elif message.document.file_name.upper().endswith("TORRENT"):
        os.remove(f'{message.from_user.id}.json')
        oldm = app.send_message(message.chat.id,'__Getting Magnet Link__', reply_to_message_id=message.id)
        ml = threading.Thread(target=lambda:getmag(message,oldm),daemon=True)
        ml.start()
        return
    
    # SUB
    elif message.document.file_name.upper().endswith(SUB):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 🗯️ \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{SUB_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=SUBboard, reply_to_message_id=message.id)

    # PRO
    elif message.document.file_name.upper().endswith(PRO):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 👨‍💻 \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{PRO_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=PROboard, reply_to_message_id=message.id)
    
    # T3D
    elif message.document.file_name.upper().endswith(T3D):
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 💠 \n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{T3D_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=T3Dboard, reply_to_message_id=message.id)

    # else
    else:
        app.send_message(message.chat.id,'__No Available Conversions found.\n\nYou can use:__\n**/rename new-filename** __to Rename__\n**/read** __to Read the File__')
    


# animation
@app.on_message(filters.animation)
def annimations(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id,'**Turning it into Document then you can use that to Convert**',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=message.id)
    sd = threading.Thread(target=lambda:senddoc(message,oldm),daemon=True)
    sd.start()


# video
@app.on_message(filters.video)
def video(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    try:
        if message.video.file_name.upper().endswith(VIDAUD):
            with open(f'{message.from_user.id}.json', 'wb') as handle:
                pickle.dump(message, handle)
            dext = message.video.file_name.split(".")[-1].upper()
            app.send_message(message.chat.id,
                            f'__Detected Extension:__ **{dext}** 📹 / 🔊\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                            reply_markup=VAboard, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id, f'--**Available formats**--:\n\n**VIDEOS/AUDIOS** 📹 / 🔊\n__{VA_TEXT}__',
                            reply_to_message_id=message.id)
   
    except:
        oldm = app.send_message(message.chat.id,'**Turning it into Document then you can use that to Convert**',reply_markup=ReplyKeyboardRemove())
        sd = threading.Thread(target=lambda:senddoc(message,oldm),daemon=True)
        sd.start()


# video note
@app.on_message(filters.video_note)
def videonote(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'__Detected Extension:__ **MP4** 📹 / 🔊\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                reply_markup=VAboard, reply_to_message_id=message.id)


# audio
@app.on_message(filters.audio)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.audio.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.audio.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'__Detected Extension:__ **{dext}** 📹 / 🔊\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'--**Available formats**--:\n\n**VIDEOS/AUDIOS** 📹 / 🔊 \n__{VIDAUD}__',
                         reply_to_message_id=message.id)


# voice
@app.on_message(filters.voice)
def voice(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'__Detected Extension:__ **OGG** 📹 / 🔊\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                reply_markup=VAboard, reply_to_message_id=message.id)


# photo
@app.on_message(filters.photo)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                     f'__Detected Extension:__ **JPG** 📷\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__Colorize, Positive, Upscale & Scan__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                     reply_markup=IMGboard, reply_to_message_id=message.id)


# sticker
@app.on_message(filters.sticker)
def sticker(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
    if not message.sticker.is_animated and not message.sticker.is_video:
        app.send_message(message.chat.id,
                     f'__Detected Extension:__ **WEBP** 📷\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__Colorize, Positive, Upscale & Scan__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                     reply_markup=IMGboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id,
                    f'__Detected Extension:__ **TGS** 📷\n__Now send extension to Convert to...__\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__Colorize, Positive, Upscale & Scan__\n\n{message.from_user.mention} __choose or click /cancel to Cancel or use /rename  to  Rename__',
                    reply_markup=IMGboard, reply_to_message_id=message.id)


# conversion starts here
@app.on_message(filters.text)
def text(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):  

    # save restricted
    if "https://t.me/" in message.text:
        mf = threading.Thread(target=lambda:saverec(message),daemon=True)
        mf.start()
        return

    # magnet link
    if message.text[:8] == "magnet:?":
        oldm = app.send_message(message.chat.id,'__Processing...__', reply_to_message_id=message.id) 
        tf = threading.Thread(target=lambda:gettorfile(message,oldm),daemon=True)
        tf.start()
        return

    # normal
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')

        if "COLOR" == message.text or "POSITIVE" == message.text:

            oldm = app.send_message(message.chat.id,'__Processing__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id) 
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])

            if "COLOR" in message.text:
                col = threading.Thread(target=lambda:colorizeimage(nmessage,oldm),daemon=True)
                col.start()
                return
            else:
                pos = threading.Thread(target=lambda:negetivetopostive(nmessage,oldm),daemon=True)
                pos.start() 
                return

        if "READ" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Reading File__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            rf = threading.Thread(target=lambda:readf(nmessage,oldm),daemon=True)
            rf.start()
            return

        if "SENDPHOTO" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Sending in Photo Format__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            sp = threading.Thread(target=lambda:sendphoto(nmessage,oldm),daemon=True)
            sp.start()
            return

        if "SENDDOC" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Sending in Document Format__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            sd = threading.Thread(target=lambda:senddoc(nmessage,oldm),daemon=True)
            sd.start()
            return    

        if "SENDVID" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Sending in Stream Format__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            sv = threading.Thread(target=lambda:sendvideo(nmessage,oldm),daemon=True)
            sv.start()
            return

        if "SpeechToText" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Transcripting, takes long time for Long Files__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            stt = threading.Thread(target=lambda:transcript(nmessage,oldm),daemon=True)
            stt.start()
            return

        if "TextToSpeech" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Generating Speech__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            tts = threading.Thread(target=lambda:speak(nmessage,oldm),daemon=True)
            tts.start()
            return

        if "UPSCALE" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Upscaling Your Image__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            upscl = threading.Thread(target=lambda:increaseres(nmessage,oldm),daemon=True)
            upscl.start()
            return

        if "EXTRACT" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Extracting File__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            ex = threading.Thread(target=lambda:extract(nmessage,oldm),daemon=True)
            ex.start()
            return 

        if "COMPILE" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Compiling__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            cmp = threading.Thread(target=lambda:compile(nmessage,oldm),daemon=True)
            cmp.start()
            return

        if "SCAN" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Scanning__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            scn = threading.Thread(target=lambda:scan(nmessage,oldm),daemon=True)
            scn.start()
            return

        if "RUN" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'__Running__',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            rpro = threading.Thread(target=lambda:runpro(nmessage,oldm),daemon=True)
            rpro.start()
            return

        if "document" in str(nmessage):
            inputt = nmessage.document.file_name
            print("File is a Document")
        else:
            if "audio" in str(nmessage) or "voice" in str(nmessage):
                try:
                    inputt = nmessage.audio.file_name
                    print("File is a Audio")
                except:
                    inputt = "voice.ogg"
                    print("File is a Voice")
            else:
                if "voice" in str(nmessage):
                    inputt = "voice.ogg"
                    print("File is a Voice")
                else:
                    if "sticker" in str(nmessage):
                        if (not nmessage.sticker.is_animated) and (not nmessage.sticker.is_video):
                            inputt = nmessage.sticker.set_name + ".webp"
                        else:
                            inputt = nmessage.sticker.set_name + ".tgs"
                        print("File is a Sticker")
                    else:
                        if "video" in str(nmessage):
                            try:
                                inputt = nmessage.video.file_name
                                print("File is a Video")
                            except:
                                inputt = "video_note.mp4"
                                print("File is a Video Note")     
                        else:
                            if "video_note" in str(nmessage):
                                inputt = "voice_note.mp4"
                                print("File is a Video Note")   
                            else:
                                if "photo" in str(nmessage):
                                    temp = app.download_media(nmessage)
                                    inputt = temp.split("/")[-1]
                                    os.remove(temp)
                                    print("File is a Photo")
                                else:
                                    inputt = ""

        newext = message.text.lower()
        oldext = inputt.split(".")[-1]

        #if newext == "ico":
            #app.send_message(message.chat.id, "Warning: for ICO, image will be resized and made multi-resolution", reply_to_message_id=message.id)
        
        if oldext.upper() == newext.upper():
            app.send_message(message.chat.id, "__Nice try, Don't choose same Extension__", reply_to_message_id=nmessage.id, reply_markup=ReplyKeyboardRemove())
            
        else:
            msg = app.send_message(message.chat.id, f'Converting from **{oldext.upper()}** to **{newext.upper()}**', reply_to_message_id=nmessage.id, reply_markup=ReplyKeyboardRemove())
            conv = threading.Thread(target=lambda: follow(nmessage, inputt, newext, oldext, msg), daemon=True)
            conv.start()

        app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])

    else:
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        if str(message.from_user.id) == str(message.chat.id):
            if len(message.text.split("\n")) == 1:
                os.remove(f'{message.from_user.id}.json')
                ots = threading.Thread(target=lambda: other(message), daemon=True)
                ots.start()
            else:    
                app.send_message(message.chat.id, '__for Text messages, You can use **/make** to Create a File from it.\n(first line of text will be trancated and used as filename)__', reply_to_message_id=message.id)
            

#apprun
print("Bot Started")
app.run()
