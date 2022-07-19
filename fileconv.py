import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram import enums
import os
import threading
import pickle
import os.path
from telegraph import Telegraph
import shutil
import sys
from buttons import *
import pycolorizer
import positive

#env
bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
owner_id = os.environ.get("OWNERID", "")

#bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)
telegraph = Telegraph()
telegraph.create_account(short_name='1337')

#global
global task
task = 0

#setting
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
os.system("chmod 777 c41lab.py")
os.system("chmod 777 negfix8")


#suporrtedextension
VIDAUD = ("AIFF","AAC","M4A","OGA","WMA","FLAC","WAV","OPUS","OGG","MP3","MKV","MP4","MOV","AVI","M4B","VOB","DVD","WEBM","WMV")
IMG = ("OCR","ICO","GIF","TIFF","BMP","WEBP","JP2","JPEG","JPG","PNG","COLORIZE","POSITIVE")
LBW = ("ODT","DOC","DOCX","DOTX","PDF","XML","HTML","DOTM","WPS","OTT","TXT")
LBI = ("ODP","PPT","PPTX","PPTM","PPSX","POTM","POTX","PPS","POT","ODG","OTP","XML","PDF")
LBC = ("ODS","XLS","HTML","XLSX","XLSM","XLTM","XLTX","OTS","XML","PDF","CSV","XLM")
FF = ("SFD","BDF","FNT","OTF","PFA","PFB","TTC","TTF","UFO","WOFF")
EB = ("EPUB","MOBI","AZW3","KFX","FB2","HTMLZ","LIT","LRF","PDB","PDF","TXT","ZIP")

#main
def follow(message,inputt,new):
    global task
    output = updtname(inputt,new)
    task = task + 1

    if output.upper().endswith(VIDAUD) and inputt.upper().endswith(VIDAUD):
        print("It is VID/AUD option")
        file = app.download_media(message)
        srclink = videoinfo(file)
        cmd = ffmpegcommand(file,output,new)
        os.system(cmd)
        os.remove(file)
        conlink = videoinfo(output)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, caption=f'Source File : {srclink}\n\nConverted File : {conlink}')
            # app.send_message(owner_id,f'SUCCESS\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        except:
            app.send_message(message.chat.id,"Error while conversion")
            try:
                app.send_document(owner_id,document=message.document.file_id,caption=f'FAILED\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
            except:
                try:
                    app.send_document(owner_id,document=message.video.file_id,caption=f'FAILED\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
                except:
                    app.send_document(owner_id,document=message.audio.file_id,caption=f'FAILED\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')

        task = task -1
        os.remove(output)

    elif output.upper().endswith(IMG) and inputt.upper().endswith(IMG):
        print("It is IMG option")
        file = app.download_media(message)
        srclink = imageinfo(file)
        cmd = magickcommand(file,output,new)
        os.system(cmd)
        conlink = imageinfo(output)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, caption=f'Source File : {srclink}\n\nConverted File : {conlink}')
            # app.send_message(owner_id,f'SUCCESS\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        except:
            app.send_message(message.chat.id,"Error while conversion")
            app.send_document(owner_id,document=message.document.file_id,caption=f'FAILED\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        os.remove(output)

        if new == "ocr":
            cmd = tesrctcommand(file,"ocr")
            os.system(cmd)
            with open("ocr.txt","r") as ocr:
                text = ocr.read()
            os.remove("ocr.txt")
            app.send_message(message.chat.id,text)
            
        if new == "ico":
            slist = ["256", "128", "96", "64", "48", "32", "16"]
            for ele in slist:
                toutput = updtname(inputt,f"{ele}.png")
                os.remove(toutput)
        task = task -1
        os.remove(file)

    elif output.upper().endswith(EB) and inputt.upper().endswith(EB):
        print("It is Ebook option")
        file = app.download_media(message)
        cmd = calibrecommand(file,output)
        os.system(cmd)
        os.remove(file)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output)
            # app.send_message(owner_id,f'SUCCESS\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        except:
            app.send_message(message.chat.id,"Error while conversion")
            app.send_document(owner_id,document=message.document.file_id,caption=f'FAILED\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        task = task -1
        os.remove(output)

    elif (output.upper().endswith(LBW) and inputt.upper().endswith(LBW)) or (output.upper().endswith(LBI) and inputt.upper().endswith(LBI)) or (output.upper().endswith(LBC) and inputt.upper().endswith(LBC)):
        print("It is LibreOffice option")
        file = app.download_media(message)
        cmd = libreofficecommand(file,new)
        os.system(cmd)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output)
            # app.send_message(owner_id,f'SUCCESS\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        except:
            app.send_message(message.chat.id,"Error while conversion")
            app.send_document(owner_id,document=message.document.file_id,caption=f'FAILED\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        task = task -1
        os.remove(file)
        os.remove(output)

    elif output.upper().endswith(FF) and inputt.upper().endswith(FF):
        print("It is FontForge option")
        file = app.download_media(message)
        cmd = fontforgecommand(file,output)
        os.system(cmd)
        os.remove("convert.pe")
        os.remove(file)
        try:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output)
            # app.send_message(owner_id,f'SUCCESS\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        except:
            app.send_message(message.chat.id,"Error while conversion")
            app.send_document(owner_id,document=message.document.file_id,caption=f'FAILED\n\nFrom: {message.from_user.id}\nTask : {message.id}\n\n{inputt} to {new.upper()}')
        task = task -1
        os.remove(output)

    else:
        app.send_message(message.chat.id,"Send me valid Extension")
        task = task -1

# negative to positive
def negetivetopostive(message):
    file = app.download_media(message)
    output = file.split("/")[-1]

    print("using c41lab")
    os.system(f'./c41lab.py "{file}" "{output}"')
    app.send_document(message.chat.id,document=output,caption="used tool -> c41lab")
    os.remove(output)
    
    print("using simple tool")
    positive.positiver(file,output)
    app.send_document(message.chat.id,document=output,caption="used tool -> simple tool")
    os.remove(output)
    
    print("using negfix8")
    os.system(f'./negfix8 "{file}" "{output}"')
    app.send_document(message.chat.id,document=output,caption="used tool -> negfix8")
    os.remove(output)

    os.remove(file)

# color image
def colorizeimage(message):
    file = app.download_media(message)
    output = file.split("/")[-1]

    pycolorizer.colorize_image(output,file)
    app.send_document(message.chat.id,document=output)
    os.remove(output)

    os.remove(file)

#newfilename
def updtname(inputt,new):
    inputt = inputt.split(".")
    inputt[-1] = new
    output = ""
    for ele in inputt:
        output = output+"."+ele
    output = output[1:]
    print(f'New Filename will be' )
    print(output)
    return output

#calibrecmd
def calibrecommand(inputt,output):
    cmd = f'ebook-convert "{inputt}" "{output}" --enable-heuristics'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#fontforgecmd
def fontforgecommand(inputt,output):
    des = dirPath + f"/{output}"
    cdes = dirPath + "/convert.pe"
    text = f'Open(\'{inputt}\')\nGenerate(\'{des}\')'
    with open("convert.pe","w") as file:
        file.write(text)
    os.system("chmod 777 convert.pe")
    #cmd = f'{fontforge} --appimage-extract-and-run -script "{cdes}"'
    cmd = f'fontforge -script "{cdes}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#libreofficecmd
def libreofficecommand(inputt,new):
    #cmd = f'{libreoffice} --appimage-extract-and-run --headless --convert-to "{new}" "{inputt}" --outdir "{dirPath}"'
    if inputt.split(".")[-1] == 'pdf':
        cmd = f'libreoffice --infilter=="writer_pdf_import" --headless --convert-to "{new}":"writer_pdf_Export" "{inputt}" --outdir "{dirPath}"'
    else:
        cmd = f'libreoffice --headless --convert-to "{new}" "{inputt}" --outdir "{dirPath}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#tesseractcmd
def tesrctcommand(inputt,output):
    #cmd = f'{tesseract} --appimage-extract-and-run "{inputt}" "{output}"'
    cmd = f'tesseract "{inputt}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#ffmpegcmd
def ffmpegcommand(inputt,output,new):
    #cmd = f'{ffmpeg} -i "{inputt}" "{output}"'
    if new in  ["mp4", "mkv", "mov", "webm"]:
        cmd = f'ffmpeg -i "{inputt}" -c copy "{output}"'
    else:
        cmd = f'ffmpeg -i "{inputt}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd

#magiccmd
def magickcommand(inputt,output,new):
    #cmd = f'{magick} --appimage-extract-and-run "{inputt}" "{output}"'
    if new == "ico":
        cmd = "convert"
        slist = ["256", "128", "96", "64", "48", "32", "16"]
        for ele in slist:
           toutput = updtname(inputt,f"{ele}.png")
           tcmd = f'convert "{inputt}" -resize {ele}x{ele}\! "{toutput}"'
           os.system(tcmd)
           cmd = f'{cmd} "{toutput}"'
        cmd = f'{cmd} "{output}"'
    else:
        cmd = f'convert "{inputt}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd  

#imageinfo
def imageinfo(file):
    cmd = f'identify -verbose {file} > {file}.txt'
    os.system(cmd)

    with open(f"{file}.txt", "r") as infofile:
        info = infofile.read()
    os.remove(f'{file}.txt')
    file = file.split("downloads")[-1]
    if file[0] == '/':
       file = file[1:]
    response = telegraph.create_page(f'{file}',html_content=f'<p>{info}</p>')
    return response['url']

#videoinfo
def videoinfo(file):
    cmd = f'ffprobe -v quiet -show_format -show_streams "{file}" > "{file}.txt"'
    print(cmd)
    os.system(cmd)
    with open(f"{file}.txt", "rb") as infile:
        info = str(infile.read())

    os.remove(f"{file}.txt")

    stream = info[10:].split("[/STREAM]")
    formats = str(stream[1])[10:-12]
    stream = stream[0]

    info = formats + stream[2:]
    info = info.replace("=", "     =        ")
    info = info.replace("\\n", "<br>")
    info = info.replace(":", "   ")
    info = info.replace("./", "")

    file = file.split("downloads")[-1]
    if file[0] == "/":
        file = file[1:]
    print(file)
    response = telegraph.create_page(
        f'{file.replace("./", "")}', html_content=f"<p>{info}</p>"
    )
    return response["url"]

#listbeautifier
def give_name(data):
    name = ""
    for i in data:
        name += ", " + str(i)
    return name[1:]

#app
@app.on_message(filters.command(['start']))
def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"Welcome {message.from_user.mention}\nSend a File first and then Extension\n\n"
                                      f"Available formats:\n\nIMAGES: {give_name(IMG)}\n\nVIDEOS/AUDIOS: {give_name(VIDAUD)}\n\nDocuments: {give_name(LBW)},{give_name(LBI)},{give_name(LBC)}\n\nFonts: {give_name(FF)}\n\nEBooks: {give_name(EB)}")


@app.on_message(filters.command(['help']))
def help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id,
                     "/start - to check availabe conversions\n/help - this message\n/source - github source code\n/feedback - send feedback or report problems with the bot")


@app.on_message(filters.command(['source']))
def source(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, "GITHUB - https://github.com/bipinkrish/File-Converter-Bot")


@app.on_message(filters.command(['feedback']))
def feedback(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    try:
        text = message.text.split("feedback ")[1]
        app.send_message(owner_id, f'from: {message.from_user.id}\n\n{text}')
        app.send_message(message.chat.id, "Thank You for your feedback")
    except:
        app.send_message(message.chat.id, "no message to send\nexample: /feedback Wonderfull Bot!")


@app.on_message(filters.command(['sendmess']))
def echo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if int(message.from_user.id) == int(owner_id):
        text = message.text.split("sendmess ")[1]
        uid = int(text.split(" ")[0])
        text = text[10:]
        app.send_message(uid, text)
        app.send_message(message.chat.id, "Message Sent")
    else:
        app.send_message(message.chat.id, "Unauthorized")


@app.on_message(filters.command(['tasks']))
def echo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    global task
    if int(message.from_user.id) == int(owner_id):
        app.send_message(message.chat.id, f"Total Tasks Running : {task}")
    else:
        app.send_message(message.chat.id, "Unauthorized")


@app.on_message(filters.command(['restrt']))
def rstrt(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if int(message.from_user.id) == int(owner_id):
        shutil.rmtree("downloads")
        app.send_message(owner_id, 'Bot Restarting')
        os.execv(sys.executable, ['python3'] + sys.argv)
    else:
        app.send_message(message.chat.id, "Unauthorized")

@app.on_message(filters.command(["color"]))
def cdocumnet(client, message):
    app.send_message(message.chat.id,'Processing',reply_markup=ReplyKeyboardRemove())
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')
    else:
        app.send_message(message.chat.id,"First send me a File")

    col = threading.Thread(target=lambda:colorizeimage(nmessage),daemon=True)
    col.start()
    
@app.on_message(filters.command(["positive"]))
def pdocumnet(client, message):
    app.send_message(message.chat.id,'Processing',reply_markup=ReplyKeyboardRemove())
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')
    else:
        app.send_message(message.chat.id,"First send me a File")

    pos = threading.Thread(target=lambda:negetivetopostive(nmessage),daemon=True)
    pos.start()   

@app.on_message(filters.document)
def documnet(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.document.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(VIDAUD)}\n\n{message.from_user.mention} choose:',
                         reply_markup=VAboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(IMG):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(IMG)}\n\n{message.from_user.mention} choose:',
                         reply_markup=IMGboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBW):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(LBW)}\n\n{message.from_user.mention} choose:',
                         reply_markup=LBWboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBC):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(LBC)}\n\n{message.from_user.mention} choose:',
                         reply_markup=LBCboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBI):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(LBI)}\n\n{message.from_user.mention} choose:',
                         reply_markup=LBIboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(FF):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(FF)}\n\n{message.from_user.mention} choose:',
                         reply_markup=FFboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(EB):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(EB)}\n\n{message.from_user.mention} choose:',
                         reply_markup=EBboard, reply_to_message_id=message.id)

    else:
        app.send_message(message.chat.id,
                         f'Available formats:\n\nIMAGES: {give_name(IMG)}\n\nVIDEOS/AUDIOS: {give_name(VIDAUD)}\n\nDocuments: {give_name(LBW)} {give_name(LBI)} {give_name(LBC)}\n\nFonts: {give_name(FF)}\n\nEBooks: {give_name(EB)}',
                         reply_to_message_id=message.id)


@app.on_message(filters.video)
def video(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.video.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.video.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(VIDAUD)}\n\n{message.from_user.mention} choose:',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'Available formats:\n\nVIDEOS/AUDIOS: {give_name(VIDAUD)}',
                         reply_to_message_id=message.id)


@app.on_message(filters.audio)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.audio.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.audio.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: {dext} \nNow send extension to Convert to...\n\nAvailable formats: {give_name(VIDAUD)}\n\n{message.from_user.mention} choose:',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'Available formats:\n\nVIDEOS/AUDIOS: {VIDAUD}',
                         reply_to_message_id=message.id)


@app.on_message(filters.photo)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                     f'Detected Extension: JPG \nNow send extension to Convert to...\n\nAvailable formats: {give_name(IMG)}\n\n{message.from_user.mention} choose:',
                     reply_markup=IMGboard, reply_to_message_id=message.id)


@app.on_message(filters.text)
def text(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if "/color" in message.text or "/positive" in message.text:
        return
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')

        if "document" in str(nmessage):
            inputt = nmessage.document.file_name
            print("File is a Document")
        else:
            if "audio" in str(nmessage):
                inputt = nmessage.audio.file_name
                print("File is a Audio")
            else:
                if "video" in str(nmessage):
                    inputt = nmessage.video.file_name
                    print("File is a Video")
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
        if newext == "ico":
            app.send_message(message.chat.id, "Warning: for ICO, image will be resized and made multi-resolution",
                             reply_to_message_id=message.id)
        app.send_message(message.chat.id, f'Converting from {oldext.upper()} to {newext.upper()}',
                         reply_to_message_id=message.id, reply_markup=ReplyKeyboardRemove())
        conv = threading.Thread(target=lambda: follow(nmessage, inputt, newext), daemon=True)
        conv.start()
    else:
        app.send_message(message.chat.id, "First send me a File", reply_to_message_id=message.id,
                         reply_markup=ReplyKeyboardRemove())
        
        
#apprun
app.run()
