from pyrogram import Client
from pyrogram import filters
import os
import threading
import pickle

'''
bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
'''

#binaries
link = "wget https://archive.org/download/binaries/binaries.zip"
os.system(link)
os.system("unzip binaries.zip")
os.remove("binaries.zip")	

#bot
api_id = 11223922
api_hash = "ac6664c07855e0455095d970a98a082d"
bot_token = "5358186417:AAGKQt1Xf2ps2gU0_CCkquAZRDofY7MKte8"
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

#setting
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
ffmpeg = dirPath + "/binaries" + "/ffmpeg/ffmpeg"
magick = dirPath + "/binaries" + "/magick"
os.system(f"chmod 777 {ffmpeg} {magick}")

#suporrtedextension
VIDAUD = ("AUDIONOTE","AIFF","AAC","M4A","OGA","WMA","FLAC","WAV","OPUS","OGG","MP3","MKV","MP4","MOV")
IMG = ("OCR","SENDPHOTO","PDF","ICO","GIF","TIFF","TIF","BMP","WEBP","JP2","JPEG","JPG","PNG")

#main
def follow(message,input,new):
    output = updtname(input,new)
    if input.upper().endswith(VIDAUD):
        print("It is VID/AUD option")
        file = app.download_media(message)
        cmd = ffmpegcommand(file,output)
        os.system(cmd)
        os.remove(file)
        app.send_document(message.chat.id,document=output)
        os.remove(output)

    elif input.upper().endswith(IMG):
        print("It is IMG option")
        file = app.download_media(message)
        cmd = magickcommand(file,output)
        os.system(cmd)
        os.remove(file)
        app.send_document(message.chat.id,document=output)
        os.remove(output)

#newfilename
def updtname(input,new):
    input = input.split(".")
    input[-1] = new
    output = ""
    for ele in input:
        output = output+"."+ele
    output = output[1:]
    print(f'New Filename will be' )
    print(output)
    return output

#ffmpegcmd
def ffmpegcommand(input,output):
    cmd = f'{ffmpeg} -i "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#magiccmd
def magickcommand(input,output):
    cmd = f'{magick} "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd  

#app
@app.on_message(filters.command(['start']))
def echo(client, message):
    app.send_message(message.chat.id,f"Welcome\nSend a File first and then Extension\n\nAvailable formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}")
    

@app.on_message(filters.document)
def documnet(client, message):
    if message.document.file_name.upper().endswith(VIDAUD): 
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {VIDAUD}')

    elif message.document.file_name.upper().endswith(IMG): 
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {IMG}')
    else:
        app.send_message(message.chat.id,f'Available formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}')

@app.on_message(filters.video)
def video(client, message):
    if message.document.file_name.upper().endswith(VIDAUD): 
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {VIDAUD}')
    else:
        app.send_message(message.chat.id,f'Available formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}')

@app.on_message(filters.audio)
def audio(client, message):
    if message.audio.file_name.upper().endswith(VIDAUD): 
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {VIDAUD}')
    else:
        app.send_message(message.chat.id,f'Available formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}')

@app.on_message(filters.photo)
def photo(client, message):
    #json.dump(json.loads(str(message)),open(f'{message.from_user.id}.json',"w"))
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {IMG}')

@app.on_message(filters.text)
def text(client, message):
    if os.path.exists(f'{message.from_user.id}.json'):
        #nmessage = json.load(open(f'{message.from_user.id}.json',"r"))
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')

        if "document" in str(nmessage):
            input = nmessage.document.file_name
            print("File is a Document")
        else:
            if "audio" in str(nmessage):   
                input = nmessage.audio.file_name
                print("File is a Audio")
            else:
                if "video" in str(nmessage): 
                    input = nmessage.video.file_name  
                    print("File is a Video")
                else:
                    if "photo" in str(nmessage):
                        temp = app.download_media(nmessage)
                        input = temp.split("/")[-1]
                        os.remove(temp)
                        print("File is a Photo")

        newext = message.text.lower()
        oldext = input.split(".")[-1]
        if newext == "ico":
            app.send_message(message.chat.id,"Warning: for ICO to work, make sure image is in 256x256 size")
        app.send_message(message.chat.id,f'Converting from {oldext.upper()} to {newext.upper()}')
        conv = threading.Thread(target=lambda:follow(nmessage,input,newext),daemon=True)
        conv.start()

#apprun
app.run()
