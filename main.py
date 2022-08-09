import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram import enums

import os
import threading
import pickle
import time

from buttons import *
import aifunctions
import helperfunctions


# env
bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")


# bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)
os.system("chmod 777 c41lab.py negfix8 tgsconverter")


# main function to follow
def follow(message,inputt,new,oldmessage):
    output = helperfunctions.updtname(inputt,new)

    if output.upper().endswith(VIDAUD) and inputt.upper().endswith(VIDAUD):
        print("It is VID/AUD option")
        file = app.download_media(message)
        srclink = helperfunctions.videoinfo(file)
        cmd = helperfunctions.ffmpegcommand(file,output,new)
        os.system(cmd)
        os.remove(file)
        conlink = helperfunctions.videoinfo(output)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, caption=f'Source File : {srclink}\n\nConverted File : {conlink}')
        except:
            app.send_message(message.chat.id,"Error while conversion")
            
        os.remove(output)

    elif output.upper().endswith(IMG) and inputt.upper().endswith(IMG):
        print("It is IMG option")
        file = app.download_media(message)
        srclink = helperfunctions.imageinfo(file)
        cmd = helperfunctions.magickcommand(file,output,new)
        os.system(cmd)
        conlink = helperfunctions.imageinfo(output)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, caption=f'Source File : {srclink}\n\nConverted File : {conlink}')
        except:
            app.send_message(message.chat.id,"Error while conversion")
            
        os.remove(output)

        if new == "ocr":
            cmd = helperfunctions.tesrctcommand(file,message.id)
            os.system(cmd)
            with open(f"{message.id}.txt","r") as ocr:
                text = ocr.read()
            os.remove(f"{message.id}.txt")
            app.send_message(message.chat.id,text)
            
        if new == "ico":
            slist = ["256", "128", "96", "64", "48", "32", "16"]
            for ele in slist:
                toutput = helperfunctions.updtname(inputt,f"{ele}.png")
                os.remove(toutput)
        
        os.remove(file)

    elif output.upper().endswith(IMG) and inputt.upper().endswith("TGS"):
        if new == "webp" or new == "gif" or new == "png":
            print("It is Animated Sticker option")
            file = app.download_media(message)
            srclink = helperfunctions.imageinfo(file)        
            os.system(f'./tgsconverter "{file}" "{new}"')
            output = helperfunctions.updtname(file,new)
            conlink = helperfunctions.imageinfo(output)
            try:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, caption=f'Source File : {srclink}\n\nConverted File : {conlink}')
            except:
                app.send_message(message.chat.id,"Error while conversion")

            os.remove(file)
            os.remove(output)
            
        else:
            app.send_message(message.chat.id,"Only Availble Conversions for Animated Stickers are GIF, PNG and WEBP")

    elif output.upper().endswith(EB) and inputt.upper().endswith(EB):
        print("It is Ebook option")
        file = app.download_media(message)
        cmd = helperfunctions.calibrecommand(file,output)
        os.system(cmd)
        os.remove(file)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output,force_document=True)
        except:
            app.send_message(message.chat.id,"Error while conversion")
            
        os.remove(output)

    elif (output.upper().endswith(LBW) and inputt.upper().endswith(LBW)) or (output.upper().endswith(LBI) and inputt.upper().endswith(LBI)) or (output.upper().endswith(LBC) and inputt.upper().endswith(LBC)):
        print("It is LibreOffice option")
        file = app.download_media(message)
        cmd = helperfunctions.libreofficecommand(file,new)
        os.system(cmd)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True)
        except:
            app.send_message(message.chat.id,"Error while conversion")
            
        os.remove(file)
        os.remove(output)

    elif output.upper().endswith(FF) and inputt.upper().endswith(FF):
        print("It is FontForge option")
        file = app.download_media(message)
        cmd = helperfunctions.fontforgecommand(file,output,message)
        os.system(cmd)
        os.remove(f"{message.id}-convert.pe")
        os.remove(file)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True)
        except:
            app.send_message(message.chat.id,"Error while conversion")
            
        os.remove(output)
    else:
        app.send_message(message.chat.id,"Send me valid Extension")

    # deleting message    
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id+1])


# negative to positive
def negetivetopostive(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    print("using c41lab")
    os.system(f'./c41lab.py "{file}" "{output}"')
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> c41lab")
    os.remove(output)
    
    print("using simple tool")
    aifunctions.positiver(file,output)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> simple tool")
    os.remove(output)
    
    print("using negfix8")
    os.system(f'./negfix8 "{file}" "{output}"')
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> negfix8")
    os.remove(output)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# color image
def colorizeimage(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    aifunctions.deoldify(file,output)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> Deoldify")
    os.remove(output)

    aifunctions.colorize_image(output,file)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> simple tool")
    os.remove(output)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# dalle
def genrateimages(message,prompt):
    
    # requsting
    mdhash = aifunctions.mindalle(prompt,AutoCall=False) # min dalle
    ldhash = aifunctions.latdif(prompt,AutoCall=False) # latent 
    filelist = aifunctions.dallemini(prompt) # dalle mini
    latfile = aifunctions.latentdiff(prompt) # latent direct
    imagelist = aifunctions.latdifstatus(ldhash,prompt) # latent get
    mdfile = aifunctions.mindallestatus(mdhash,prompt) # min dalle get

    # dalle mini
    app.send_message(message.chat.id,f"DALLE-MINI : {prompt}")
    for ele in filelist:
        app.send_document(message.chat.id,document=ele,force_document=True)
        os.remove(ele)
    os.rmdir(prompt)

    # latent diffusion
    app.send_message(message.chat.id,f"LATENT DIFFUSION : {prompt}")
    app.send_document(message.chat.id,document=latfile,force_document=True)
    os.remove(latfile)
    for ele in imagelist:
        app.send_document(message.chat.id,document=ele,force_document=True)
        os.remove(ele)
        
    # min dalle
    app.send_message(message.chat.id,f"MIN-DALLE : {prompt}")
    app.send_document(message.chat.id,document=mdfile,force_document=True)
    os.remove(mdfile)

    # delete msg
    app.delete_messages(message.chat.id,message_ids=[message.id+1])


# cog video
def genratevideos(message,prompt):

    hash, queuepos = aifunctions.cogvideo(prompt,AutoCall=False)
    msg = app.send_message(message.chat.id,f"Prompt received and Request is sent. Expected waiting time is {(queuepos+1)*1.5} mins")

    file = aifunctions.cogvideostatus(hash,prompt)
    app.send_video(message.chat.id, video=file)#,caption=f"COGVIDEO : {prompt}")
    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[msg.id])


# delete msg
def dltmsg(message,sec=15):
    time.sleep(sec)
    app.delete_messages(message.chat.id,message_ids=[message.id,message.id-1])


# read file
def readf(message,oldmessage):
    file = app.download_media(message)
    with open(file,"r") as rf:
        txt = rf.read()
    try:
        n = 4096
        split = [txt[i:i+n] for i in range(0, len(txt), n)]
        for ele in split:
            app.send_message(message.chat.id,ele)   
    except:
        app.send_message(message.chat.id,"Error in Reading File")   

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])

# send video
def sendvideo(message,oldmessage):
    file = app.download_media(message)
    app.send_video(message.chat.id,video=file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)


# send document
def senddoc(message,oldmessage):
    file = app.download_media(message)
    app.send_document(message.chat.id,document=file,force_document=True)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)


# send photo
def sendphoto(message,oldmessage):
    file = app.download_media(message)
    app.send_photo(message.chat.id,photo=file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)


# make file
def makefile(message,oldmessage):
    text = message.text.split("\n")
    firstline = text[0]
    text.remove(text[0])
    
    message.text = ""
    for ele in text: 
        message.text = message.text + f"{ele}\n"
    
    with open(firstline,"w") as file:
        file.write(message.text)
    try:
        app.send_document(message.chat.id, document=firstline)
    except:
        app.send_message(message.chat.id, "Makefile takes first line of your Text as Filename and File content will start from Second line")

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
        
    app.send_document(message.chat.id, document=temp)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)
    os.remove(temp)
    

# text to speech 
def speak(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
    output = helperfunctions.updtname(inputt,"mp3")
   
    aifunctions.texttospeech(file,output)
    os.remove(file)

    app.send_document(message.chat.id, document=output)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(output)


# upscaling
def increaseres(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
   
    aifunctions.upscale(file,inputt)
    os.remove(file)

    app.send_document(message.chat.id, document=inputt)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(input)


# app messages
@app.on_message(filters.command(['start']))
def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id, f"Welcome {message.from_user.mention}\nSend a File first and then Extension\n\n{START_TEXT}")
    dm = threading.Thread(target=lambda:dltmsg(oldm,30),daemon=True)
    dm.start()                        

@app.on_message(filters.command(['help']))
def help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id,
                     "/start - To Check Availabe Conversions\n/help - This Message\n/dalle - Text to Image\n/cogvideo - Text to Video\n/cancel - To Cancel\n/source - Github Source Code\n")
    dm = threading.Thread(target=lambda:dltmsg(oldm),daemon=True)
    dm.start() 

@app.on_message(filters.command(['source']))
def source(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id, "GITHUB - https://github.com/bipinkrish/File-Converter-Bot")
    dm = threading.Thread(target=lambda:dltmsg(oldm),daemon=True)
    dm.start() 

@app.on_message(filters.command(['cancel']))
def source(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')
        app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
        app.send_message(message.chat.id,"Your job was Canceled",reply_markup=ReplyKeyboardRemove())
    else:
        app.send_message(message.chat.id,"No job to Cancel")     

# dalle command
@app.on_message(filters.command(["dalle"]))
def getpompt(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# getting prompt from the text
	try:
		prompt = message.text.split("/dalle ")[1]
	except:
		app.send_message(message.chat.id,'Send Prompt with Command,\nUssage : "/dalle high defination studio image of pokemon"')
		return	

	# threding	
	app.send_message(message.chat.id,"Prompt received and Request is sent. Waiting time is 1-2 mins")
	ai = threading.Thread(target=lambda:genrateimages(message,prompt),daemon=True)
	ai.start()


# cog video
@app.on_message(filters.command(["cogvideo"]))
def videocog(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# getting prompt from the text
	try:
		prompt = message.text.split("/cogvideo ")[1]
	except:
		app.send_message(message.chat.id,'Send Prompt with Command,\nUssage : "/cogvideo a man climbing up a mountain"')
		return	

	# threding	
	vi = threading.Thread(target=lambda:genratevideos(message,prompt),daemon=True)
	vi.start()
    

@app.on_message(filters.document)
def documnet(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.document.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=VAboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(IMG):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{IMG_TEXT}\n\n**SPECIAL** 🎁\nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=IMGboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBW):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 💼 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{LBW_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=LBWboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBC):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 💼 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{LBC_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=LBCboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBI):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 💼 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{LBI_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=LBIboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(FF):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 🔤 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{FF_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=FFboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(EB):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📚 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{EB_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=EBboard, reply_to_message_id=message.id)

    else:
        #app.send_message(message.chat.id,f'{START_TEXT}',reply_to_message_id=message.id)
        oldm = app.send_message(message.chat.id,'No Available Conversions Found, Reading File',reply_markup=ReplyKeyboardRemove())
        rf = threading.Thread(target=lambda:readf(message,oldm),daemon=True)
        rf.start()


@app.on_message(filters.video)
def video(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.video.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.video.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'--**Available formats**--:\n\n**VIDEOS/AUDIOS** 📹 / 🔊\n{VA_TEXT}',
                         reply_to_message_id=message.id)


@app.on_message(filters.video_note)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'Detected Extension: **MP4** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                reply_markup=VAboard, reply_to_message_id=message.id)


@app.on_message(filters.audio)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.audio.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.audio.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'--**Available formats**--:\n\n**VIDEOS/AUDIOS** 📹 / 🔊 \n{VIDAUD}',
                         reply_to_message_id=message.id)


@app.on_message(filters.voice)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'Detected Extension: **OGG** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                reply_markup=VAboard, reply_to_message_id=message.id)


@app.on_message(filters.photo)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                     f'Detected Extension: **JPG** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{IMG_TEXT}\n\n**SPECIAL** 🎁\nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                     reply_markup=IMGboard, reply_to_message_id=message.id)


@app.on_message(filters.sticker)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
    if not message.sticker.is_animated and not message.sticker.is_video:
        app.send_message(message.chat.id,
                     f'Detected Extension: **WEBP** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{IMG_TEXT}\n\n**SPECIAL** 🎁\nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                     reply_markup=IMGboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id,
                    f'Detected Extension: **TGS** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n{IMG_TEXT}\n\n**SPECIAL** 🎁\nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                    reply_markup=IMGboard, reply_to_message_id=message.id)


@app.on_message(filters.text)
def text(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):  

    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')

        if "COLOR" == message.text or "POSITIVE" == message.text:

            oldm = app.send_message(message.chat.id,'Processing',reply_markup=ReplyKeyboardRemove()) 
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
            oldm = app.send_message(message.chat.id,'Reading File',reply_markup=ReplyKeyboardRemove())
            rf = threading.Thread(target=lambda:readf(nmessage,oldm),daemon=True)
            rf.start()
            return

        if "SENDPHOTO" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Photo',reply_markup=ReplyKeyboardRemove())
            sp = threading.Thread(target=lambda:sendphoto(nmessage,oldm),daemon=True)
            sp.start()
            return

        if "SENDDOC" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Document',reply_markup=ReplyKeyboardRemove())
            sd = threading.Thread(target=lambda:senddoc(nmessage,oldm),daemon=True)
            sd.start()
            return    

        if "SENDVID" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Video',reply_markup=ReplyKeyboardRemove())
            sv = threading.Thread(target=lambda:sendvideo(nmessage,oldm),daemon=True)
            sv.start()
            return

        if "SpeechToText" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Transcripting, takes long time for Long Files',reply_markup=ReplyKeyboardRemove())
            stt = threading.Thread(target=lambda:transcript(nmessage,oldm),daemon=True)
            stt.start()
            return

        if "TextToSpeech" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Generating Speech',reply_markup=ReplyKeyboardRemove())
            tts = threading.Thread(target=lambda:speak(nmessage,oldm),daemon=True)
            tts.start()
            return

        if "UPSCALE" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Upscaling Your Image',reply_markup=ReplyKeyboardRemove())
            upscl = threading.Thread(target=lambda:increaseres(nmessage,oldm),daemon=True)
            upscl.start()
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
                        if not nmessage.sticker.is_animated and not nmessage.sticker.is_video:
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
        
        app.send_message(message.chat.id, f'Converting from **{oldext.upper()}** to **{newext.upper()}**', reply_to_message_id=message.id, reply_markup=ReplyKeyboardRemove())
        app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])

        conv = threading.Thread(target=lambda: follow(nmessage, inputt, newext, message), daemon=True)
        conv.start()

    else:
        if message.from_user.id == message.chat.id:
            #app.send_message(message.chat.id, "First send me a File", reply_to_message_id=message.id)
            oldm = app.send_message(message.chat.id,'Making File',reply_markup=ReplyKeyboardRemove())
            mf = threading.Thread(target=lambda:makefile(message,oldm),daemon=True)
            mf.start()
            

#apprun
print("Bot Started")
app.run()
