import os
from telegraph import Telegraph

# setting
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
telegraph = Telegraph()
telegraph.create_account(short_name='file-converter')


# calibre cmd
def calibrecommand(inputt,output):
    cmd = f'ebook-convert "{inputt}" "{output}" --enable-heuristics'
    print("Command to be Executed is")
    print(cmd)
    return cmd


# fontforge cmd
def fontforgecommand(inputt,output,message):
    des = dirPath + f"/{output}"
    cdes = dirPath + f"/{message.id}-convert.pe"
    text = f'Open(\'{inputt}\')\nGenerate(\'{des}\')'
    with open(f"{message.id}-convert.pe","w") as file:
        file.write(text)
    os.system(f"chmod 777 {message.id}-convert.pe")
    #cmd = f'{fontforge} --appimage-extract-and-run -script "{cdes}"'
    cmd = f'fontforge -script "{cdes}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd


# libreoffice cmd
def libreofficecommand(inputt,new):
    #cmd = f'{libreoffice} --appimage-extract-and-run --headless --convert-to "{new}" "{inputt}" --outdir "{dirPath}"'
    if inputt.split(".")[-1] == 'pdf':
        cmd = f'libreoffice --infilter=="writer_pdf_import" --headless --convert-to "{new}":"writer_pdf_Export" "{inputt}" --outdir "{dirPath}"'
    else:
        cmd = f'libreoffice --headless --convert-to "{new}" "{inputt}" --outdir "{dirPath}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd


# tesseract cmd
def tesrctcommand(inputt,out):
    #cmd = f'{tesseract} --appimage-extract-and-run "{inputt}" "{output}"'
    cmd = f'tesseract "{inputt}" {out}'
    print("Command to be Executed is")
    print(cmd)
    return cmd


# ffmpeg cmd
def ffmpegcommand(inputt,output,new):
    #cmd = f'{ffmpeg} -i "{inputt}" "{output}"'
    if new in  ["mp4", "mkv", "mov"] and not (new == "mov" and ".webm" in inputt):
        cmd = f'ffmpeg -i "{inputt}" -c copy "{output}"'
    else:
        cmd = f'ffmpeg -i "{inputt}" "{output}"'
    print("Command to be Executed is")
    print(cmd)
    return cmd


# magic cmd (imagemagic)
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


# 7zip cmd
def zipcommand(file,message):
    cmd = f'7z x "{file}" -o{message.id}z'
    print("Command to be Executed is")
    print(cmd)
    return cmd, f'{message.id}z'


# zip info
def ziplist(file,message):
    os.system(f'7z l "{file}" > {message.id}zl')
    with open(f'{message.id}zl', 'r') as f:
        lines = f.read().splitlines()
    last_line = lines[-1]
    os.remove{f'{message.id}zl')
    text = ''
    if "folders" in last_line:
        fld = last_line[-2]
        text = f'**{fld}** __Folders__\n'
        i = 2
    else:
        i = 0 

    last_line = last_line.split(" ")
    fil = last_line[-(2+i)]
    com = last_line[-(4+i)]
    siz = last_line[-(10+i)]

    text = f'{text}**{fil}** __Files__\n**{com}** __Compressed Size__\n**{siz}** __Actual Size__'
    return text


# new file name
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

# image info
def imageinfo(file):
    cmd = f'identify -verbose {file} > "{file}.txt"'
    os.system(cmd)

    with open(f'{file}.txt', "rb") as infile:
        info = str(infile.read())
    os.remove(f'{file}.txt')
   
    info = info.replace(":", ": ")
    info = info.replace("b'","")
    info = info.replace("'","")
    info = info.replace("\\n","<br>")
    
    file = file.split("downloads")[-1]
    if file[0] == '/':
       file = file[1:]
    try:
        response = telegraph.create_page(f'{file.replace("./", "")}', html_content=f"<p>{info}</p>")
    except:
        return "Error in getting Info"
    return response['url']


# video info
def videoinfo(file):
    cmd = f'ffprobe -v quiet -show_format -show_streams "{file}" > "{file}.txt"'
    print(cmd)
    os.system(cmd)
    with open(f'{file}.txt', "rb") as infile:
        info = str(infile.read())

    os.remove(f'{file}.txt')

    stream = info[10:].split("[/STREAM]")
    try:
        formats = str(stream[1])[10:-12]
    except:
        formats = ""
    stream = stream[0]

    info = formats + stream[2:]
    info = info.replace("=", "     =        ")
    info = info.replace("\\n", "<br>")
    info = info.replace(":", "   ")
    info = info.replace("./", "")

    file = file.split("downloads")[-1]
    if file[0] == "/":
        file = file[1:]
    
    try:
        response = telegraph.create_page(f'{file.replace("./", "")}', html_content=f"<p>{info}</p>")
    except:
        return "Error in getting Info"
    return response["url"]   


# list beautifier
def give_name(data):
    name = ""
    for i in data:
        name += ", " + str(i)
    return name[2:]
