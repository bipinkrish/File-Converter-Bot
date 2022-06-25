from pyrogram import Client
from pyrogram import filters
import os
import threading
import pickle

#env
bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")

#binaries
link = "wget https://github.com/bipinkrish/file-converter-telegram-bot/releases/download/binaries/binaries.zip"
os.system(link)
os.system("unzip binaries.zip")
os.remove("binaries.zip")	

#bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

#setting
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
ffmpeg = dirPath + "/binaries" + "/ffmpeg/ffmpeg"
magick = dirPath + "/binaries" + "/magick"
tesseract = dirPath + "/binaries" + "/tesseract"
libreoffice = dirPath + "/binaries" + "/LibreOffice"
fontforge = dirPath + "/binaries" + "/FontForge"
os.system(f"chmod 777 {ffmpeg} {magick} {tesseract} {libreoffice} {fontforge}")

#suporrtedextension
VIDAUD = ("AIFF","AAC","M4A","OGA","WMA","FLAC","WAV","OPUS","OGG","MP3","MKV","MP4","MOV")
IMG = ("OCR","ICO","GIF","TIFF","TIF","BMP","WEBP","JP2","JPEG","JPG","PNG")
LB = ("ODT","CSV","DB","DOC","DOCX","DOTX","FODP","FODS","FODT","MML","ODB","ODF","ODG","ODM","ODP","ODS","OTG","OTP","OTS","OTT","OXT","PDF","PPTX","PSW","SDA","SDC","SDD","SDP","SDW","SLK:","SMF","STC","STD","STI","STW","SXC","SXG","SXI","SXM","SXW","UOF","UOP","UOS","UOT","VSD","VSDX","WDB","WPS","WRI","XLS","XLSX")
FF = ("SFD","BDF","FNT","OTF","PFA","PFB","TTC","TTF","UFO","WOFF")

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
        app.send_document(message.chat.id,document=output)
        os.remove(output)
        if new == "ocr":
            cmd = tesrctcommand(file,"ocr")
            os.system(cmd)
            app.send_document(message.chat.id,document="ocr.txt")
            os.remove("ocr.txt")
        os.remove(file)

    elif input.upper().endswith(LB):
        print("It is LibreOffice option")
        file = app.download_media(message)
        cmd = libreofficecommand(file,new)
        os.system(cmd)
        os.remove(file)
        app.send_document(message.chat.id,document=output)
        os.remove(output)

    elif input.upper().endswith(FF):
        print("It is FontForge option")
        file = app.download_media(message)
        cmd = fontforgecommand(file,output)
        os.system(cmd)
        os.remove("convert.pe")
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

#fontforgecmd
def fontforgecommand(input,output):
    des = dirPath + f"/{output}"
    cdes = dirPath + "/convert.pe"
    text = f'Open(\'{input}\')\nGenerate(\'{des}\')'
    with open("convert.pe","w") as file:
        file.write(text)
    os.system("chmod 777 convert.pe")
    cmd = f'{fontforge} --appimage-extract-and-run -script "{cdes}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#libreofficecmd
def libreofficecommand(input,new):
    cmd = f'{libreoffice} --appimage-extract-and-run --headless --convert-to "{new}" "{input}" --outdir "{dirPath}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#tesseractcmd
def tesrctcommand(input,output):
    cmd = f'{tesseract} --appimage-extract-and-run "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#ffmpegcmd
def ffmpegcommand(input,output):
    cmd = f'{ffmpeg} -i "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#magiccmd
def magickcommand(input,output):
    cmd = f'{magick} --appimage-extract-and-run "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd  

#app
@app.on_message(filters.command(['start']))
def echo(client, message):
    app.send_message(message.chat.id,f"Welcome\nSend a File first and then Extension\n\nAvailable formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}\n\nDocuments: {LB}\n\nFonts: {FF}")
    

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

    elif message.document.file_name.upper().endswith(LB): 
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {LB}')

    elif message.document.file_name.upper().endswith(FF): 
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {FF}')

    else:
        app.send_message(message.chat.id,f'Available formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}\n\nDocuments: {LB}\n\nFonts: {FF}')

@app.on_message(filters.video)
def video(client, message):
    if message.video.file_name.upper().endswith(VIDAUD): 
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
