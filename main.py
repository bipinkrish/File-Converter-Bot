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
            cmd = helperfunctions.tesrctcommand(file,"ocr")
            os.system(cmd)
            with open("ocr.txt","r") as ocr:
                text = ocr.read()
            os.remove("ocr.txt")
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
    
    # min dalle requsting
    hash = aifunctions.mindalle(prompt,AutoCall=False)

    # dalle mini
    filelist = aifunctions.dallemini(prompt)
    app.send_message(message.chat.id,f"DALLE-MINI : {prompt}")
    for ele in filelist:
        app.send_document(message.chat.id,document=ele,force_document=True)
        os.remove(ele)
    os.rmdir(prompt)

    # latent diffusion
    file = aifunctions.latentdiff(prompt)
    app.send_document(message.chat.id,document=file,force_document=True,caption=f"Latent Diffusion : {prompt}")
    os.remove(file)
    
    # min dalle
    file = aifunctions.mindallestatus(hash,prompt)
    app.send_document(message.chat.id,document=file,force_document=True,caption=f"MIN-DALLE : {prompt}")
    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[message.id+1])


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


# app messages
@app.on_message(filters.command(['start']))
def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id, f"Welcome {message.from_user.mention}\nSend a File first and then Extension\n\n{START_TEXT}")
    dm = threading.Thread(target=lambda:dltmsg(oldm,30),daemon=True)
    dm.start()                        

@app.on_message(filters.command(['help']))
def help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id,
                     "/start - To Check Availabe Conversions\n/help - This Message\n/dalle - Text to Image\n/cancel - To Cancel\n/source - Github Source Code\n")
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


@app.on_message(filters.document)
def documnet(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.document.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=VAboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(IMG):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{IMG_TEXT}\n\n**SPECIAL** \nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=IMGboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBW):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{LBW_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=LBWboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBC):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{LBC_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=LBCboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBI):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{LBI_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=LBIboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(FF):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{FF_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=FFboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(EB):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{EB_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=EBboard, reply_to_message_id=message.id)

    else:
        app.send_message(message.chat.id,f'{START_TEXT}',reply_to_message_id=message.id)


@app.on_message(filters.video)
def video(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.video.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.video.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'Available formats:\n\nVIDEOS/AUDIOS: {VA_TEXT}',
                         reply_to_message_id=message.id)


@app.on_message(filters.video_note)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'Detected Extension: **MP4** \nNow send extension to Convert to...\n\n**Available formats** \n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                reply_markup=VAboard, reply_to_message_id=message.id)


@app.on_message(filters.audio)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.audio.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.audio.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** \nNow send extension to Convert to...\n\n**Available formats** \n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'Available formats:\n\nVIDEOS/AUDIOS: {VIDAUD}',
                         reply_to_message_id=message.id)


@app.on_message(filters.voice)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'Detected Extension: **OGG** \nNow send extension to Convert to...\n\n**Available formats** \n{VA_TEXT}\n\n{message.from_user.mention} choose or click /cancel',
                reply_markup=VAboard, reply_to_message_id=message.id)


@app.on_message(filters.photo)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                     f'Detected Extension: **JPG** \nNow send extension to Convert to...\n\n**Available formats** \n{IMG_TEXT}\n\n**SPECIAL** \nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                     reply_markup=IMGboard, reply_to_message_id=message.id)


@app.on_message(filters.sticker)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
    if not message.sticker.is_animated and not message.sticker.is_video:
        app.send_message(message.chat.id,
                     f'Detected Extension: **WEBP** \nNow send extension to Convert to...\n\n**Available formats** \n{IMG_TEXT}\n\n**SPECIAL** \nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                     reply_markup=IMGboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id,
                    f'Detected Extension: **TGS** \nNow send extension to Convert to...\n\n**Available formats** \n{IMG_TEXT}\n\n**SPECIAL** \nCOLORIZE & POSITIVE\n\n{message.from_user.mention} choose or click /cancel',
                    reply_markup=IMGboard, reply_to_message_id=message.id)


@app.on_message(filters.text)
def text(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):  

    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')

        if "COLOR" in message.text or "POSITIVE" in message.text:

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

        if "READ" in message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Reading File',reply_markup=ReplyKeyboardRemove())
            rf = threading.Thread(target=lambda:readf(nmessage,oldm),daemon=True)
            rf.start()
            return

        if "SENDPHOTO" in message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Photo',reply_markup=ReplyKeyboardRemove())
            sp = threading.Thread(target=lambda:sendphoto(nmessage,oldm),daemon=True)
            sp.start()
            return

        if "SENDDOC" in message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Document',reply_markup=ReplyKeyboardRemove())
            sd = threading.Thread(target=lambda:senddoc(nmessage,oldm),daemon=True)
            sd.start()
            return    

        if "SENDVID" in message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Video',reply_markup=ReplyKeyboardRemove())
            sv = threading.Thread(target=lambda:sendvideo(nmessage,oldm),daemon=True)
            sv.start()
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
        
        app.send_message(message.chat.id, f'Converting from {oldext.upper()} to {newext.upper()}', reply_to_message_id=message.id, reply_markup=ReplyKeyboardRemove())
        app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])

        conv = threading.Thread(target=lambda: follow(nmessage, inputt, newext, message), daemon=True)
        conv.start()

    else:
        if message.from_user.id == message.chat.id:
            app.send_message(message.chat.id, "First send me a File", reply_to_message_id=message.id)
        

#apprun
print("Bot Started")
app.run()
