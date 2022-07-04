from pyrogram import Client
from pyrogram import filters
import os
import threading
import pickle
import os.path

#env
bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")

#binaries not used
# path = './binaries'
# isdir = os.path.isdir(path)
# if not isdir:  
#     link = "wget https://github.com/bipinkrish/file-converter-telegram-bot/releases/download/binaries/binaries.zip"
#     os.system(link)
#     os.system("unzip binaries.zip")
#     os.remove("binaries.zip")

#bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

#setting
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)

#binaries settngs not used
# ffmpeg = dirPath + "/binaries" + "/ffmpeg/ffmpeg"
# magick = dirPath + "/binaries" + "/magick"
# tesseract = dirPath + "/binaries" + "/tesseract"
# libreoffice = dirPath + "/binaries" + "/LibreOffice"
# #libreoffice = dirPath + "/lb" + "/AppRun"
# fontforge = dirPath + "/binaries" + "/FontForge"
# os.system(f"chmod 777 {ffmpeg} {magick} {tesseract} {libreoffice} {fontforge}")

#suporrtedextension
VIDAUD = ("AIFF","AAC","M4A","OGA","WMA","FLAC","WAV","OPUS","OGG","MP3","MKV","MP4","MOV","AVI","M4B","VOB","DVD","WEBM","WMV")
IMG = ("OCR","ICO","GIF","TIFF","TIF","BMP","WEBP","JP2","JPEG","JPG","PNG")
#LB = ("ODT","CSV","DB","DOC","DOCX","DOTX","FODP","FODS","FODT","MML","ODB","ODF","ODG","ODM","ODP","ODS","OTG","OTP","OTS","OTT","OXT","PDF","PPTX","PSW","SDA","SDC","SDD","SDP","SDW","SLK:","SMF","STC","STD","STI","STW","SXC","SXG","SXI","SXM","SXW","UOF","UOP","UOS","UOT","VSD","VSDX","WDB","WPS","WRI","XLS","XLSX")
LB = ("ODT","DOC","DOCX","DOTX","PDF")
FF = ("SFD","BDF","FNT","OTF","PFA","PFB","TTC","TTF","UFO","WOFF")
EB = ("EPUB","MOBI","AZW3","KFX","FB2","HTMLZ","LIT","LRF","PDB","PDF","TXT","ZIP")

#main
def follow(message,input,new):
    output = updtname(input,new)

    if output.upper().endswith(VIDAUD):
        print("It is VID/AUD option")
        file = app.download_media(message)
        cmd = ffmpegcommand(file,output,new)
        os.system(cmd)
        os.remove(file)
        try:
            app.send_document(message.chat.id,document=output)
        except:
            app.send_message(message.chat.id,"Error while conversion")
        os.remove(output)

    elif output.upper().endswith(IMG):
        print("It is IMG option")
        file = app.download_media(message)
        cmd = magickcommand(file,output,new)
        os.system(cmd)
        try:
            app.send_document(message.chat.id,document=output)
        except:
            app.send_message(message.chat.id,"Error while conversion")
        os.remove(output)
        if new == "ocr":
            cmd = tesrctcommand(file,"ocr")
            os.system(cmd)
            app.send_document(message.chat.id,document="ocr.txt")
            os.remove("ocr.txt")
        if new == "ico":
            slist = ["256", "128", "96", "64", "48", "32", "16"]
            for ele in slist:
                toutput = updtname(input,f"-{ele}.png")
                os.system(toutput)
        os.remove(file)

    elif output.upper().endswith(EB) and input.upper().endswith(EB):
        print("It is Ebook option")
        file = app.download_media(message)
        cmd = calibrecommand(file,output)
        os.system(cmd)
        os.remove(file)
        try:
            app.send_document(message.chat.id,document=output)
        except:
            app.send_message(message.chat.id,"Error while conversion")
        os.remove(output)

    elif output.upper().endswith(LB):
        print("It is LibreOffice option")
        file = app.download_media(message)
        cmd = libreofficecommand(file,new)
        os.system(cmd)
        os.remove(file)
        try:
            app.send_document(message.chat.id,document=output)
        except:
            app.send_message(message.chat.id,"Error while conversion")
        os.remove(output)

    elif output.upper().endswith(FF):
        print("It is FontForge option")
        file = app.download_media(message)
        cmd = fontforgecommand(file,output)
        os.system(cmd)
        os.remove("convert.pe")
        os.remove(file)
        try:
            app.send_document(message.chat.id,document=output)
        except:
            app.send_message(message.chat.id,"Error while conversion")
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

#calibrecmd
def calibrecommand(input,output):
    cmd = f'ebook-convert "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#fontforgecmd
def fontforgecommand(input,output):
    des = dirPath + f"/{output}"
    cdes = dirPath + "/convert.pe"
    text = f'Open(\'{input}\')\nGenerate(\'{des}\')'
    with open("convert.pe","w") as file:
        file.write(text)
    os.system("chmod 777 convert.pe")
    #cmd = f'{fontforge} --appimage-extract-and-run -script "{cdes}"'
    cmd = f'fontforge -script "{cdes}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#libreofficecmd
def libreofficecommand(input,new):
    #cmd = f'{libreoffice} --appimage-extract-and-run --headless --convert-to "{new}" "{input}" --outdir "{dirPath}"'
    cmd = f'libreoffice --headless --convert-to "{new}" "{input}" --outdir "{dirPath}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#tesseractcmd
def tesrctcommand(input,output):
    #cmd = f'{tesseract} --appimage-extract-and-run "{input}" "{output}"'
    cmd = f'tesseract "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#ffmpegcmd
def ffmpegcommand(input,output,new):
    #cmd = f'{ffmpeg} -i "{input}" "{output}"'
    if new in  ["mp4", "mkv", "mov", "webm"]:
        cmd = f'ffmpeg -i "{input}" -c copy "{output}"'
    else:
        cmd = f'ffmpeg -i "{input}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#magiccmd
def magickcommand(input,output,new):
    #cmd = f'{magick} --appimage-extract-and-run "{input}" "{output}"'
    if new == "ico":
        cmd = "convert"
        slist = ["256", "128", "96", "64", "48", "32", "16"]
        for ele in slist:
           toutput = updtname(input,f"-{ele}.png")
           tcmd = f'convert "{input}" -resize {ele}x{ele}\! "{toutput}"'
           os.system(tcmd)
           cmd = f'{cmd} {toutput}'
        cmd = f'{cmd} "{output}"'
        print("Command to be Executed is")
        print(cmd)
        return cmd  
    else:
        cmd = f'convert "{input}" "{output}"'
        print("Command to be Executed is")
        print(cmd)
        return cmd  

#app
@app.on_message(filters.command(['start']))
def echo(client, message):
    app.send_message(message.chat.id,f"Welcome\nSend a File first and then Extension\n\nAvailable formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}\n\nDocuments: {LB}\n\nFonts: {FF}\n\nEBooks: {EB}")
 
@app.on_message(filters.command(['help']))
def echo(client, message):
    app.send_message(message.chat.id,"/start - to check availabe conversions\n/help - this message\n/source - github source code\n/feedback - send feedback or report problems with the bot")

@app.on_message(filters.command(['source']))
def echo(client, message):
    app.send_message(message.chat.id,"GITHUB - https://github.com/bipinkrish/file-converter-telegram-bot")
    
@app.on_message(filters.command(['feedback']))
def echo(client, message):
    try:
        text = message.text.split("feedback ")[1]
        app.send_message(623741973,f'from: {message.from_user.id}\n\n{text}')
        app.send_message(message.chat.id,"Thank You for your feedback")    
    except:
        app.send_message(message.chat.id,"no message to send\nexample: /feedback Wonderfull Bot!") 
        
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

    elif message.document.file_name.upper().endswith(EB): 
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        app.send_message(message.chat.id,f'Now send extension to Convert to...\n\nAvailable formats: {EB}')

    else:
        app.send_message(message.chat.id,f'Available formats:\n\nIMAGES: {IMG}\n\nVIDEOS/AUDIOS: {VIDAUD}\n\nDocuments: {LB}\n\nFonts: {FF}\n\nEBooks: {EB}')

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
            app.send_message(message.chat.id,"Warning: for ICO, image will be resized and made multi-resolution")
        app.send_message(message.chat.id,f'Converting from {oldext.upper()} to {newext.upper()}')
        conv = threading.Thread(target=lambda:follow(nmessage,input,newext),daemon=True)
        conv.start()

#apprun
app.run()
